"""
SIFSM - Sistema Integrado de Futuro Sustentável em Marte
Colônia Aurora Siger

Execução:
    python codigo_fonte.py

O programa cria o banco SQLite local, importa os dados JSON uma única vez
e oferece menu CRUD, análise lógica, fila de manutenção e simulação energética.
"""

from pathlib import Path
from collections import deque
import sqlite3
import json
import traceback

from simulacao_computacional import executar_analise

PASTA = Path(__file__).resolve().parent
ARQUIVO_BANCO = PASTA / "aurora_siger.db"
ARQUIVO_SQL = PASTA / "script_banco.sql"
ARQUIVO_JSON = PASTA / "dados_aurora_siger.json"

LIMIAR_CONSUMO = 60.0
PRESSAO_MINIMA = 80.0

def conectar():
    conexao = sqlite3.connect(ARQUIVO_BANCO)
    conexao.row_factory = sqlite3.Row
    conexao.execute("PRAGMA foreign_keys = ON")
    return conexao

def inicializar_banco():
    """Cria tabelas e importa JSON apenas se o banco ainda estiver vazio."""
    try:
        with conectar() as con:
            con.executescript(ARQUIVO_SQL.read_text(encoding="utf-8"))
            quantidade = con.execute("SELECT COUNT(*) FROM modulos").fetchone()[0]
            if quantidade == 0:
                importar_json(con)
        print(f"Banco de dados pronto: {ARQUIVO_BANCO.name}")
    except (sqlite3.Error, OSError, json.JSONDecodeError) as erro:
        print(f"Erro ao inicializar o banco: {erro}")
        raise

def importar_json(con):
    dados = json.loads(ARQUIVO_JSON.read_text(encoding="utf-8"))
    for m in dados["modulos"]:
        con.execute("""INSERT INTO modulos
            (codigo, nome, ativo, critico, descricao) VALUES (?, ?, ?, ?, ?)""",
            (m["codigo"], m["nome"], m["ativo"], m["critico"], m["descricao"]))
    for s in dados["sensores"]:
        con.execute("""INSERT INTO sensores
            (codigo, modulo_codigo, tipo, unidade) VALUES (?, ?, ?, ?)""",
            (s["codigo"], s["modulo_codigo"], s["tipo"], s["unidade"]))
    for t in dados["telemetria_inicial"]:
        con.execute("""INSERT INTO telemetria
            (sensor_codigo, ciclo, valor, status) VALUES (?, ?, ?, ?)""",
            (t["sensor_codigo"], t["ciclo"], t["valor"], t["status"]))
    # A fila organiza os chamados de manutenção em ordem de chegada (FIFO).
    fila_manutencao = deque([
        ("COM-01", "Verificar módulo de comunicação", 1),
        ("LAB-01", "Avaliar disponibilidade do laboratório", 3)
    ])
    while fila_manutencao:
        modulo, descricao, prioridade = fila_manutencao.popleft()
        con.execute("""INSERT INTO manutencoes
            (modulo_codigo, descricao, prioridade) VALUES (?, ?, ?)""",
            (modulo, descricao, prioridade))
    print("Dados JSON importados para o banco.")

def listar_modulos():
    with conectar() as con:
        linhas = con.execute("SELECT * FROM modulos ORDER BY codigo").fetchall()
    print("\n--- MODULOS DA AURORA SIGER ---")
    for m in linhas:
        print(f'{m["codigo"]} | {m["nome"]} | '
              f'Ativo: {"SIM" if m["ativo"] else "NAO"} | '
              f'Critico: {"SIM" if m["critico"] else "NAO"}')

def cadastrar_modulo():
    codigo = input("Código (ex.: AGR-01): ").strip().upper()
    nome = input("Nome do módulo: ").strip()
    descricao = input("Descrição: ").strip()
    if not codigo or not nome:
        raise ValueError("Código e nome são obrigatórios.")
    critico = int(input("É crítico? (1=sim, 0=não): "))
    ativo = int(input("Está ativo? (1=sim, 0=não): "))
    if critico not in (0, 1) or ativo not in (0, 1):
        raise ValueError("Os campos ativo e crítico devem ser 0 ou 1.")
    with conectar() as con:
        con.execute("""INSERT INTO modulos
            (codigo, nome, ativo, critico, descricao) VALUES (?, ?, ?, ?, ?)""",
            (codigo, nome, ativo, critico, descricao))
    print("Módulo cadastrado com sucesso.")

def alterar_modulo():
    codigo = input("Código do módulo que deseja alterar: ").strip().upper()
    nome = input("Novo nome: ").strip()
    ativo = int(input("Novo estado (1=ativo, 0=inativo): "))
    if ativo not in (0, 1) or not nome:
        raise ValueError("Nome inválido ou estado diferente de 0/1.")
    with conectar() as con:
        cursor = con.execute("UPDATE modulos SET nome=?, ativo=? WHERE codigo=?",
                             (nome, ativo, codigo))
    print("Registro alterado." if cursor.rowcount else "Código não encontrado.")

def excluir_modulo():
    codigo = input("Código do módulo que deseja excluir: ").strip().upper()
    with conectar() as con:
        cursor = con.execute("DELETE FROM modulos WHERE codigo=?", (codigo,))
    print("Registro excluído." if cursor.rowcount else "Código não encontrado.")
    # A integridade referencial impede excluir módulos ainda referenciados.

def registrar_telemetria():
    sensor = input("Código do sensor: ").strip().upper()
    ciclo = int(input("Número do ciclo: "))
    valor = float(input("Valor medido: ").replace(",", "."))
    status = input("Status (NORMAL/ATENCAO): ").strip().upper() or "NORMAL"
    if ciclo < 1 or status not in ("NORMAL", "ATENCAO"):
        raise ValueError("Ciclo ou status inválido.")
    with conectar() as con:
        con.execute("""INSERT INTO telemetria
            (sensor_codigo, ciclo, valor, status) VALUES (?, ?, ?, ?)""",
            (sensor, ciclo, valor, status))
    print("Leitura registrada.")

def listar_telemetria():
    with conectar() as con:
        linhas = con.execute("""
            SELECT t.id, t.sensor_codigo, s.tipo, t.ciclo, t.valor, s.unidade, t.status
            FROM telemetria t JOIN sensores s ON s.codigo=t.sensor_codigo
            ORDER BY t.ciclo, t.id
        """).fetchall()
    print("\n--- TELEMETRIA ---")
    for t in linhas:
        print(f'ID {t["id"]} | {t["sensor_codigo"]} ({t["tipo"]}) | '
              f'Ciclo {t["ciclo"]} | {t["valor"]} {t["unidade"]} | {t["status"]}')

def aplicar_regra_booleana():
    """Alerta = (consumo alto E módulo crítico) OU integridade falha OU pressão baixa."""
    consumo = float(input("Consumo atual em kWh: ").replace(",", "."))
    codigo = input("Código do módulo associado: ").strip().upper()
    integridade = int(input("Integridade estrutural (1=OK, 0=falha): "))
    pressao = float(input("Pressão do tanque em kPa: ").replace(",", "."))
    if integridade not in (0, 1):
        raise ValueError("Integridade deve ser 0 ou 1.")
    with conectar() as con:
        modulo = con.execute("SELECT critico FROM modulos WHERE codigo=?", (codigo,)).fetchone()
        if modulo is None:
            raise ValueError("Módulo não encontrado.")
        modulo_critico = bool(modulo["critico"])
        consumo_alto = consumo > LIMIAR_CONSUMO
        integridade_falha = integridade == 0
        pressao_baixa = pressao < PRESSAO_MINIMA
        alerta = (consumo_alto and modulo_critico) or integridade_falha or pressao_baixa
        nivel = "CRITICO" if integridade_falha or pressao_baixa else ("ATENCAO" if alerta else "INFO")
        mensagem = ("ALERTA: verificar imediatamente o módulo e os parâmetros informados."
                    if alerta else "Condições dentro dos limites definidos.")
        if alerta:
            con.execute("""INSERT INTO alertas
                (ciclo, modulo_codigo, mensagem, nivel) VALUES (?, ?, ?, ?)""",
                (0, codigo, mensagem, nivel))
    print("\nResultado da regra booleana:")
    print(f"Consumo alto: {consumo_alto}; módulo crítico: {modulo_critico}")
    print(f"Falha de integridade: {integridade_falha}; pressão baixa: {pressao_baixa}")
    print(f"Expressão: ({consumo_alto} AND {modulo_critico}) OR "
          f"{integridade_falha} OR {pressao_baixa}")
    print(mensagem)

def listar_alertas():
    with conectar() as con:
        linhas = con.execute("SELECT * FROM alertas ORDER BY id DESC").fetchall()
    if not linhas:
        print("Nenhum alerta registrado.")
    for a in linhas:
        print(f'#{a["id"]} | {a["nivel"]} | {a["modulo_codigo"]} | {a["mensagem"]}')

def mostrar_manutencoes():
    with conectar() as con:
        linhas = con.execute("""SELECT * FROM manutencoes
            ORDER BY prioridade ASC, id ASC""").fetchall()
    print("\n--- FILA/PRIORIDADE DE MANUTENÇÃO ---")
    for item in linhas:
        print(f'#{item["id"]} | prioridade {item["prioridade"]} | '
              f'{item["modulo_codigo"]} | {item["descricao"]} | {item["status"]}')

def menu():
    opcoes = {
        "1": ("Listar módulos", listar_modulos),
        "2": ("Cadastrar módulo", cadastrar_modulo),
        "3": ("Alterar módulo", alterar_modulo),
        "4": ("Excluir módulo", excluir_modulo),
        "5": ("Registrar leitura de sensor", registrar_telemetria),
        "6": ("Listar telemetria", listar_telemetria),
        "7": ("Executar regra booleana", aplicar_regra_booleana),
        "8": ("Listar alertas", listar_alertas),
        "9": ("Executar simulação energética e previsão", lambda: executar_analise()),
        "10": ("Consultar manutenções", mostrar_manutencoes),
    }
    while True:
        print("\n========== SIFSM | AURORA SIGER ==========")
        for chave, (descricao, _) in opcoes.items():
            print(f"{chave}. {descricao}")
        print("0. Sair")
        escolha = input("Selecione uma opção: ").strip()
        if escolha == "0":
            print("Encerrando o SIFSM. Até mais!")
            break
        if escolha not in opcoes:
            print("Opção inválida. Escolha uma opção do menu.")
            continue
        try:
            opcoes[escolha][1]()
        except ValueError as erro:
            print(f"Entrada inválida: {erro}")
        except sqlite3.IntegrityError as erro:
            print(f"Falha de integridade do banco (verifique código/referências): {erro}")
        except sqlite3.Error as erro:
            print(f"Erro no banco de dados: {erro}")
        except (OSError, json.JSONDecodeError) as erro:
            print(f"Erro ao acessar arquivo: {erro}")
        except Exception as erro:
            print(f"Erro inesperado: {erro}")
        input("\nPressione ENTER para voltar ao menu...")

if __name__ == "__main__":
    try:
        inicializar_banco()
        menu()
    except Exception:
        print("Não foi possível iniciar o SIFSM.")
        traceback.print_exc()
