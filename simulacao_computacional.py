"""
Simulações do SIFSM - Aurora Siger.
Não exige bibliotecas externas: utiliza apenas recursos nativos do Python.
"""

DADOS_ENERGIA = {
    "geracao_solar": [40, 38, 35, 30, 28, 22],
    "consumo": [45, 50, 58, 65, 70, 78],
    "bateria": [90, 82, 74, 60, 48, 32]
}

def regressao_linear(valores):
    """Calcula y = a*x + b pelo método dos mínimos quadrados."""
    n = len(valores)
    if n < 2:
        raise ValueError("São necessários pelo menos dois valores.")
    xs = list(range(1, n + 1))
    media_x = sum(xs) / n
    media_y = sum(valores) / n
    denominador = sum((x - media_x) ** 2 for x in xs)
    if denominador == 0:
        raise ValueError("Não foi possível calcular a regressão.")
    a = sum((x - media_x) * (y - media_y) for x, y in zip(xs, valores)) / denominador
    b = media_y - a * media_x
    return a, b

def prever_proximos_ciclos(valores, quantidade=3):
    a, b = regressao_linear(valores)
    inicio = len(valores) + 1
    return [a * x + b for x in range(inicio, inicio + quantidade)]

def simular_energia(dados=None):
    """Compara geração e consumo e estima o saldo energético por ciclo."""
    dados = dados or DADOS_ENERGIA
    geracao = dados["geracao_solar"]
    consumo = dados["consumo"]
    bateria = dados["bateria"]
    if not (len(geracao) == len(consumo) == len(bateria)):
        raise ValueError("As séries de energia devem ter o mesmo tamanho.")

    resultado = []
    saldo_acumulado = 0.0
    for i, (g, c, b) in enumerate(zip(geracao, consumo, bateria), start=1):
        saldo = g - c
        saldo_acumulado += saldo
        resultado.append({
            "ciclo": i,
            "geracao_kwh": g,
            "consumo_kwh": c,
            "saldo_kwh": saldo,
            "bateria_percentual": b,
            "situacao": "DEFICIT" if saldo < 0 else "SUPERAVIT"
        })
    return resultado

def executar_analise(dados=None, imprimir=True):
    dados = dados or DADOS_ENERGIA
    ciclos = simular_energia(dados)
    previsao = prever_proximos_ciclos(dados["consumo"], 3)
    a, b = regressao_linear(dados["consumo"])
    if imprimir:
        print("\\n=== SIMULACAO ENERGETICA DA AURORA SIGER ===")
        print("Ciclo | Geracao | Consumo | Saldo | Bateria | Situacao")
        for item in ciclos:
            print(f'{item["ciclo"]:>5} | {item["geracao_kwh"]:>7.1f} | '
                  f'{item["consumo_kwh"]:>7.1f} | {item["saldo_kwh"]:>5.1f} | '
                  f'{item["bateria_percentual"]:>6.1f}% | {item["situacao"]}')
        print(f"\\nRegressao linear do consumo: y = {a:.2f}x + {b:.2f}")
        for i, valor in enumerate(previsao, start=len(dados["consumo"]) + 1):
            print(f"Previsao do consumo no ciclo {i}: {valor:.2f} kWh")
        print("\\nInterpretacao: a geracao solar ficou abaixo do consumo nos ciclos")
        print("observados. A bateria diminuiu de 90% para 32%, indicando necessidade")
        print("de priorizar cargas essenciais e buscar reduzir o consumo.")
        print("Limitacao: previsao linear baseada em apenas seis ciclos simulados;")
        print("nao representa todas as variacoes ambientais de Marte.")
    return {"ciclos": ciclos, "previsao_consumo": previsao, "coeficientes": (a, b)}

if __name__ == "__main__":
    executar_analise()
