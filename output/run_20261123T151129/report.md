# Relatório de fechamento da pousada

## Execução

- Id da execução: 20261123T151129
- Início: 2026-11-23T15:11:29-03:00
- Comando: `python run_pipeline.py`
- Situação: sucesso
- Modo da fonte externa: live
- Pasta: output/run_20261123T151129
- Log: logs/run_20261123T151129.log

## Escopo

Tarefa recorrente: fechar a receita da pousada de 8 quartos a partir dos CSV de reservas exportados pela recepção. O usuário é quem opera a pousada e precisa de ocupação, comissão e receita líquida sem redigitar o mês. Entrada: um CSV por período, com o mesmo leiaute. Saída desta execução: CSV processado por arquivo, CSV de noites integradas aos feriados, planilha e este relatório.

Arquivos lidos: reservas_2026-09.csv, reservas_2026-10.csv.
Meses presentes: 2026-09, 2026-10.
Os originais em data/raw não são alterados. Cada linha processada guarda o nome do arquivo de origem e o id desta execução.

## Validação

Três regras, com o motivo de cada uma:

1. Campo obrigatório vazio torna a linha incompleta. Ela sai do fechamento e, quando existe, vai para `incompletas.csv`. Motivo: completar hóspede, data ou noites no chute inventaria receita. Linha incompleta não é mostrada como reserva válida.
2. Canal, quarto, hóspedes e noites precisam cair no domínio do theme2.py: canais Booking, Airbnb, Own website e WhatsApp direct; quartos 1 a 8; 1 a 4 hóspedes; noites inteiras que terminam dentro do mês do check-in. Motivo: fora desse domínio não há tarifa nem comissão definidas. Um valor inválido rejeita o lote inteiro, para não publicar um fechamento parcial com cara de oficial.
3. `booking_id` não pode repetir e o mesmo quarto não pode ter duas estadias sobrepostas. Motivo: identificador repetido contaria a reserva duas vezes; sobreposição contaria a diária duas vezes e poderia levar a ocupação acima de 100% sem o quarto existir em dobro.

Nesta execução, linhas incompletas separadas: 0. Reservas válidas: 86.

## Indicadores

Os cinco indicadores abaixo saem das reservas válidas. Ocupação é diárias vendidas divididas por 8 quartos vezes os dias do mês. Comissão é a soma da comissão sobre a hospedagem, sem a taxa de turismo. Receita líquida é hospedagem menos comissão, café da manhã e limpeza. Percentual retido é a receita líquida dividida pelo valor pago pelo hóspede. Diárias vendidas são a soma das noites.

| Indicador | 2026-09 | 2026-10 | Lote |
| --- | --- | --- | --- |
| Reservas | 47 | 39 | 86 |
| Diárias vendidas | 158 | 134 | 292 |
| Diárias disponíveis | 240 | 248 | 488 |
| Ocupação | 65,8% | 54,0% | 59,8% |
| Valor pago pelo hóspede | R$ 47.073,20 | R$ 39.263,20 | R$ 86.336,40 |
| Comissão dos canais | R$ 4.384,21 | R$ 3.535,08 | R$ 7.919,30 |
| Receita líquida | R$ 32.160,99 | R$ 27.234,12 | R$ 59.395,10 |
| Percentual retido | 68,3% | 69,4% | 68,8% |

## Conferência de outubro

O arquivo reservas_2026-10.csv foi conferido contra o fechamento conhecido do theme2.py.
- Reservas: 39 (esperado 39) — confere
- Diárias: 134 (esperado 134) — confere
- Ocupação: 54,0% (esperado 54,0%) — confere
- Receita líquida: R$ 27.234,12 (esperado R$ 27.234,12) — confere
- Comissão: R$ 3.535,08 (esperado R$ 3.535,08) — confere

## Achado

Pergunta: a ocupação e a receita se concentram em feriados nacionais e em pontes (fins de semana prolongados)?

Regra do calendário usada na evidência: feriado na segunda puxa sábado e domingo; feriado na sexta puxa sábado e domingo; feriado na terça inclui a segunda; feriado na quinta inclui a sexta. A receita de cada reserva é rateada em partes iguais entre as noites da estadia.

Evidência:

- Mês 2026-09: 3 de 30 dias do calendário são feriado ou ponte (10,0%). Datas: 05/09, 06/09, 07/09. Nesses dias caem 20 de 158 diárias vendidas (12,7%) e R$ 3.766,87 de R$ 32.160,99 da receita líquida rateada (11,7%). Ocupação nesses dias: 83,3%. Ocupação nos demais dias: 63,9%.
- Mês 2026-10: 4 de 31 dias do calendário são feriado ou ponte (12,9%). Datas: 10/10, 11/10, 12/10, 31/10. Nesses dias caem 19 de 134 diárias vendidas (14,2%) e R$ 3.770,32 de R$ 27.234,12 da receita líquida rateada (13,8%). Ocupação nesses dias: 59,4%. Ocupação nos demais dias: 53,2%.
- Mês lote: 7 de 61 dias do calendário são feriado ou ponte (11,5%). Datas: 05/09, 06/09, 07/09, 10/10, 11/10, 12/10, 31/10. Nesses dias caem 39 de 292 diárias vendidas (13,4%) e R$ 7.537,19 de R$ 59.395,10 da receita líquida rateada (12,7%). Ocupação nesses dias: 69,6%. Ocupação nos demais dias: 58,6%.

Interpretação: chamo de concentração quando a fatia das diárias e a fatia da receita rateada superam, cada uma, a fatia do calendário em pelo menos 2 pontos percentuais, e a ocupação desses dias também supera a dos demais. Por esse critério, a resposta para o lote é não. A fatia das diárias e a fatia da receita rateada ficam perto do peso desses dias no calendário, sem folga de 2 pontos percentuais. A ocupação nos dias especiais ficou 11,1 pontos percentuais acima da ocupação dos outros dias. A taxa pode subir sem que o volume se afaste do calendário, porque esses dias são poucos. 2026-09 fica +2,7 pontos percentuais nas diárias e +1,7 na receita rateada, em relação ao calendário do mês. 2026-10 fica +1,3 pontos percentuais nas diárias e +0,9 na receita rateada, em relação ao calendário do mês. Em outubro as datas especiais são 10, 11 e 12/10, a ponte de Nossa Senhora Aparecida (feriado numa segunda), e também 31/10: Finados em 2026 cai numa segunda, e a regra da ponte puxa o sábado anterior, que ainda é outubro. Setembro é um caderno fictício; outubro reproduz o theme2.py. Por isso a evidência está aberta por mês.

## Limitação

A evidência acima descreve este lote, não um efeito causal do feriado. A BrasilAPI traz só feriados nacionais: feriado estadual ou municipal da cidade da pousada entra como dia comum. O rateio igual da receita líquida reparte também café, limpeza e comissão entre as noites; o modelo de tarifa, herdado do theme2.py, não tem preço diferente no fim de semana. Estadia que cruzaria o mês é rejeitada, como o limite de noites do theme2.py. Setembro de 2026 foi escrito para o exercício e não é um extrato real; outubro é o caderno do theme2.py.

## Dados externos e junção

- Provedor: BrasilAPI
- Endpoint: https://brasilapi.com.br/api/feriados/v1/2026
- Parâmetros: year=2026
- Coleta registrada no arquivo: 2026-11-23T15:11:29-03:00
- Modo nesta execução: live
- Registros: 14
- Unidades: date: data civil no calendário gregoriano, formato ISO-8601 (YYYY-MM-DD); name: nome do feriado nacional em português; type: classificação da BrasilAPI; nesta rota o valor esperado é national
- Termos de uso: A BrasilAPI oferece feriados nacionais como dado público, sem chave de acesso. O uso neste trabalho é acadêmico. Não há garantia de disponibilidade: se a consulta falhar, fica valendo a última resposta bruta salva em data/external. A resposta bruta não é editada à mão. Termos e documentação: https://brasilapi.com.br/

O que cada linha significa: no CSV de reservas, uma linha é uma hospedagem; no JSON de feriados, uma linha é uma data nacional; no CSV integrado, uma linha é uma noite ocupada de uma reserva. A chave de junção é a data ISO (`night_date`). A relação é many-to-one: várias noites podem cair no mesmo feriado e cada noite encontra no máximo um feriado. Noite sem feriado permanece no arquivo, com o nome do feriado vazio. Isso é ausência esperada de correspondência, não erro.

Checagens desta execução:

- Datas de feriado únicas: sim.
- Cardinalidade declarada na junção: many_to_one.
- Chave (booking_id, night_date) única: sim.
- Reservas antes e depois: 86 e 86.
- Diárias antes e depois: 292 e 292.
- Receita líquida antes e depois: R$ 59.395,10 e R$ 59.395,10.
- Valor pago antes e depois: R$ 86.336,40 e R$ 86.336,40.
- Noites com feriado: 10. Noites sem feriado: 282.
- Feriados do ano sem nenhuma diária neste lote: 12.
- Noites em feriado ou ponte: 39.

Rastreio: as colunas `source_file` e `run_id` seguem da reserva para a noite integrada. O id desta execução é 20261123T151129.

## Mesma base nas três saídas

Reservas válidas no CSV processado e na aba Detalhe: 86. Noites no CSV integrado: 292. Receita líquida do detalhe: R$ 59.395,10. Receita líquida depois da expansão das noites: R$ 59.395,10.

Reação a dado externo inválido, se ocorresse: JSON fora da estrutura, data ilegível, data repetida ou cobertura abaixo do mínimo não substitui o arquivo em data/external. Havendo cache válido, o log marca source_mode=cache e o fechamento segue. Sem cache válido, a execução para com status falha e não grava CSV, planilha nem este relatório.
