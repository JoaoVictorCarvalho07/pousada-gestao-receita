custo_cafe_por_hospede_por_noite = 18.00
taxa_limpeza_por_reserva = 70.00

nome_hospede = input("Nome do hospede: ")
canal_reserva = input("Canal da reserva (Booking, Airbnb, Site proprio, WhatsApp direto): ")
valor_diaria = float(input("Valor da diaria (R$): "))
numero_noites = int(input("Numero de noites: "))
numero_hospedes = int(input("Numero de hospedes: "))

valor_bruto = valor_diaria * numero_noites

if numero_noites >= 7:
    percentual_desconto = 15.0
    faixa_estadia = "Estadia longa"
elif numero_noites >= 3:
    percentual_desconto = 8.0
    faixa_estadia = "Estadia media"
else:
    percentual_desconto = 0.0
    faixa_estadia = "Estadia curta"

valor_desconto = valor_bruto * percentual_desconto / 100
valor_ao_hospede = valor_bruto - valor_desconto

canal_normalizado = canal_reserva.strip().lower()

if canal_normalizado == "booking":
    percentual_comissao = 15.0
elif canal_normalizado == "airbnb":
    percentual_comissao = 14.0
elif canal_normalizado == "site proprio":
    percentual_comissao = 3.0
else:
    percentual_comissao = 0.0

valor_comissao = valor_ao_hospede * percentual_comissao / 100
custo_cafe = custo_cafe_por_hospede_por_noite * numero_hospedes * numero_noites
custo_total = valor_comissao + custo_cafe + taxa_limpeza_por_reserva
receita_liquida = valor_ao_hospede - custo_total
receita_liquida_por_noite = receita_liquida / numero_noites
percentual_retido = receita_liquida / valor_ao_hospede * 100

print("\n--- RESUMO DA RESERVA ---")
print(f"Hospede: {nome_hospede}")
print(f"Canal: {canal_reserva}")
print(f"Estadia: {numero_noites} noite(s) para {numero_hospedes} hospede(s)")
print(f"Classificacao da estadia: {faixa_estadia}")
print(f"Valor de tabela: R$ {valor_bruto:.2f}")
print(f"Desconto por duracao ({percentual_desconto:.1f}%): R$ {valor_desconto:.2f}")
print(f"Valor pago pelo hospede: R$ {valor_ao_hospede:.2f}")
print(f"Comissao do canal ({percentual_comissao:.1f}%): R$ {valor_comissao:.2f}")
print(f"Cafe da manha: R$ {custo_cafe:.2f}")
print(f"Limpeza: R$ {taxa_limpeza_por_reserva:.2f}")
print(f"Custo total da reserva: R$ {custo_total:.2f}")
print(f"Receita liquida da pousada: R$ {receita_liquida:.2f}")
print(f"Receita liquida por noite: R$ {receita_liquida_por_noite:.2f}")
print(f"Percentual retido pela pousada: {percentual_retido:.1f}%")
