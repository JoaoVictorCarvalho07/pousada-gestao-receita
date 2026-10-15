custo_cafe_por_hospede_por_noite = 18.00
taxa_limpeza_por_reserva = 70.00

nome_hospede = input("Nome do hospede: ")
canal_reserva = input("Canal da reserva (Booking, Airbnb, Site proprio, WhatsApp direto): ")
valor_diaria = float(input("Valor da diaria (R$): "))
numero_noites = int(input("Numero de noites: "))
numero_hospedes = int(input("Numero de hospedes: "))
percentual_comissao = float(input("Percentual de comissao do canal (%): "))

valor_bruto = valor_diaria * numero_noites
valor_comissao = valor_bruto * percentual_comissao / 100
custo_cafe = custo_cafe_por_hospede_por_noite * numero_hospedes * numero_noites
custo_total = valor_comissao + custo_cafe + taxa_limpeza_por_reserva
receita_liquida = valor_bruto - custo_total
receita_liquida_por_noite = receita_liquida / numero_noites
percentual_retido = receita_liquida / valor_bruto * 100

print("\n--- RESUMO DA RESERVA ---")
print(f"Hospede: {nome_hospede}")
print(f"Canal: {canal_reserva}")
print(f"Estadia: {numero_noites} noite(s) para {numero_hospedes} hospede(s)")
print(f"Valor pago pelo hospede: R$ {valor_bruto:.2f}")
print(f"Comissao do canal ({percentual_comissao:.1f}%): R$ {valor_comissao:.2f}")
print(f"Cafe da manha: R$ {custo_cafe:.2f}")
print(f"Limpeza: R$ {taxa_limpeza_por_reserva:.2f}")
print(f"Custo total da reserva: R$ {custo_total:.2f}")
print(f"Receita liquida da pousada: R$ {receita_liquida:.2f}")
print(f"Receita liquida por noite: R$ {receita_liquida_por_noite:.2f}")
print(f"Percentual retido pela pousada: {percentual_retido:.1f}%")
