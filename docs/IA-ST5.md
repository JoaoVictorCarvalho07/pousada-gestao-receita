# Interação com a ferramenta — ST5

## Ferramenta

- Ferramenta: Cursor
- Modelo: Grok 4.7
- Data: 23/11/2026
- Prompt: o mesmo enunciado da tarefa LO2, na parte de feriados e integração

Trecho usado:

> 5.1 API: business question [...] 'Do occupancy and revenue concentrate on holidays and long weekends (pontes)?'. Use BrasilAPI holidays `GET https://brasilapi.com.br/api/feriados/v1/{year}` (no key) via requests with params, timeout and HTTP error handling; save raw response + metadata [...] Offline fallback: use last saved response and log source mode (live/cache).
>
> 5.2 Integration: define what a row is in each source [...]; expand bookings to occupied nights with ISO dates; normalized join key (date); check uniqueness, cardinality, no-match; counts and totals preserved before/after join; traceability (source_file, run id).
>
> 5.3 Workflow: acquisition, validation, integration, storage in named functions in .py; one documented command runnable in VS Code (`python run_pipeline.py`, plus .vscode/launch.json); extends ST4 with integrated CSV, updated workbook (extra sheet e.g. Feriados) [...]

## Resposta que virou código

A pergunta de negócio ficou no relatório: a ocupação e a receita se concentram em feriados e pontes? `pipeline/api.py` consulta a BrasilAPI, grava o JSON bruto e o metadado em `data/external` e, se a consulta falha ou o processo pede `--offline`, relê o último arquivo válido. `pipeline/integrate.py` expande cada reserva em noites e junta pela data ISO. As funções nomeadas são `acquire_bookings`, `validate_batch`, `acquire_holidays`, `integrate_bookings` e `store_results`.

## Sugestões: o que entrou e o que ficou de fora

### 1. `requests` com `params`, timeout e erro de HTTP

Sugestão considerada: chamar a URL só com o ano no caminho, sem o argumento `params`, porque a documentação da rota não tem query string.

Decisão: o ano continua no caminho e também vai em `params={"year": year}`, com timeout de 20 segundos. `raise_for_status` transforma HTTP de erro em `ExternalDataError`. Timeout e falha de conexão também.

Teste de sonda, antes de fechar o código: `urllib` sem o cliente do `requests` recebeu HTTP 403. Em seguida, `requests` na URL limpa e na URL com `?year=2026` recebeu 200 e o mesmo corpo, 14 feriados, entre eles Independência em 2026-09-07 (segunda) e Nossa Senhora Aparecida em 2026-10-12 (segunda).

Testes no pytest: `test_consulta_envia_params_e_timeout` confere `params == {"year": 2026}` e `timeout == 20`. `test_http_500_vira_erro_claro` confere a mensagem `HTTP 500`. A execução `20261123T151129` registrou `source_mode=live http=200 registros=14`.

Resultado: a resposta bruta está em `data/external/feriados_2026.json` e o metadado (provedor, endpoint, parâmetros, data da coleta, unidades, termos) em `feriados_2026.meta.json`.

Limitação: o parâmetro de consulta é redundante. A BrasilAPI devolveu o mesmo JSON com e sem ele. O metadado diz isso em `params_note`. O 403 do `urllib` não foi investigado além de trocar para `requests`, que é a biblioteca pedida.

### 2. Resposta inválida não apaga o cache; modo offline não chama a rede

Sugestão considerada: gravar qualquer corpo HTTP 200 e só depois tentar interpretar. Outra variante: se o JSON viesse ruim, inventar a lista dos feriados fixos para a junção não parar.

Decisão: as duas foram rejeitadas. O arquivo em `data/external` só é substituído depois que a lista passa na checagem (objeto com `date`, `name` e `type`, data no ano pedido, sem data repetida, pelo menos 8 feriados e os feriados nacionais fixos). JSON inválido cai no cache anterior, se ele ainda for válido. Sem cache válido, a execução para e não grava planilha. `--offline` lê o arquivo e não abre conexão.

Testes: `test_json_de_feriado_invalido_e_recusado`, `test_resposta_invalida_nao_apaga_o_cache` (o arquivo no disco continua igual ao texto original e `source_mode` volta `cache`) e `test_offline_nao_chama_a_rede` (o `requests.get` falso lançaria erro se fosse chamado).

Execução real, em sequência:

```text
Execução 20261123T151129 concluída.
Status: sucesso
Modo da fonte externa: live

Execução 20261123T151130 concluída.
Status: sucesso
Modo da fonte externa: cache
```

O log do cache diz `motivo=offline arquivo=feriados_2026.json` e não tem linha `http=200`. As duas pastas `output/run_20261123T151129` e `output/run_20261123T151130` continuam no disco.

Resultado: o modo da fonte fica no log, no relatório e em `output/latest_status.json` (a última execução gravada é a `20261123T151130`, status sucesso, `source_mode` cache).

Limitação: o fallback automático quando a rede cai usa o mesmo caminho do `--offline`, mas eu não desliguei a rede de propósito para ver esse ramo ao vivo. O ramo está coberto pelo teste que devolve um JSON inválido com cache já presente.

### 3. Ratear a receita pela noite, em vez de jogá-la no check-in

Sugestão considerada: marcar a receita inteira da reserva no dia do check-in, que é mais simples e não exige rateio.

Decisão: rejeitada. A pergunta é sobre noites ocupadas. Uma estadia de 7 noites colocaria 100% da receita no dia da entrada, mesmo que o feriado fosse outra noite. A receita líquida é dividida entre as noites, e a última noite absorve o resto da divisão para a soma fechar.

Teste: `test_integracao_preserva_totais_e_rastreio`. O log da execução ao vivo registra `reservas=86/86 diarias=292/292 liquida_antes=59395.10 liquida_depois=59395.10 cardinalidade=many_to_one sem_feriado=282 com_feriado=10`. Cada linha integrada tem `source_file` e `run_id`.

Resultado: a junção é many-to-one pela data. Noite sem feriado permanece no CSV, com o nome do feriado vazio. Isso é ausência de correspondência esperada, não erro. Doze feriados do ano não têm nenhuma diária neste lote.

Limitação: o rateio é igual entre as noites. O `theme2.py` não tem tarifa de fim de semana, então o rateio não mede disposição a pagar diferente. Café, limpeza e comissão também se espalham pelas noites.

### 4. A ponte de Finados puxa 31/10

Sugestão que eu cheguei a considerar enquanto lia o resultado: contar em outubro só 10, 11 e 12/10, para a ponte "óbvia" de Nossa Senhora Aparecida, e ignorar 31/10.

Decisão: rejeitada. A regra já estava declarada para qualquer feriado numa segunda: sábado, domingo e segunda. Finados em 2026 cai numa segunda (02/11). O sábado anterior é 31/10 e ainda pertence a outubro. Apagar essa data só para a conta ficar com três dias mudaria a regra no meio do caminho.

Teste da regra geral: `test_ponte_de_feriado_na_segunda` espera 05, 06 e 07/09 para o feriado de 07/09. Não escrevi um teste com o nome "Finados". A consequência em outubro está na evidência do relatório da execução `20261123T151129`: as datas de outubro são 10/10, 11/10, 12/10 e 31/10, quatro de 31 dias (12,9%).

Resultado: o lote tem 7 dias especiais em 61 (11,5%), 39 diárias em 292 (13,4%) e 12,7% da receita líquida rateada. Pelo critério de 2 pontos percentuais acima do calendário, a resposta do lote é não. A ocupação nesses dias foi 69,6%, contra 58,6% nos demais. Setembro, fictício, fica +2,7 pontos nas diárias. Outubro, o mês do `theme2.py`, fica +1,3 nas diárias e +0,9 na receita.

Limitação: o "não" depende do limiar de 2 pontos, que eu escolhi e o relatório declara. A taxa de ocupação é mais alta nesses dias. Outro leitor pode chamar isso de concentração leve. Setembro não é um extrato real. A BrasilAPI não traz feriado municipal.

## Resultado do ST5

A execução ao vivo e a execução offline respondem a mesma pergunta com os mesmos totais de outubro. A planilha ganha a aba Feriados. O comando único está em `run_pipeline.py` e em `.vscode/launch.json` (`Pipeline LO2` e `Pipeline LO2 (offline)`).
