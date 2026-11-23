# Entrega LO2 — onde cada item da rubrica está

Os comandos abaixo foram executados em 23/11/2026 na raiz do repositório. Neste ambiente o interpretador é `python3`. O comando documentado para o VS Code continua `python run_pipeline.py`.

## ST4

### 4.1 Arquivos e lote

Tarefa, usuário, entradas e saídas: `README.md`, seções "Problema" e "Como executar".

Regras reaproveitadas e o que mudou em relação ao `theme2.py`: `pipeline/rules.py` (a função `calculate_booking`) e `README.md`, seção "Adaptações em relação ao theme2.py". `theme1.py` e `theme2.py` não foram editados.

Dois CSV compatíveis na mesma execução: `data/raw/reservas_2026-09.csv` e `data/raw/reservas_2026-10.csv`. A leitura está em `acquire_bookings` (`pipeline/batch.py`) e não entra em subpastas, então o exemplo inválido fica de fora. Cada linha ganha `source_file`.

O log da execução `20261123T151129` mostra os dois arquivos num único comando:

```text
passo=aquisicao diretorio=data/raw
arquivo=reservas_2026-09.csv
arquivo=reservas_2026-10.csv
linhas_lidas=86
arquivos_gravados=processado_reservas_2026-09.csv,processado_reservas_2026-10.csv,integrado_noites.csv,fechamento_pousada.xlsx,report.md
passo=fim status=sucesso source_mode=live
```

Os CSV processados estão em `output/run_20261123T151129/`. Os originais continuam em `data/raw`.

### 4.2 Planilha

Geração: `pipeline/spreadsheet.py`, chamado por `store_results`. Arquivo: `output/run_20261123T151129/fechamento_pousada.xlsx`.

Abas: Detalhe, Resumo de negócio e Feriados. O resumo por mês e canal é ordenado pela receita líquida, da maior para a menor. Cabeçalho em negrito, largura de coluna, formato de moeda `"R$" #,##0.00`, data `yyyy-mm-dd`, congelamento em `A2` e autofilter na tabela principal. Os valores de dinheiro e de quantidade são números.

Conferência de outubro no relatório da mesma execução:

```text
- Reservas: 39 (esperado 39) — confere
- Diárias: 134 (esperado 134) — confere
- Ocupação: 54,0% (esperado 54,0%) — confere
- Receita líquida: R$ 27.234,12 (esperado R$ 27.234,12) — confere
- Comissão: R$ 3.535,08 (esperado R$ 3.535,08) — confere
```

O terminal imprimiu a mesma conta: `Outubro/2026: 39 reservas, 134 diárias, ocupação 54.0%, líquida 27234.12, comissão 3535.08.`

O bloco "Conferência de outubro/2026" na aba Resumo de negócio repete calculado, esperado e "sim". O pytest `test_pipeline_offline_grava_planilha_com_outubro` relê o xlsx com openpyxl e soma outubro de novo: 39 linhas, 134 diárias, receita 27234.12 e comissão 3535.08.

### 4.3 Relatório e robustez

Relatório: `output/run_20261123T151129/report.md`. Tem o id `20261123T151129`, os dois arquivos, o escopo da pousada, cinco indicadores (reservas, diárias, ocupação, comissão, receita líquida e também o percentual retido), a conferência de outubro, um achado e uma limitação.

O achado separa evidência e interpretação. Evidência do lote: 7 de 61 dias (11,5%), 39 de 292 diárias (13,4%), R$ 7.537,19 de R$ 59.395,10 (12,7%), ocupação 69,6% nesses dias e 58,6% nos demais. Interpretação: pelo limiar declarado de 2 pontos percentuais, o lote não mostra concentração. A limitação diz que a BrasilAPI só tem feriado nacional, que o rateio da receita é igual entre as noites, que a estadia não cruza o mês e que setembro é fictício.

As três regras justificadas estão na seção "Validação" do relatório e, com o mesmo texto de motivo, no README:

1. Campo vazio separa a linha, para não inventar receita.
2. Canal, quarto, hóspedes e noites fora do domínio do `theme2.py` rejeitam o lote, porque não há tarifa.
3. `booking_id` repetido ou quarto sobreposto rejeita o lote, porque a diária seria contada duas vezes.

Lote inválido, comando real:

```text
python3 run_pipeline.py --input-dir data/raw/invalid_example
```

```text
Lote rejeitado. Nenhuma saída de fechamento foi gerada.
- Canal desconhecido em R-BAD-3: "Instagram". [...]
- Noites fora do intervalo em R-BAD-5: "0". [...]
- Quarto 3 com estadias sobrepostas: R-BAD-1 [...] e R-BAD-4 [...].
Status: falha
Execução 20261123T151128
```

O log dessa execução está em `logs/run_20261123T151128.log` (`incompletas=1`, `status=falha`). Não há pasta `output/run_20261123T151128`. A linha incompleta não entrou num fechamento.

Saídas anteriores preservadas: `output/run_20261123T151129` (ao vivo) e `output/run_20261123T151130` (offline) existem juntas. A última execução está em `output/latest_status.json`:

```text
run_id 20261123T151130
status sucesso
source_mode cache
output_dir output/run_20261123T151130
```

O comando único é `python run_pipeline.py` (`run_pipeline.py`). O status também é impresso no terminal (`Status: sucesso` ou `Status: falha`).

### 4.4 Interação

`docs/IA-ST4.md`.

## ST5

### 5.1 API

Pergunta: a ocupação e a receita se concentram em feriados e pontes? Está na seção "Achado" do relatório.

Cliente: `pipeline/api.py`, `fetch_live` e `acquire_holidays`. `GET https://brasilapi.com.br/api/feriados/v1/2026`, sem chave, com `params={"year": 2026}` e timeout de 20 segundos. Erro de HTTP, timeout e falha de conexão viram `ExternalDataError`.

Resposta bruta e metadado: `data/external/feriados_2026.json` e `data/external/feriados_2026.meta.json` (provedor BrasilAPI, endpoint, parâmetros, `retrieved_at` 2026-11-23T15:11:29-03:00, unidades e termos de uso).

O JSON vira DataFrame com as colunas `date`, `name` e `type` em `parse_holiday_payload`. A checagem exige lista, tipos, datas únicas, pelo menos 8 registros e os feriados nacionais fixos. Dado inválido não substitui o cache; sem cache válido a execução para. O relatório descreve essa reação no final.

Modo da fonte no log ao vivo: `source_mode=live http=200 registros=14`. No offline: `source_mode=cache motivo=offline`.

### 5.2 Integração

Definição de linha, chave, cardinalidade e linhas sem correspondente: seção "Dados externos e junção" do relatório e o docstring de `pipeline/integrate.py`.

- Reserva: uma hospedagem.
- Feriado: uma data nacional.
- Integrado: uma noite ocupada, data ISO, chave `night_date`.

Rastreio: `source_file` e `run_id` seguem para `integrado_noites.csv`.

Preservação, no log da execução ao vivo:

```text
integracao reservas=86/86 diarias=292/292 liquida_antes=59395.10 liquida_depois=59395.10 cardinalidade=many_to_one sem_feriado=282 com_feriado=10
```

O pytest `test_integracao_preserva_totais_e_rastreio` confere as mesmas igualdades e a ponte de 05/09, que não é feriado.

### 5.3 Fluxo

Funções: `acquire_bookings` (`pipeline/batch.py`), `validate_batch` (`pipeline/validate.py`), `acquire_holidays` (`pipeline/api.py`), `integrate_bookings` (`pipeline/integrate.py`) e `store_results` (`pipeline/batch.py`). A ordem está em `execute`, em `run_pipeline.py`.

Comando e VS Code: `README.md`, seção "Como executar", e `.vscode/launch.json` (configurações `Pipeline LO2` e `Pipeline LO2 (offline)`).

O que o ST5 acrescenta ao ST4, na mesma pasta de execução: `integrado_noites.csv`, a aba Feriados e a seção de dados externos do `report.md`. O log traz o id e o modo `live` ou `cache`. A execução inválida não ganha pasta de fechamento. A execução ao vivo permanece depois da execução offline.

### 5.4 Interação

`docs/IA-ST5.md`.

## Testes

```text
python3 -m pytest -q --tb=line
.............
13 passed in 1.13s
```

## O que não foi feito

Não há um teste que derrube a rede de propósito para observar o fallback ao vivo. Esse caminho está no código e no teste em que a resposta falsa é inválida e o cache antigo é mantido. O comando `python` não existe neste ambiente; as execuções gravadas usaram `python3`.
