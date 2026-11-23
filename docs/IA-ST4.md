# Interação com a ferramenta — ST4

## Ferramenta

- Ferramenta: Cursor
- Modelo: Grok 4.7
- Data: 23/11/2026
- Onde: esta conversa, com o enunciado da tarefa LO2 (ST4 e ST5) como prompt

Não há outra sessão. O que está abaixo é o que foi de fato considerado e testado enquanto o pipeline era escrito. Não inventei uma conversa anterior.

## Prompt

Trecho do enunciado usado para o ST4:

> Implement the university assessment 'AI-Assisted Python — Summative LO2' (ST4 + ST5) in this repo [...] theme2.py = monthly revenue close for an 8-room inn [...] Known October close: 39 bookings, 134 room-nights, occupancy 54.0%, net R$ 27.234,12, commission R$ 3.535,08. Keep theme1.py/theme2.py untouched.
>
> 4.1 Files & batch: recurring task/user/inputs/outputs described; >=2 compatible CSVs processed in one run; reuse cleaning/validation/business rules from earlier work (document adaptations from theme2.py) [...]
> 4.2 Spreadsheet: Excel generated automatically [...] >=2 sheets (Detalhe + Resumo de negócio); aggregation, summary sorted by a metric; readable headers, column widths, numeric/currency formats, frozen header, autofilter; values numeric (not strings); check totals against data
> 4.3 Report & robustness: text report [...] >=3 indicators; 1 finding + 1 limitation separating evidence from interpretation; [...] >=3 justified validation rules; clear error and invalid input rejects the WHOLE batch; log file [...]; incomplete rows separated; previous outputs preserved [...]; runs with 1 command; show last run and status.

## Resposta que virou código

O fechamento deixou de ser o menu interativo de `theme2.py` e passou a ser `python run_pipeline.py`, lendo `data/raw/reservas_2026-09.csv` e `data/raw/reservas_2026-10.csv` na mesma execução. A fórmula de diária, desconto, comissão, café, limpeza e taxa de turismo ficou em `pipeline/rules.py`. A planilha, o relatório e o log saem de um único DataFrame validado.

## Sugestões: o que entrou e o que ficou de fora

### 1. Fórmula do theme2, sem descontar a taxa de turismo outra vez

Sugestão considerada: tratar a taxa de turismo como custo e subtraí-la de novo da receita líquida.

Decisão: rejeitada. Em `theme2.py`, a taxa entra no valor pago pelo hóspede e é repasse para a prefeitura. A receita líquida sai da hospedagem, já sem comissão, café e limpeza. Descontar a taxa de novo mudaria o fechamento conhecido.

Teste rodado:

```text
round net 27234.12
round net menos taxa 26186.12
```

O mesmo critério está em `tests/test_pipeline.py`: `test_taxa_de_turismo_nao_e_descontada_de_novo_da_receita_liquida` e `test_outubro_bate_com_o_fechamento_conhecido_e_com_theme2`. O segundo compara cada reserva de outubro com `theme2.calculate_booking`.

Resultado: outubro fecha em 39 reservas, 134 diárias, ocupação 54,0%, receita líquida R$ 27.234,12 e comissão R$ 3.535,08.

Limitação: a conta continua em ponto flutuante, como no `theme2.py`. A apresentação arredonda para centavos. A soma arredondada bate com o fechamento conhecido; o valor interno de outubro antes do arredondamento é 27234,116.

### 2. Data ISO no CSV, em vez do dia 1–31

Sugestão considerada: manter o check-in como dia do mês, para ficar idêntico ao dicionário do `theme2.py`.

Decisão: rejeitada para o CSV. Com setembro e outubro no mesmo lote, o dia 7 deixaria de identificar a noite.

Teste rodado nesta sessão:

```text
chave dia {7: ['setembro', 'outubro']}
chave ISO {'2026-09-07': ['setembro'], '2026-10-07': ['outubro']}
```

Resultado: `checkin` no CSV é `AAAA-MM-DD`. A adaptação está no README, seção "Adaptações em relação ao theme2.py". A estadia ainda tem de caber no mês do check-in, como o limite de noites do `theme2.py`.

Limitação: uma hospedagem que cruzasse o mês é rejeitada. O modelo antigo também não fechava esse caso.

### 3. Linha incompleta separada; valor inválido rejeita o lote inteiro

Sugestão considerada: ou rejeitar a linha incompleta do mesmo jeito que a inválida, ou publicar as linhas boas e só avisar das ruins.

Decisão: as duas variantes foram rejeitadas. Campo vazio é dado que não existe e vai para a separação de incompletas. Canal, quarto, noites ou sobreposição errados rejeitam o lote todo, inclusive o arquivo que estaria certo. Não se grava planilha nesse caso.

Teste rodado:

```text
python3 run_pipeline.py --input-dir data/raw/invalid_example
```

Saída:

```text
Lote rejeitado. Nenhuma saída de fechamento foi gerada.
- Canal desconhecido em R-BAD-3: "Instagram". Canais aceitos: Booking, Airbnb, Own website, WhatsApp direct.
- Noites fora do intervalo em R-BAD-5: "0". Use um inteiro a partir de 1.
- Quarto 3 com estadias sobrepostas: R-BAD-1 (check-in 2026-09-02, 2 noites) e R-BAD-4 (check-in 2026-09-03, 2 noites).
Status: falha
Execução 20261123T151128
```

O log `logs/run_20261123T151128.log` registra `completas=6 incompletas=1` e `incompletas_ids=['R-BAD-2']` antes da falha. Não existe `output/run_20261123T151128/`. O pytest `test_lote_invalido_rejeita_o_lote_inteiro` repete essa recusa num diretório temporário e confere que nenhum xlsx foi criado.

Resultado: o lote inválido não produz fechamento. A linha sem hóspede é incompleta; as outras três falhas são de domínio ou de sobreposição.

Limitação: o exemplo inválido está numa subpasta de propósito. O comando padrão não o lê, porque a leitura não é recursiva.

### 4. Número na planilha, não texto com "R$"

Sugestão considerada: gravar a moeda já formatada como texto (`R$ 27.234,12`) para o leitor ver o padrão brasileiro.

Decisão: rejeitada. A rubrica pede valor numérico. A aparência fica no formato da célula.

Teste rodado: `python3 -m pytest` passou `test_pipeline_offline_grava_planilha_com_outubro`. O openpyxl leu a coluna "Receita líquida (R$)" como número, com formato `"R$" #,##0.00`, cabeçalho congelado em `A2` e autofilter. Uma diária sem centavos (512) volta como `int`, e o teste aceita `int` ou `float`. Conferi também a execução ao vivo: check-in com formato `yyyy-mm-dd`, cabeçalho em negrito branco sobre azul `1F4E79`.

Resultado: Detalhe, Resumo de negócio e Feriados saem com número, largura, filtro e cabeçalho congelado. O resumo por mês e canal está ordenado pela receita líquida, da maior para a menor.

Limitação: o valor guardado na aba Detalhe mantém o ponto flutuante da fórmula. O formato de moeda mostra centavos. A conferência oficial de outubro, na própria planilha, usa os totais já arredondados (27234,12 e 3535,08).

### 5. O id da execução não pode repetir no mesmo segundo

O que aconteceu: na primeira vez em que rodei o lote inválido e, no segundo seguinte, o lote normal, os dois receberam o id `20261123T151053`. O log abriu em modo append. O arquivo `logs/run_20261123T151053.log`, que depois apaguei ao regenerar as saídas limpas, começou com o comando do lote inválido e, mais abaixo, continuou com `comando=python run_pipeline.py` da execução que deu certo.

Decisão: rejeitei deixar o log assim. O id novo olha a pasta de saída e o arquivo de log. O log abre em modo exclusivo (`mode="x"`), então não acrescenta texto num arquivo que já existe.

Teste: a sequência limpa gerou três arquivos, cada um com um único `run_id`:

- `logs/run_20261123T151128.log` — falha
- `logs/run_20261123T151129.log` — ao vivo
- `logs/run_20261123T151130.log` — cache

Além disso, `test_id_da_execucao_nao_reaproveita_log_existente` marca como ocupado um id cujo log já existe. O pytest final foi `13 passed`.

Limitação: o teste automático cobre a função que detecta o id ocupado. A prova de que os três logs não se misturam é a leitura desses arquivos, não um teste que dispare duas execuções no mesmo segundo.

## Resultado do ST4 e limite do que a ferramenta fez

O lote padrão fecha outubro no número conhecido e recusa o exemplo inválido. A ferramenta escolheu o limiar de 2 pontos percentuais usado na interpretação do relatório. Esse limiar não está nos dados: é uma regra de leitura, e o relatório a declara antes de responder. Quem mudar o limiar pode descrever o mesmo quadro como concentração leve, porque a ocupação nos dias especiais (69,6%) fica acima da ocupação dos outros dias (58,6%).
