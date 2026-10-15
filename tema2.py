mes_referencia = "Outubro de 2026"
dias_no_mes = 31
capacidade_padrao_quarto = 2
maximo_hospedes_quarto = 4
custo_cafe_por_hospede_por_noite = 18.00
taxa_limpeza_por_reserva = 70.00
taxa_hospede_extra_por_noite = 60.00
taxa_turismo_por_hospede_por_noite = 4.00
percentual_sinal = 30.0

canais = ["Booking", "Airbnb", "Site proprio", "WhatsApp direto"]
canais_de_plataforma = ["Booking", "Airbnb"]

quartos = {
    1: {"tipo": "Standard", "diaria": 250.00},
    2: {"tipo": "Standard", "diaria": 250.00},
    3: {"tipo": "Standard", "diaria": 250.00},
    4: {"tipo": "Standard", "diaria": 250.00},
    5: {"tipo": "Superior", "diaria": 320.00},
    6: {"tipo": "Superior", "diaria": 320.00},
    7: {"tipo": "Superior", "diaria": 320.00},
    8: {"tipo": "Suite", "diaria": 420.00},
}

reservas_do_mes = [
    {"hospede": "Carolina Vieira", "canal": "Booking", "quarto": 6, "checkin": 1, "noites": 7, "hospedes": 1},
    {"hospede": "Thiago Martins", "canal": "WhatsApp direto", "quarto": 2, "checkin": 2, "noites": 7, "hospedes": 2},
    {"hospede": "Leticia Freitas", "canal": "Booking", "quarto": 4, "checkin": 2, "noites": 3, "hospedes": 3},
    {"hospede": "Eduardo Monteiro", "canal": "Airbnb", "quarto": 7, "checkin": 3, "noites": 2, "hospedes": 2},
    {"hospede": "Bruno Carvalho", "canal": "WhatsApp direto", "quarto": 3, "checkin": 4, "noites": 3, "hospedes": 2},
    {"hospede": "Camila Ferreira", "canal": "Booking", "quarto": 5, "checkin": 5, "noites": 1, "hospedes": 4},
    {"hospede": "Patricia Gomes", "canal": "Booking", "quarto": 7, "checkin": 7, "noites": 3, "hospedes": 1},
    {"hospede": "Gabriel Batista", "canal": "WhatsApp direto", "quarto": 3, "checkin": 8, "noites": 7, "hospedes": 1},
    {"hospede": "Larissa Mendes", "canal": "WhatsApp direto", "quarto": 8, "checkin": 8, "noites": 2, "hospedes": 1},
    {"hospede": "Marcelo Pinto", "canal": "WhatsApp direto", "quarto": 1, "checkin": 9, "noites": 7, "hospedes": 2},
    {"hospede": "Vanessa Moreira", "canal": "WhatsApp direto", "quarto": 4, "checkin": 9, "noites": 2, "hospedes": 3},
    {"hospede": "Beatriz Nunes", "canal": "Booking", "quarto": 5, "checkin": 9, "noites": 2, "hospedes": 2},
    {"hospede": "Mariana Alves", "canal": "Booking", "quarto": 2, "checkin": 10, "noites": 2, "hospedes": 2},
    {"hospede": "Elisa Siqueira", "canal": "Booking", "quarto": 6, "checkin": 10, "noites": 2, "hospedes": 2},
    {"hospede": "Diego Barbosa", "canal": "Airbnb", "quarto": 7, "checkin": 11, "noites": 5, "hospedes": 3},
    {"hospede": "Bianca Cunha", "canal": "Booking", "quarto": 8, "checkin": 11, "noites": 2, "hospedes": 2},
    {"hospede": "Natalia Farias", "canal": "Airbnb", "quarto": 6, "checkin": 15, "noites": 4, "hospedes": 1},
    {"hospede": "Vinicius Lopes", "canal": "Booking", "quarto": 2, "checkin": 16, "noites": 2, "hospedes": 1},
    {"hospede": "Renata Duarte", "canal": "Booking", "quarto": 3, "checkin": 16, "noites": 3, "hospedes": 2},
    {"hospede": "Rodrigo Teixeira", "canal": "Site proprio", "quarto": 4, "checkin": 16, "noites": 5, "hospedes": 4},
    {"hospede": "Fernanda Lima", "canal": "Airbnb", "quarto": 5, "checkin": 16, "noites": 1, "hospedes": 2},
    {"hospede": "Lucas Ribeiro", "canal": "Booking", "quarto": 8, "checkin": 16, "noites": 7, "hospedes": 3},
    {"hospede": "Henrique Dias", "canal": "Booking", "quarto": 5, "checkin": 18, "noites": 3, "hospedes": 2},
    {"hospede": "Daniela Fonseca", "canal": "Site proprio", "quarto": 7, "checkin": 18, "noites": 3, "hospedes": 1},
    {"hospede": "Sabrina Rezende", "canal": "Airbnb", "quarto": 1, "checkin": 20, "noites": 4, "hospedes": 2},
    {"hospede": "Mateus Pacheco", "canal": "Site proprio", "quarto": 2, "checkin": 23, "noites": 4, "hospedes": 2},
    {"hospede": "Aline Castro", "canal": "Airbnb", "quarto": 3, "checkin": 23, "noites": 3, "hospedes": 3},
    {"hospede": "Fabio Correia", "canal": "Site proprio", "quarto": 4, "checkin": 23, "noites": 1, "hospedes": 2},
    {"hospede": "Paulo Azevedo", "canal": "Booking", "quarto": 5, "checkin": 23, "noites": 5, "hospedes": 1},
    {"hospede": "Felipe Araujo", "canal": "Site proprio", "quarto": 6, "checkin": 23, "noites": 2, "hospedes": 1},
    {"hospede": "Priscila Campos", "canal": "WhatsApp direto", "quarto": 7, "checkin": 23, "noites": 3, "hospedes": 2},
    {"hospede": "Gustavo Pereira", "canal": "WhatsApp direto", "quarto": 8, "checkin": 23, "noites": 3, "hospedes": 1},
    {"hospede": "Ricardo Sales", "canal": "WhatsApp direto", "quarto": 4, "checkin": 24, "noites": 7, "hospedes": 2},
    {"hospede": "Tatiane Moura", "canal": "WhatsApp direto", "quarto": 1, "checkin": 25, "noites": 2, "hospedes": 1},
    {"hospede": "Andre Cardoso", "canal": "Booking", "quarto": 1, "checkin": 27, "noites": 3, "hospedes": 2},
    {"hospede": "Otavio Brandao", "canal": "Airbnb", "quarto": 3, "checkin": 28, "noites": 4, "hospedes": 2},
    {"hospede": "Leonardo Prado", "canal": "Booking", "quarto": 8, "checkin": 28, "noites": 3, "hospedes": 2},
    {"hospede": "Isabela Ramos", "canal": "Booking", "quarto": 7, "checkin": 29, "noites": 3, "hospedes": 2},
    {"hospede": "Juliana Rocha", "canal": "Airbnb", "quarto": 6, "checkin": 30, "noites": 2, "hospedes": 3},
]


def percentual_desconto(numero_noites):
    if numero_noites >= 7:
        return 15.0
    elif numero_noites >= 3:
        return 8.0
    else:
        return 0.0


def percentual_comissao(canal):
    if canal == "Booking":
        return 15.0
    elif canal == "Airbnb":
        return 14.0
    elif canal == "Site proprio":
        return 3.0
    else:
        return 0.0


def hospedes_extras(numero_hospedes):
    if numero_hospedes > capacidade_padrao_quarto:
        return numero_hospedes - capacidade_padrao_quarto
    else:
        return 0


def classificar_ocupacao(taxa_ocupacao):
    if taxa_ocupacao >= 80:
        return "Alta", "Demanda forte: nao conceda desconto e priorize reservas diretas."
    elif taxa_ocupacao >= 50:
        return "Media", "Demanda regular: ofereca incentivo para o hospede reservar direto."
    else:
        return "Baixa", "Demanda fraca: a visibilidade das plataformas compensa a comissao."


def calcular_reserva(reserva):
    diaria = quartos[reserva["quarto"]]["diaria"]
    noites = reserva["noites"]
    hospedes = reserva["hospedes"]

    valor_tabela = diaria * noites
    valor_hospede_extra = taxa_hospede_extra_por_noite * hospedes_extras(hospedes) * noites
    valor_desconto = (valor_tabela + valor_hospede_extra) * percentual_desconto(noites) / 100
    valor_hospedagem = valor_tabela + valor_hospede_extra - valor_desconto
    valor_taxa_turismo = taxa_turismo_por_hospede_por_noite * hospedes * noites
    valor_pago = valor_hospedagem + valor_taxa_turismo

    valor_comissao = valor_hospedagem * percentual_comissao(reserva["canal"]) / 100
    custo_cafe = custo_cafe_por_hospede_por_noite * hospedes * noites
    receita_liquida = valor_hospedagem - valor_comissao - custo_cafe - taxa_limpeza_por_reserva

    return {
        "valor_tabela": valor_tabela,
        "valor_hospede_extra": valor_hospede_extra,
        "valor_desconto": valor_desconto,
        "valor_hospedagem": valor_hospedagem,
        "valor_taxa_turismo": valor_taxa_turismo,
        "valor_pago": valor_pago,
        "valor_sinal": valor_pago * percentual_sinal / 100,
        "valor_comissao": valor_comissao,
        "custo_cafe": custo_cafe,
        "receita_liquida": receita_liquida,
    }


def quarto_disponivel(reservas, quarto, checkin, noites):
    checkout = checkin + noites
    for reserva in reservas:
        if reserva["quarto"] == quarto:
            checkout_existente = reserva["checkin"] + reserva["noites"]
            if checkin < checkout_existente and reserva["checkin"] < checkout:
                return False
    return True


def ler_texto(mensagem):
    texto = input(mensagem).strip()
    while texto == "":
        print("Este campo nao pode ficar vazio.")
        texto = input(mensagem).strip()
    return texto


def ler_inteiro(mensagem, minimo, maximo):
    texto = input(mensagem).strip()
    while not texto.isdigit() or int(texto) < minimo or int(texto) > maximo:
        print(f"Digite um numero inteiro entre {minimo} e {maximo}.")
        texto = input(mensagem).strip()
    return int(texto)


def escolher_canal():
    for posicao in range(len(canais)):
        print(f"  {posicao + 1}. {canais[posicao]}")
    escolha = ler_inteiro("Canal: ", 1, len(canais))
    return canais[escolha - 1]


def escolher_quarto():
    for numero in quartos:
        print(f"  {numero}. {quartos[numero]['tipo']:<9} R$ {quartos[numero]['diaria']:.2f} por noite")
    return ler_inteiro(f"Quarto (1 a {len(quartos)}): ", 1, len(quartos))


def mostrar_cotacao(reserva, valores):
    print("\n--- COTACAO ---")
    print(f"Hospede: {reserva['hospede']} | Canal: {reserva['canal']}")
    print(f"Quarto {reserva['quarto']} ({quartos[reserva['quarto']]['tipo']}), "
          f"check-in dia {reserva['checkin']}, {reserva['noites']} noite(s), {reserva['hospedes']} hospede(s)")
    print(f"Diarias: R$ {valores['valor_tabela']:.2f}")
    print(f"Hospede extra: R$ {valores['valor_hospede_extra']:.2f}")
    print(f"Desconto por duracao ({percentual_desconto(reserva['noites']):.1f}%): - R$ {valores['valor_desconto']:.2f}")
    print(f"Taxa de turismo (repassada a prefeitura): R$ {valores['valor_taxa_turismo']:.2f}")
    print(f"Valor pago pelo hospede: R$ {valores['valor_pago']:.2f}")
    print(f"Sinal para confirmar ({percentual_sinal:.0f}%): R$ {valores['valor_sinal']:.2f}")
    print(f"Comissao do canal ({percentual_comissao(reserva['canal']):.1f}%): R$ {valores['valor_comissao']:.2f}")
    print(f"Cafe da manha: R$ {valores['custo_cafe']:.2f} | Limpeza: R$ {taxa_limpeza_por_reserva:.2f}")
    print(f"Receita liquida da pousada: R$ {valores['receita_liquida']:.2f}")


def registrar_reserva(reservas):
    print("\n--- NOVA RESERVA ---")
    hospede = ler_texto("Nome do hospede: ")
    canal = escolher_canal()
    quarto = escolher_quarto()
    checkin = ler_inteiro(f"Dia do check-in (1 a {dias_no_mes}): ", 1, dias_no_mes)
    maximo_noites = dias_no_mes + 1 - checkin
    noites = ler_inteiro(f"Numero de noites (1 a {maximo_noites}): ", 1, maximo_noites)

    if not quarto_disponivel(reservas, quarto, checkin, noites):
        print(f"\nO quarto {quarto} ja esta ocupado em parte desse periodo. Reserva nao registrada.")
        return

    hospedes = ler_inteiro(f"Numero de hospedes (1 a {maximo_hospedes_quarto}): ", 1, maximo_hospedes_quarto)
    reserva = {"hospede": hospede, "canal": canal, "quarto": quarto,
               "checkin": checkin, "noites": noites, "hospedes": hospedes}
    mostrar_cotacao(reserva, calcular_reserva(reserva))

    confirmacao = input("\nConfirmar reserva? (s/n): ").strip().lower()
    if confirmacao == "s":
        reservas.append(reserva)
        print("Reserva registrada.")
    else:
        print("Reserva descartada.")


def mostrar_reservas(reservas):
    print(f"\n--- RESERVAS DE {mes_referencia.upper()} ---")
    print(f"{'Dia':>3} {'Qto':>3}  {'Hospede':<18}{'Canal':<17}{'Noites':>6}{'Pago':>11}{'Liquido':>11}")
    for dia in range(1, dias_no_mes + 1):
        for reserva in reservas:
            if reserva["checkin"] == dia:
                valores = calcular_reserva(reserva)
                print(f"{reserva['checkin']:>3} {reserva['quarto']:>3}  {reserva['hospede']:<18}"
                      f"{reserva['canal']:<17}{reserva['noites']:>6}"
                      f"{valores['valor_pago']:>11.2f}{valores['receita_liquida']:>11.2f}")
    print(f"Total: {len(reservas)} reservas")


def fechar_mes(reservas):
    totais = {}
    for canal in canais:
        totais[canal] = {"reservas": 0, "noites": 0, "pago": 0.0, "comissao": 0.0, "liquido": 0.0}

    total_taxa_turismo = 0.0
    for reserva in reservas:
        valores = calcular_reserva(reserva)
        total_canal = totais[reserva["canal"]]
        total_canal["reservas"] = total_canal["reservas"] + 1
        total_canal["noites"] = total_canal["noites"] + reserva["noites"]
        total_canal["pago"] = total_canal["pago"] + valores["valor_pago"]
        total_canal["comissao"] = total_canal["comissao"] + valores["valor_comissao"]
        total_canal["liquido"] = total_canal["liquido"] + valores["receita_liquida"]
        total_taxa_turismo = total_taxa_turismo + valores["valor_taxa_turismo"]

    print(f"\n--- FECHAMENTO DE {mes_referencia.upper()} ---")
    print(f"{'Canal':<17}{'Reservas':>9}{'Noites':>8}{'Pago':>12}{'Comissao':>11}{'Liquido':>12}{'% retido':>10}")

    noites_vendidas = 0
    pago_mes = 0.0
    comissao_mes = 0.0
    liquido_mes = 0.0
    melhor_canal = ""
    melhor_percentual_retido = 0.0

    for canal in canais:
        total_canal = totais[canal]
        percentual_retido = 0.0
        if total_canal["pago"] > 0:
            percentual_retido = total_canal["liquido"] / total_canal["pago"] * 100
        if percentual_retido > melhor_percentual_retido:
            melhor_percentual_retido = percentual_retido
            melhor_canal = canal
        print(f"{canal:<17}{total_canal['reservas']:>9}{total_canal['noites']:>8}{total_canal['pago']:>12.2f}"
              f"{total_canal['comissao']:>11.2f}{total_canal['liquido']:>12.2f}{percentual_retido:>9.1f}%")
        noites_vendidas = noites_vendidas + total_canal["noites"]
        pago_mes = pago_mes + total_canal["pago"]
        comissao_mes = comissao_mes + total_canal["comissao"]
        liquido_mes = liquido_mes + total_canal["liquido"]

    percentual_retido_mes = 0.0
    if pago_mes > 0:
        percentual_retido_mes = liquido_mes / pago_mes * 100
    print(f"{'TOTAL':<17}{len(reservas):>9}{noites_vendidas:>8}{pago_mes:>12.2f}{comissao_mes:>11.2f}"
          f"{liquido_mes:>12.2f}{percentual_retido_mes:>9.1f}%")

    noites_disponiveis = len(quartos) * dias_no_mes
    taxa_ocupacao = noites_vendidas / noites_disponiveis * 100
    nivel, recomendacao = classificar_ocupacao(taxa_ocupacao)

    print(f"\nOcupacao: {taxa_ocupacao:.1f}% ({noites_vendidas} de {noites_disponiveis} quarto-noites), nivel {nivel}")
    print(f"Recomendacao: {recomendacao}")
    print(f"Comissao paga as plataformas no mes: R$ {comissao_mes:.2f}")
    print(f"Taxa de turismo recolhida e repassada a prefeitura: R$ {total_taxa_turismo:.2f}")
    print(f"Canal que retem a maior parte do valor pago: {melhor_canal} ({melhor_percentual_retido:.1f}%)")


def simular_canal_direto(reservas):
    print("\n--- SIMULACAO: E SE VIESSE DIRETO? ---")
    print("Cada reserva de Booking e Airbnb passa a ser feita por WhatsApp, sem comissao,")
    print("e o hospede recebe um desconto de incentivo para aceitar a troca.")
    incentivo = ler_inteiro("Desconto de incentivo (0 a 30%): ", 0, 30)

    liquido_atual = 0.0
    liquido_simulado = 0.0
    reservas_migradas = 0
    for reserva in reservas:
        valores = calcular_reserva(reserva)
        liquido_atual = liquido_atual + valores["receita_liquida"]
        if reserva["canal"] in canais_de_plataforma:
            hospedagem_com_incentivo = valores["valor_hospedagem"] * (100 - incentivo) / 100
            liquido_direto = hospedagem_com_incentivo - valores["custo_cafe"] - taxa_limpeza_por_reserva
            liquido_simulado = liquido_simulado + liquido_direto
            reservas_migradas = reservas_migradas + 1
        else:
            liquido_simulado = liquido_simulado + valores["receita_liquida"]

    diferenca = liquido_simulado - liquido_atual
    print(f"\nReservas migradas para o canal direto: {reservas_migradas}")
    print(f"Receita liquida real do mes: R$ {liquido_atual:.2f}")
    print(f"Receita liquida simulada: R$ {liquido_simulado:.2f}")
    print(f"Diferenca: R$ {diferenca:.2f}")

    if reservas_migradas == 0:
        print("Conclusao: nao ha reservas de plataforma neste mes, nada muda.")
    elif diferenca > 0:
        print("Conclusao: compensa. O incentivo custa menos que a comissao economizada.")
    else:
        print("Conclusao: nao compensa. O incentivo custa mais que a comissao economizada.")

    for canal in canais_de_plataforma:
        print(f"No {canal}, qualquer incentivo abaixo de {percentual_comissao(canal):.0f}% ainda deixa mais dinheiro na pousada.")


def mostrar_menu():
    print("\n=== POUSADA: CADERNO DE RESERVAS ===")
    print(f"Mes: {mes_referencia} | {len(quartos)} quartos")
    print("1. Registrar reserva")
    print("2. Ver reservas do mes")
    print("3. Fechamento do mes por canal")
    print("4. Simular: e se viesse direto?")
    print("0. Sair")


def executar_caderno():
    opcao = ""
    while opcao != "0":
        mostrar_menu()
        opcao = input("Escolha uma opcao: ").strip()
        if opcao == "1":
            registrar_reserva(reservas_do_mes)
        elif opcao == "2":
            mostrar_reservas(reservas_do_mes)
        elif opcao == "3":
            fechar_mes(reservas_do_mes)
        elif opcao == "4":
            simular_canal_direto(reservas_do_mes)
        elif opcao == "0":
            print("Ate logo.")
        else:
            print("Opcao invalida. Escolha um numero do menu.")


if __name__ == "__main__":
    executar_caderno()
