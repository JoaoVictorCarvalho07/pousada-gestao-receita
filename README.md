# Fechamento em lote da pousada (LO2, ST4 e ST5)

A pousada tem 8 quartos (4 Standard a R$ 250, 3 Superior a R$ 320 e 1 Suíte a R$ 420). O problema de negócio é quanto fica no caixa depois da comissão do canal, do café da manhã, da limpeza e da taxa de turismo (repasse). A entrega anterior (`theme1.py` e `theme2.py`) fecha uma cotação e o mês de outubro de 2026 a partir de reservas escritas no próprio programa. Esses dois arquivos não foram alterados.

Esta entrega (LO2) automatiza o fechamento em lote: um comando lê os CSV de setembro e outubro, aplica as mesmas regras de receita, gera planilha, relatório e log (ST4) e cruza as noites ocupadas com os feriados nacionais da BrasilAPI (ST5).

## Como executar

Na raiz do repositório, com as dependências de [`requirements.txt`](requirements.txt):

```bash
python run_pipeline.py
python run_pipeline.py --offline
python -m pytest
```

O primeiro comando consulta a BrasilAPI. O segundo usa o último JSON salvo em [`data/external`](data/external). Os dois gravam pastas diferentes em `output/run_<id>/`, então a execução anterior permanece.

No VS Code, use as configurações [`Pipeline LO2`](.vscode/launch.json) e `Pipeline LO2 (offline)`. As duas rodam [`run_pipeline.py`](run_pipeline.py) com a raiz do repositório como pasta de trabalho.

A última execução e o status ficam em [`output/latest_status.json`](output/latest_status.json) e também na última linha do terminal (`Status: sucesso` ou `Status: falha`).

O exemplo quebrado não entra no comando padrão, porque está numa subpasta:

```bash
python run_pipeline.py --input-dir data/raw/invalid_example
```

Esse comando deve terminar com status falha, sem planilha nova.

Neste ambiente o interpretador pode se chamar `python3`. O comando da disciplina é `python run_pipeline.py`.

## Estrutura

```text
theme1.py / theme2.py             entrega anterior (intactos)
run_pipeline.py                   comando único do LO2
pipeline/                         regras, validação, lote, planilha, relatório, API e junção
data/raw/                         CSV originais (setembro e outubro)
data/raw/invalid_example/         lote inválido, só para demonstrar a recusa
data/external/                    resposta bruta da BrasilAPI e o metadado
docs/entrega-LO2.md               mapa detalhado da rubrica
docs/IA-ST4.md / docs/IA-ST5.md   interação com a ferramenta
tests/test_pipeline.py            testes automatizados
output/run_<id>/                  saídas daquela execução (CSV, planilha, relatório)
output/latest_status.json         última execução e status
logs/run_<id>.log                 passos, arquivos, modo da fonte e sucesso ou falha
.vscode/launch.json               comando único no VS Code
```

As execuções de referência já versionadas são [`output/run_20261123T151129`](output/run_20261123T151129) (ao vivo) e [`output/run_20261123T151130`](output/run_20261123T151130) (offline). Outubro fecha com 39 reservas, 134 diárias, ocupação 54,0%, receita líquida R$ 27.234,12 e comissão R$ 3.535,08.

## Rubrica oficial (ST4 e ST5)

Detalhamento com trechos das execuções: [`docs/entrega-LO2.md`](docs/entrega-LO2.md).

| Critério | Onde está |
| --- | --- |
| **4.1** Files and batch processing | Tarefa, usuário, entradas e saídas neste README. Dois CSV na mesma execução: [`data/raw/reservas_2026-09.csv`](data/raw/reservas_2026-09.csv) e [`data/raw/reservas_2026-10.csv`](data/raw/reservas_2026-10.csv). Leitura em [`pipeline/batch.py`](pipeline/batch.py) (`acquire_bookings`); cada linha leva `source_file`. Regras e adaptações: [`pipeline/rules.py`](pipeline/rules.py) e a seção abaixo. Processados em `output/run_<id>/`. |
| **4.2** Spreadsheet automation | [`pipeline/spreadsheet.py`](pipeline/spreadsheet.py). Exemplo: [`output/run_20261123T151129/fechamento_pousada.xlsx`](output/run_20261123T151129/fechamento_pousada.xlsx) (abas Detalhe, Resumo de negócio e Feriados). Resumo ordenado pela receita líquida. Conferência de outubro na própria planilha e no relatório. |
| **4.3** Reports and robustness | Relatório: [`output/run_20261123T151129/report.md`](output/run_20261123T151129/report.md). Regras e recusa do lote neste README. Log de recusa: [`logs/run_20261123T151128.log`](logs/run_20261123T151128.log). Último status: [`output/latest_status.json`](output/latest_status.json). Comando único: [`run_pipeline.py`](run_pipeline.py). |
| **4.4** Document your AI interaction | [`docs/IA-ST4.md`](docs/IA-ST4.md) |
| **5.1** API integration | [`pipeline/api.py`](pipeline/api.py). Cache e metadado em [`data/external`](data/external). Pergunta, endpoint e reação a dado inválido no relatório e neste README. |
| **5.2** Data acquisition and integration | [`pipeline/integrate.py`](pipeline/integrate.py). CSV integrado: [`output/run_20261123T151129/integrado_noites.csv`](output/run_20261123T151129/integrado_noites.csv). Totais e rastreio no relatório. |
| **5.3** Simple workflow design | Funções nomeadas em `pipeline/`, orquestradas por [`run_pipeline.py`](run_pipeline.py). VS Code: [`.vscode/launch.json`](.vscode/launch.json). |
| **5.4** Document your AI interaction | [`docs/IA-ST5.md`](docs/IA-ST5.md) |

## Continuidade em relação ao theme2.py (pedido de reúso do ST3)

Não há um módulo ou pasta separados com o nome ST3. A lógica de limpeza, validação e agregação reaproveitada no ST4 parte do [`theme2.py`](theme2.py): é a continuidade direta da entrega anterior (caderno mensal, regras de tarifa e fechamento de outubro). As adaptações estão abaixo e em [`pipeline/rules.py`](pipeline/rules.py).

- O check-in deixa de ser o dia 1–31 de um mês fixo e passa a ser data ISO. Setembro e outubro cabem no mesmo lote; o dia 7 dos dois meses não se confunde.
- O programa deixa de pedir `input()` e lê CSV. Entram `booking_id`, `source_file` e `run_id`.
- A ocupação usa os dias reais de cada mês (30 em setembro, 31 em outubro), não um 31 fixo.
- A estadia ainda tem de caber no mês do check-in, como o limite `days_in_month + 1 - checkin` do `theme2.py`.
- A fórmula não mudou: desconto de 0% até 2 noites, 8% de 3 a 6 e 15% a partir de 7; comissão de 15%, 14%, 3% e 0%; hóspede extra a R$ 60 acima de 2 pessoas; café R$ 18 por hóspede por noite; limpeza R$ 70 por reserva; taxa de turismo R$ 4 por hóspede por noite, só como repasse. A receita líquida é a hospedagem menos comissão, café e limpeza. A taxa de turismo não entra na hospedagem e não é descontada de novo.

Se `reservas_2026-10.csv` está no lote e a conta de outubro diverge do fechamento conhecido (39 reservas, 134 diárias, ocupação 54,0%, líquida R$ 27.234,12, comissão R$ 3.535,08), a execução falha e não publica a planilha.

## Regras de validação

1. Campo obrigatório vazio (`booking_id`, `guest`, `channel`, `room`, `checkin`, `nights`, `guests`) torna a linha incompleta. Ela não entra nos totais e, se existir, vai para `incompletas.csv`. Motivo: preencher o vazio no chute inventaria receita. Incompleta não aparece como reserva válida.
2. Canal, quarto, hóspedes e noites têm de cair no domínio do `theme2.py`, e a estadia tem de terminar no mês do check-in. Motivo: fora disso não há tarifa nem comissão. Um valor inválido rejeita o lote inteiro, inclusive as linhas que estariam certas, para não entregar um fechamento parcial com cara de oficial.
3. `booking_id` repetido ou duas estadias no mesmo quarto com noites em comum rejeitam o lote inteiro. Motivo: a reserva seria contada duas vezes, ou a mesma diária seria vendida duas vezes.

Arquivo sem as colunas obrigatórias também rejeita o lote: não é uma linha incompleta, é outro leiaute.

## Feriados e pontes (ST5)

A pergunta que o caderno interno não responde: a ocupação e a receita se concentram em feriados e pontes?

A fonte é a BrasilAPI, `GET https://brasilapi.com.br/api/feriados/v1/{year}`, sem chave, com timeout de 20 segundos. A resposta bruta e o metadado ficam em [`data/external`](data/external). Cada reserva vira uma linha por noite ocupada; a junção é pela data ISO.

Dado externo inválido não substitui o cache. Se o cache antigo for válido, a execução segue com modo `cache`. Se não houver cache válido, o status fica `falha` e não saem CSV, planilha nem relatório.

Na execução [`20261123T151129`](output/run_20261123T151129/report.md), feriados e pontes são 11,5% dos dias, 13,4% das diárias e 12,7% da receita líquida rateada. Pelo limiar de 2 pontos percentuais declarado no relatório, isso não caracteriza concentração, embora a ocupação nesses dias (69,6%) fique acima da dos demais (58,6%).
