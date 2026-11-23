# Fechamento em lote da pousada (LO2, ST4 e ST5)

A pousada tem 8 quartos: 4 Standard a R$ 250, 3 Superior a R$ 320 e 1 Suíte a R$ 420. O fechamento de um mês já existia em `theme2.py`, com as reservas de outubro de 2026 escritas no próprio programa. Este pipeline repete essa conta para arquivos CSV, em lote, e cruza as noites ocupadas com os feriados nacionais.

`theme1.py` e `theme2.py` ficam como estão.

## Problema

Todo mês a recepção exporta as reservas e a gestão precisa responder, sem redigitar linha por linha:

- quantas diárias foram vendidas e qual foi a ocupação;
- quanto ficou de comissão para Booking, Airbnb, site próprio e WhatsApp;
- qual foi a receita líquida da pousada;
- se ocupação e receita se concentram em feriados e pontes.

Usuário: quem fecha o mês da pousada. Entrada: um ou mais CSV com o mesmo leiaute (`booking_id`, `guest`, `channel`, `room`, `checkin`, `nights`, `guests`). Saída de cada execução: CSV processado por arquivo, CSV de noites integradas, planilha, relatório e log. Os originais em `data/raw` não são alterados.

## Como executar

Na raiz do repositório, com as dependências de `requirements.txt`:

```bash
python run_pipeline.py
python run_pipeline.py --offline
```

O primeiro comando consulta a BrasilAPI. O segundo usa o último JSON salvo em `data/external`. Os dois gravam pastas diferentes em `output/run_<data-hora>/`, então a execução anterior permanece.

No VS Code, as configurações em `.vscode/launch.json` são `Pipeline LO2` e `Pipeline LO2 (offline)`. As duas rodam `run_pipeline.py` com a raiz do repositório como pasta de trabalho.

A última execução e o status ficam em `output/latest_status.json` e também na última linha impressa no terminal (`Status: sucesso` ou `Status: falha`).

O exemplo quebrado não entra no comando padrão, porque está numa subpasta:

```bash
python run_pipeline.py --input-dir data/raw/invalid_example
```

Esse comando deve terminar com status falha, sem planilha. O teste automatizado faz o mesmo:

```bash
python -m pytest
```

## Estrutura

```text
data/raw/                         CSV originais de setembro e outubro
data/raw/invalid_example/         lote propositalmente inválido, só para o teste
data/external/                    resposta bruta da BrasilAPI e o metadado
pipeline/rules.py                 tarifas, desconto, comissão e receita líquida
pipeline/validate.py              incompletas separadas; inválidas rejeitam o lote
pipeline/batch.py                 leitura dos CSV e gravação das saídas
pipeline/spreadsheet.py           planilha Detalhe, Resumo de negócio e Feriados
pipeline/report.py                relatório em texto
pipeline/api.py                   BrasilAPI, validação do JSON e cache
pipeline/integrate.py             expansão das noites e junção pela data
run_pipeline.py                   comando único
output/run_<id>/                  saídas daquela execução
logs/run_<id>.log                 passos, arquivos, modo da fonte e sucesso ou falha
```

## Adaptações em relação ao theme2.py

- O check-in deixa de ser o dia 1–31 de um mês fixo e passa a ser data ISO. Setembro e outubro cabem no mesmo lote; o dia 7 dos dois meses não se confunde.
- O programa deixa de pedir `input()` e lê CSV. Entram `booking_id`, `source_file` e `run_id`.
- A ocupação usa os dias reais de cada mês (30 em setembro, 31 em outubro), não um 31 fixo.
- A estadia ainda tem de caber no mês do check-in, como o limite `days_in_month + 1 - checkin` do theme2.py.
- A fórmula não mudou: desconto de 0% até 2 noites, 8% de 3 a 6 e 15% a partir de 7; comissão de 15%, 14%, 3% e 0%; hóspede extra a R$ 60 acima de 2 pessoas; café R$ 18 por hóspede por noite; limpeza R$ 70 por reserva; taxa de turismo R$ 4 por hóspede por noite, só como repasse. A receita líquida é a hospedagem menos comissão, café e limpeza. A taxa de turismo não entra na hospedagem e não é descontada de novo.

Outubro, lido de `reservas_2026-10.csv`, tem de repetir o fechamento conhecido: 39 reservas, 134 diárias, ocupação 54,0%, receita líquida R$ 27.234,12 e comissão R$ 3.535,08. Se o arquivo está no lote e a conta diverge, a execução falha e não publica a planilha.

## Regras de validação

1. Campo obrigatório vazio (`booking_id`, `guest`, `channel`, `room`, `checkin`, `nights`, `guests`) torna a linha incompleta. Ela não entra nos totais e, se existir, vai para `incompletas.csv`. Motivo: preencher o vazio no chute inventaria receita. Incompleta não aparece como reserva válida.
2. Canal, quarto, hóspedes e noites têm de cair no domínio do theme2.py, e a estadia tem de terminar no mês do check-in. Motivo: fora disso não há tarifa nem comissão. Um valor inválido rejeita o lote inteiro, inclusive as linhas que estariam certas, para não entregar um fechamento parcial com cara de oficial.
3. `booking_id` repetido ou duas estadias no mesmo quarto com noites em comum rejeitam o lote inteiro. Motivo: a reserva seria contada duas vezes, ou a mesma diária seria vendida duas vezes.

Arquivo sem as colunas obrigatórias também rejeita o lote: não é uma linha incompleta, é outro leiaute.

## Indicadores

- Ocupação: diárias vendidas divididas por 8 quartos vezes os dias do mês.
- Receita líquida: soma do que sobra em cada reserva depois de comissão, café e limpeza.
- Comissão dos canais: soma da comissão sobre a hospedagem.
- Diárias vendidas: soma das noites.
- Percentual retido: receita líquida dividida pelo valor pago pelo hóspede.

O resumo da planilha, por mês e canal, é ordenado pela receita líquida, da maior para a menor.

## Feriados e pontes

A pergunta que o caderno interno não responde: a ocupação e a receita se concentram em feriados e pontes?

A fonte é a BrasilAPI, `GET https://brasilapi.com.br/api/feriados/v1/{year}`, sem chave. O `requests` envia o ano também em `params`, com timeout de 20 segundos. Timeout, falha de rede e HTTP com erro viram mensagem clara. A resposta bruta e o metadado (provedor, endpoint, parâmetros, data da coleta, unidades e termos de uso) ficam em `data/external`. O JSON vira um DataFrame com as colunas `date`, `name` e `type`.

Uma linha de reserva é uma hospedagem. Uma linha de feriado é uma data nacional. A reserva é expandida para uma linha por noite ocupada, com data ISO, e a junção é pela data. Várias noites podem cair no mesmo feriado; cada noite encontra no máximo um. Noite sem feriado continua no arquivo. Contagem de reservas, diárias, valor pago e receita líquida são conferidos antes e depois.

Ponte, neste trabalho: feriado na segunda inclui sábado e domingo; na sexta, inclui sábado e domingo; na terça, inclui a segunda; na quinta, inclui a sexta. Em 2026, 7 de setembro e 12 de outubro caem numa segunda.

Dado externo inválido (JSON que não é lista, campo faltando, data ilegível ou repetida, menos de 8 feriados ou ausência de um feriado nacional fixo) não substitui o cache. Se o cache antigo for válido, a execução segue com modo `cache` e o log explica a falha da consulta. Se não houver cache válido, o status fica `falha` e não saem CSV, planilha nem relatório. O pipeline não inventa feriado.

## Achado e limitação

O relatório de cada execução separa evidência e interpretação. A evidência são as fatias de dias, diárias e receita rateada. A interpretação usa um limiar explícito de 2 pontos percentuais acima do peso desses dias no calendário. A limitação também está no relatório: a API só tem feriado nacional, o rateio da receita é igual entre as noites, a estadia não cruza o mês, e setembro é fictício.

Na execução `20261123T151129`, outubro fechou com 39 reservas, 134 diárias, ocupação 54,0%, receita líquida R$ 27.234,12 e comissão R$ 3.535,08. No lote inteiro, feriados e pontes são 11,5% dos dias, 13,4% das diárias e 12,7% da receita líquida rateada. Pelo limiar de 2 pontos percentuais, isso não chega a ser concentração, embora a ocupação nesses dias (69,6%) fique acima da ocupação dos demais (58,6%). O texto com evidência e interpretação separadas está em `output/run_20261123T151129/report.md`.

Neste ambiente o interpretador se chama `python3`. O comando da disciplina é `python run_pipeline.py`; aqui ele foi executado como `python3 run_pipeline.py`.
