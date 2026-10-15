custo_cafe_por_hospede_por_noite = 18.00
taxa_limpeza_por_reserva = 70.00
taxa_hospede_extra_por_noite = 60.00
taxa_turismo_por_hospede_por_noite = 4.00
percentual_sinal = 30.0

nome_hospede = input("Nome do hospede: ")
canal_reserva = input("Canal da reserva (Booking, Airbnb, Site proprio, WhatsApp direto): ")
percentual_comissao = float(input("Percentual de comissao do canal (%): "))
valor_diaria = float(input("Valor da diaria do quarto (R$): "))
numero_noites = int(input("Numero de noites: "))
hospedes_incluidos = int(input("Hospedes incluidos na diaria (ate 2): "))
hospedes_extras = int(input("Hospedes extras (acima de 2): "))

numero_hospedes = hospedes_incluidos + hospedes_extras
hospede_noites = numero_hospedes * numero_noites

valor_diarias = valor_diaria * numero_noites
valor_hospede_extra = taxa_hospede_extra_por_noite * hospedes_extras * numero_noites
valor_hospedagem = valor_diarias + valor_hospede_extra
valor_taxa_turismo = taxa_turismo_por_hospede_por_noite * hospede_noites
valor_pago = valor_hospedagem + valor_taxa_turismo
valor_sinal = valor_pago * percentual_sinal / 100
valor_restante_no_checkin = valor_pago - valor_sinal

valor_comissao = valor_hospedagem * percentual_comissao / 100
custo_cafe = custo_cafe_por_hospede_por_noite * hospede_noites
custo_total = valor_comissao + custo_cafe + taxa_limpeza_por_reserva
receita_liquida = valor_hospedagem - custo_total

receita_liquida_por_noite = receita_liquida / numero_noites
receita_liquida_por_hospede = receita_liquida / numero_hospedes
percentual_retido = receita_liquida / valor_pago * 100

print("\n--- COTACAO DA RESERVA ---")
print(f"Hospede: {nome_hospede}")
print(f"Canal: {canal_reserva}")
print(f"Estadia: {numero_noites} noite(s) para {numero_hospedes} hospede(s), sendo {hospedes_extras} extra(s)")

print("\nO QUE O HOSPEDE PAGA")
print(f"Diarias: R$ {valor_diarias:.2f}")
print(f"Hospede extra: R$ {valor_hospede_extra:.2f}")
print(f"Taxa de turismo: R$ {valor_taxa_turismo:.2f}")
print(f"Total: R$ {valor_pago:.2f}")
print(f"Sinal para confirmar ({percentual_sinal:.0f}%): R$ {valor_sinal:.2f}")
print(f"Restante no check-in: R$ {valor_restante_no_checkin:.2f}")

print("\nO QUE SAI DO CAIXA DA POUSADA")
print(f"Comissao do canal ({percentual_comissao:.1f}%): R$ {valor_comissao:.2f}")
print(f"Cafe da manha: R$ {custo_cafe:.2f}")
print(f"Limpeza: R$ {taxa_limpeza_por_reserva:.2f}")
print(f"Taxa de turismo repassada a prefeitura: R$ {valor_taxa_turismo:.2f}")

print("\nO QUE SOBRA")
print(f"Receita liquida da pousada: R$ {receita_liquida:.2f}")
print(f"Por noite: R$ {receita_liquida_por_noite:.2f}")
print(f"Por hospede: R$ {receita_liquida_por_hospede:.2f}")
print(f"Percentual retido do valor pago: {percentual_retido:.1f}%")
