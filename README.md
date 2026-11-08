# SIFSM — Sistema Integrado de Futuro Sustentável em Marte

*Projeto:* Colônia Aurora Siger  
*Linguagens:* Python, SQL e JSON  
*Banco de dados:* SQLite

---

## 1. Sobre o projeto

O SIFSM (Sistema Integrado de Futuro Sustentável em Marte) é um protótipo computacional desenvolvido para auxiliar no monitoramento e gerenciamento dos recursos da colônia espacial Aurora Siger.

O sistema reúne informações dos módulos da colônia, registra dados de sensores simulados, identifica possíveis situações de risco e realiza análises relacionadas à geração e ao consumo de energia.

A solução utiliza Python como linguagem principal, SQLite para armazenamento de informações e JSON para organizar os dados iniciais.

## 2. Objetivos

- Monitorar as condições operacionais dos módulos da colônia.
- Organizar e armazenar informações de sensores e telemetria.
- Implementar operações CRUD para gerenciamento dos módulos.
- Identificar situações de risco por meio de regras booleanas.
- Simular a geração e o consumo de energia.
- Realizar previsões de consumo utilizando regressão linear.
- Organizar solicitações de manutenção.
- Contribuir para o planejamento sustentável dos recursos da colônia.

## 3. Tecnologias utilizadas

| Tecnologia | Aplicação |
|---|---|
| Python | Desenvolvimento da aplicação e processamento dos dados |
| SQL | Criação e organização das tabelas |
| SQLite | Banco de dados local |
| JSON | Armazenamento dos dados iniciais |
| Regressão linear | Previsão do consumo energético |

## 4. Estrutura dos arquivos

O projeto está organizado da seguinte maneira:

text
SIFSM/
- codigo_fonte.py
- script_banco.sql
- dados_aurora_siger.json
- simulacao_computacional.py
- circuito_logico.pdf
- README.md


### Descrição dos arquivos

*codigo_fonte.py*

Arquivo principal do sistema. Responsável pelo menu de navegação, integração com o banco de dados, operações CRUD, aplicação da regra booleana e execução da simulação energética.

*script_banco.sql*

Contém os comandos SQL responsáveis pela criação das tabelas do banco SQLite.

*dados_aurora_siger.json*

Armazena os dados iniciais da colônia, incluindo módulos, sensores e registros iniciais de telemetria.

*simulacao_computacional.py*

Executa a simulação energética, calcula os saldos entre geração e consumo e realiza a previsão dos próximos ciclos por regressão linear.

*circuito_logico.pdf*

Documento que apresenta a expressão booleana, o funcionamento das portas lógicas e a tabela-verdade utilizada pelo sistema.

## 5. Módulos monitorados

O sistema trabalha com seis módulos principais:

- Suporte à vida
- Energia
- Comunicação
- Habitat
- Laboratório
- Armazenamento

Cada módulo possui informações de identificação, estado de funcionamento e classificação de criticidade.

## 6. Banco de dados

O banco de dados SQLite possui cinco tabelas principais:

| Tabela | Finalidade |
|---|---|
| modulos | Cadastro e informações dos módulos |
| sensores | Identificação dos sensores |
| telemetria | Armazenamento das leituras |
| alertas | Registro de ocorrências |
| manutencoes | Organização das solicitações de manutenção |

A aplicação utiliza operações CRUD:

- *Create:* cadastrar novos registros.
- *Read:* consultar informações armazenadas.
- *Update:* alterar registros existentes.
- *Delete:* excluir registros.

O banco é inicializado automaticamente pelo programa principal. Na primeira execução, os dados do JSON são importados caso a tabela de módulos esteja vazia.

## 7. Regra booleana e monitoramento

O sistema utiliza uma expressão lógica para identificar condições que exigem atenção operacional.

A expressão implementada é:

text
ALERTA = (C AND M) OR I OR P


Onde:

- C: consumo energético acima de 60 kWh.
- M: módulo classificado como crítico.
- I: falha de integridade estrutural.
- P: pressão do tanque abaixo de 80 kPa.

A porta lógica AND verifica se o consumo está elevado e se o módulo é crítico simultaneamente.

A porta lógica OR combina esse resultado com as condições de falha estrutural e pressão baixa.

Quando uma das condições de alerta é identificada, o sistema registra a ocorrência no banco de dados.

Os limites utilizados são parâmetros didáticos da simulação.

## 8. Simulação computacional e previsão energética

A simulação utiliza dados de geração solar, consumo e nível da bateria.

| Ciclo | Geração (kWh) | Consumo (kWh) | Bateria |
|---|---:|---:|---:|
| 1 | 40 | 45 | 90% |
| 2 | 38 | 50 | 82% |
| 3 | 35 | 58 | 74% |
| 4 | 30 | 65 | 60% |
| 5 | 28 | 70 | 48% |
| 6 | 22 | 78 | 32% |

O saldo energético é calculado pela fórmula:

text
Saldo = Geração - Consumo


A previsão utiliza regressão linear simples:

text
y = ax + b


O modelo estima o consumo dos três ciclos seguintes com base nos seis ciclos simulados.

Os resultados permitem observar a tendência de aumento do consumo e a necessidade de melhorar o planejamento energético.

## 9. Estruturas de dados

O sistema utiliza:

- *Listas:* organização de conjuntos de dados.
- *Dicionários:* representação de registros e informações estruturadas.
- *Deque:* organização de solicitações de manutenção por ordem de chegada, utilizando o princípio FIFO (First In, First Out).

Essas estruturas auxiliam na organização e manipulação das informações.

## 10. Como executar o projeto

### Pré-requisitos

- Python 3 instalado.
- Todos os arquivos do projeto na mesma pasta.

O SQLite e as bibliotecas sqlite3, json, pathlib e collections utilizados pelo projeto fazem parte da biblioteca padrão do Python.

### Passo 1 — Verificar o Python

Abra o terminal e execute:

bash
python --version


### Passo 2 — Abrir a pasta do projeto

No Windows, abra a pasta onde estão os arquivos, clique na barra de endereço do Explorador de Arquivos, digite cmd e pressione Enter.

### Passo 3 — Executar o sistema

No terminal, digite:

bash
python codigo_fonte.py


O programa irá:

1. Inicializar o banco de dados SQLite.
2. Criar as tabelas utilizando o arquivo SQL.
3. Importar os dados iniciais do JSON, caso necessário.
4. Apresentar o menu principal do SIFSM.

## 11. Funcionalidades do menu

Após iniciar o programa, será apresentado o seguinte menu:

| Opção | Funcionalidade |
|---|---|
| 1 | Listar módulos |
| 2 | Cadastrar módulo |
| 3 | Alterar módulo |
| 4 | Excluir módulo |
| 5 | Registrar leitura de sensor |
| 6 | Listar telemetria |
| 7 | Executar regra booleana |
| 8 | Listar alertas |
| 9 | Executar simulação energética e previsão |
| 10 | Consultar manutenções |
| 0 | Encerrar o sistema |

Para utilizar uma funcionalidade, basta digitar o número correspondente no terminal.

## 12. Sustentabilidade e impacto socioambiental

O SIFSM busca demonstrar a importância do gerenciamento eficiente dos recursos em uma colônia espacial.

A análise energética permite identificar períodos em que o consumo supera a geração solar, indicando a necessidade de medidas para reduzir desperdícios e priorizar sistemas essenciais.

Entre as recomendações estão:

- Priorizar o fornecimento energético para sistemas críticos.
- Reduzir o consumo de equipamentos não essenciais.
- Monitorar os níveis de bateria.
- Planejar a expansão da infraestrutura.
- Organizar manutenções preventivas.

## 13. Possibilidades de expansão

O projeto pode ser ampliado futuramente por meio de:

- Integração com sensores físicos e microcontroladores.
- Implementação de agentes de inteligência artificial.
- Análise de dados operacionais em tempo real.
- Modelos matemáticos mais avançados para previsão.
- Sistemas automatizados de recomendação e manutenção.

Essas possibilidades representam evoluções futuras e não funcionalidades implementadas na versão atual.

## 14. Conclusão

O SIFSM demonstra como diferentes conceitos de programação, banco de dados, lógica digital, estruturas de dados e matemática podem ser integrados em uma solução computacional.

O protótipo permite organizar informações da colônia, registrar telemetria, identificar situações de risco e analisar o comportamento energético por meio de simulações e previsões.

Dessa forma, o projeto apresenta uma proposta de apoio à gestão sustentável da colônia Aurora Siger, contribuindo para o planejamento e a utilização responsável dos recursos disponíveis.
