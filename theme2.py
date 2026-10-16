reference_month = "October 2026"
days_in_month = 31
standard_room_capacity = 2
max_guests_per_room = 4
breakfast_cost_per_guest_per_night = 18.00
cleaning_fee_per_booking = 70.00
extra_guest_fee_per_night = 60.00
tourism_tax_per_guest_per_night = 4.00
deposit_percentage = 30.0

channels = ["Booking", "Airbnb", "Own website", "WhatsApp direct"]
platform_channels = ["Booking", "Airbnb"]

rooms = {
    1: {"type": "Standard", "nightly_rate": 250.00},
    2: {"type": "Standard", "nightly_rate": 250.00},
    3: {"type": "Standard", "nightly_rate": 250.00},
    4: {"type": "Standard", "nightly_rate": 250.00},
    5: {"type": "Superior", "nightly_rate": 320.00},
    6: {"type": "Superior", "nightly_rate": 320.00},
    7: {"type": "Superior", "nightly_rate": 320.00},
    8: {"type": "Suite", "nightly_rate": 420.00},
}

monthly_bookings = [
    {"guest": "Carolina Vieira", "channel": "Booking", "room": 6, "checkin": 1, "nights": 7, "guests": 1},
    {"guest": "Thiago Martins", "channel": "WhatsApp direct", "room": 2, "checkin": 2, "nights": 7, "guests": 2},
    {"guest": "Leticia Freitas", "channel": "Booking", "room": 4, "checkin": 2, "nights": 3, "guests": 3},
    {"guest": "Eduardo Monteiro", "channel": "Airbnb", "room": 7, "checkin": 3, "nights": 2, "guests": 2},
    {"guest": "Bruno Carvalho", "channel": "WhatsApp direct", "room": 3, "checkin": 4, "nights": 3, "guests": 2},
    {"guest": "Camila Ferreira", "channel": "Booking", "room": 5, "checkin": 5, "nights": 1, "guests": 4},
    {"guest": "Patricia Gomes", "channel": "Booking", "room": 7, "checkin": 7, "nights": 3, "guests": 1},
    {"guest": "Gabriel Batista", "channel": "WhatsApp direct", "room": 3, "checkin": 8, "nights": 7, "guests": 1},
    {"guest": "Larissa Mendes", "channel": "WhatsApp direct", "room": 8, "checkin": 8, "nights": 2, "guests": 1},
    {"guest": "Marcelo Pinto", "channel": "WhatsApp direct", "room": 1, "checkin": 9, "nights": 7, "guests": 2},
    {"guest": "Vanessa Moreira", "channel": "WhatsApp direct", "room": 4, "checkin": 9, "nights": 2, "guests": 3},
    {"guest": "Beatriz Nunes", "channel": "Booking", "room": 5, "checkin": 9, "nights": 2, "guests": 2},
    {"guest": "Mariana Alves", "channel": "Booking", "room": 2, "checkin": 10, "nights": 2, "guests": 2},
    {"guest": "Elisa Siqueira", "channel": "Booking", "room": 6, "checkin": 10, "nights": 2, "guests": 2},
    {"guest": "Diego Barbosa", "channel": "Airbnb", "room": 7, "checkin": 11, "nights": 5, "guests": 3},
    {"guest": "Bianca Cunha", "channel": "Booking", "room": 8, "checkin": 11, "nights": 2, "guests": 2},
    {"guest": "Natalia Farias", "channel": "Airbnb", "room": 6, "checkin": 15, "nights": 4, "guests": 1},
    {"guest": "Vinicius Lopes", "channel": "Booking", "room": 2, "checkin": 16, "nights": 2, "guests": 1},
    {"guest": "Renata Duarte", "channel": "Booking", "room": 3, "checkin": 16, "nights": 3, "guests": 2},
    {"guest": "Rodrigo Teixeira", "channel": "Own website", "room": 4, "checkin": 16, "nights": 5, "guests": 4},
    {"guest": "Fernanda Lima", "channel": "Airbnb", "room": 5, "checkin": 16, "nights": 1, "guests": 2},
    {"guest": "Lucas Ribeiro", "channel": "Booking", "room": 8, "checkin": 16, "nights": 7, "guests": 3},
    {"guest": "Henrique Dias", "channel": "Booking", "room": 5, "checkin": 18, "nights": 3, "guests": 2},
    {"guest": "Daniela Fonseca", "channel": "Own website", "room": 7, "checkin": 18, "nights": 3, "guests": 1},
    {"guest": "Sabrina Rezende", "channel": "Airbnb", "room": 1, "checkin": 20, "nights": 4, "guests": 2},
    {"guest": "Mateus Pacheco", "channel": "Own website", "room": 2, "checkin": 23, "nights": 4, "guests": 2},
    {"guest": "Aline Castro", "channel": "Airbnb", "room": 3, "checkin": 23, "nights": 3, "guests": 3},
    {"guest": "Fabio Correia", "channel": "Own website", "room": 4, "checkin": 23, "nights": 1, "guests": 2},
    {"guest": "Paulo Azevedo", "channel": "Booking", "room": 5, "checkin": 23, "nights": 5, "guests": 1},
    {"guest": "Felipe Araujo", "channel": "Own website", "room": 6, "checkin": 23, "nights": 2, "guests": 1},
    {"guest": "Priscila Campos", "channel": "WhatsApp direct", "room": 7, "checkin": 23, "nights": 3, "guests": 2},
    {"guest": "Gustavo Pereira", "channel": "WhatsApp direct", "room": 8, "checkin": 23, "nights": 3, "guests": 1},
    {"guest": "Ricardo Sales", "channel": "WhatsApp direct", "room": 4, "checkin": 24, "nights": 7, "guests": 2},
    {"guest": "Tatiane Moura", "channel": "WhatsApp direct", "room": 1, "checkin": 25, "nights": 2, "guests": 1},
    {"guest": "Andre Cardoso", "channel": "Booking", "room": 1, "checkin": 27, "nights": 3, "guests": 2},
    {"guest": "Otavio Brandao", "channel": "Airbnb", "room": 3, "checkin": 28, "nights": 4, "guests": 2},
    {"guest": "Leonardo Prado", "channel": "Booking", "room": 8, "checkin": 28, "nights": 3, "guests": 2},
    {"guest": "Isabela Ramos", "channel": "Booking", "room": 7, "checkin": 29, "nights": 3, "guests": 2},
    {"guest": "Juliana Rocha", "channel": "Airbnb", "room": 6, "checkin": 30, "nights": 2, "guests": 3},
]


def discount_percentage(number_of_nights):
    if number_of_nights >= 7:
        return 15.0
    elif number_of_nights >= 3:
        return 8.0
    else:
        return 0.0


def commission_percentage(channel):
    if channel == "Booking":
        return 15.0
    elif channel == "Airbnb":
        return 14.0
    elif channel == "Own website":
        return 3.0
    else:
        return 0.0


def extra_guests(number_of_guests):
    if number_of_guests > standard_room_capacity:
        return number_of_guests - standard_room_capacity
    else:
        return 0


def classify_occupancy(occupancy_rate):
    if occupancy_rate >= 80:
        return "High", "Strong demand: do not offer discounts and prioritize direct bookings."
    elif occupancy_rate >= 50:
        return "Medium", "Regular demand: offer guests an incentive to book direct."
    else:
        return "Low", "Weak demand: platform visibility is worth the commission."


def calculate_booking(booking):
    nightly_rate = rooms[booking["room"]]["nightly_rate"]
    nights = booking["nights"]
    guests = booking["guests"]

    room_charges = nightly_rate * nights
    extra_guest_charge = extra_guest_fee_per_night * extra_guests(guests) * nights
    discount_amount = (room_charges + extra_guest_charge) * discount_percentage(nights) / 100
    accommodation_total = room_charges + extra_guest_charge - discount_amount
    tourism_tax_total = tourism_tax_per_guest_per_night * guests * nights
    amount_paid = accommodation_total + tourism_tax_total

    commission_amount = accommodation_total * commission_percentage(booking["channel"]) / 100
    breakfast_cost = breakfast_cost_per_guest_per_night * guests * nights
    net_revenue = accommodation_total - commission_amount - breakfast_cost - cleaning_fee_per_booking

    return {
        "room_charges": room_charges,
        "extra_guest_charge": extra_guest_charge,
        "discount_amount": discount_amount,
        "accommodation_total": accommodation_total,
        "tourism_tax_total": tourism_tax_total,
        "amount_paid": amount_paid,
        "deposit_amount": amount_paid * deposit_percentage / 100,
        "commission_amount": commission_amount,
        "breakfast_cost": breakfast_cost,
        "net_revenue": net_revenue,
    }


def room_is_available(bookings, room, checkin, nights):
    checkout = checkin + nights
    for booking in bookings:
        if booking["room"] == room:
            existing_checkout = booking["checkin"] + booking["nights"]
            if checkin < existing_checkout and booking["checkin"] < checkout:
                return False
    return True


def read_text(message):
    text = input(message).strip()
    while text == "":
        print("This field cannot be empty.")
        text = input(message).strip()
    return text


def read_integer(message, minimum, maximum):
    text = input(message).strip()
    while not text.isdigit() or int(text) < minimum or int(text) > maximum:
        print(f"Enter a whole number between {minimum} and {maximum}.")
        text = input(message).strip()
    return int(text)


def choose_channel():
    for position in range(len(channels)):
        print(f"  {position + 1}. {channels[position]}")
    choice = read_integer("Channel: ", 1, len(channels))
    return channels[choice - 1]


def choose_room():
    for number in rooms:
        print(f"  {number}. {rooms[number]['type']:<9} R$ {rooms[number]['nightly_rate']:.2f} per night")
    return read_integer(f"Room (1 to {len(rooms)}): ", 1, len(rooms))


def show_quote(booking, values):
    print("\n--- QUOTE ---")
    print(f"Guest: {booking['guest']} | Channel: {booking['channel']}")
    print(f"Room {booking['room']} ({rooms[booking['room']]['type']}), "
          f"check-in day {booking['checkin']}, {booking['nights']} night(s), {booking['guests']} guest(s)")
    print(f"Room charges: R$ {values['room_charges']:.2f}")
    print(f"Extra guest: R$ {values['extra_guest_charge']:.2f}")
    print(f"Length-of-stay discount ({discount_percentage(booking['nights']):.1f}%): - R$ {values['discount_amount']:.2f}")
    print(f"Tourism tax (passed on to the city hall): R$ {values['tourism_tax_total']:.2f}")
    print(f"Amount paid by the guest: R$ {values['amount_paid']:.2f}")
    print(f"Deposit to confirm ({deposit_percentage:.0f}%): R$ {values['deposit_amount']:.2f}")
    print(f"Channel commission ({commission_percentage(booking['channel']):.1f}%): R$ {values['commission_amount']:.2f}")
    print(f"Breakfast: R$ {values['breakfast_cost']:.2f} | Cleaning: R$ {cleaning_fee_per_booking:.2f}")
    print(f"Guesthouse net revenue: R$ {values['net_revenue']:.2f}")


def register_booking(bookings):
    print("\n--- NEW BOOKING ---")
    guest = read_text("Guest name: ")
    channel = choose_channel()
    room = choose_room()
    checkin = read_integer(f"Check-in day (1 to {days_in_month}): ", 1, days_in_month)
    max_nights = days_in_month + 1 - checkin
    nights = read_integer(f"Number of nights (1 to {max_nights}): ", 1, max_nights)

    if not room_is_available(bookings, room, checkin, nights):
        print(f"\nRoom {room} is already taken for part of that period. Booking not registered.")
        return

    guests = read_integer(f"Number of guests (1 to {max_guests_per_room}): ", 1, max_guests_per_room)
    booking = {"guest": guest, "channel": channel, "room": room,
               "checkin": checkin, "nights": nights, "guests": guests}
    show_quote(booking, calculate_booking(booking))

    confirmation = input("\nConfirm booking? (y/n): ").strip().lower()
    if confirmation == "y":
        bookings.append(booking)
        print("Booking registered.")
    else:
        print("Booking discarded.")


def show_bookings(bookings):
    print(f"\n--- BOOKINGS FOR {reference_month.upper()} ---")
    print(f"{'Day':>3} {'Rm':>3}  {'Guest':<18}{'Channel':<17}{'Nights':>6}{'Paid':>11}{'Net':>11}")
    for day in range(1, days_in_month + 1):
        for booking in bookings:
            if booking["checkin"] == day:
                values = calculate_booking(booking)
                print(f"{booking['checkin']:>3} {booking['room']:>3}  {booking['guest']:<18}"
                      f"{booking['channel']:<17}{booking['nights']:>6}"
                      f"{values['amount_paid']:>11.2f}{values['net_revenue']:>11.2f}")
    print(f"Total: {len(bookings)} bookings")


def close_month(bookings):
    totals = {}
    for channel in channels:
        totals[channel] = {"bookings": 0, "nights": 0, "paid": 0.0, "commission": 0.0, "net": 0.0}

    total_tourism_tax = 0.0
    for booking in bookings:
        values = calculate_booking(booking)
        channel_total = totals[booking["channel"]]
        channel_total["bookings"] = channel_total["bookings"] + 1
        channel_total["nights"] = channel_total["nights"] + booking["nights"]
        channel_total["paid"] = channel_total["paid"] + values["amount_paid"]
        channel_total["commission"] = channel_total["commission"] + values["commission_amount"]
        channel_total["net"] = channel_total["net"] + values["net_revenue"]
        total_tourism_tax = total_tourism_tax + values["tourism_tax_total"]

    print(f"\n--- MONTHLY CLOSE: {reference_month.upper()} ---")
    print(f"{'Channel':<17}{'Bookings':>9}{'Nights':>8}{'Paid':>12}{'Commission':>11}{'Net':>12}{'% kept':>10}")

    nights_sold = 0
    month_paid = 0.0
    month_commission = 0.0
    month_net = 0.0
    best_channel = ""
    best_retained_percentage = 0.0

    for channel in channels:
        channel_total = totals[channel]
        retained_percentage = 0.0
        if channel_total["paid"] > 0:
            retained_percentage = channel_total["net"] / channel_total["paid"] * 100
        if retained_percentage > best_retained_percentage:
            best_retained_percentage = retained_percentage
            best_channel = channel
        print(f"{channel:<17}{channel_total['bookings']:>9}{channel_total['nights']:>8}{channel_total['paid']:>12.2f}"
              f"{channel_total['commission']:>11.2f}{channel_total['net']:>12.2f}{retained_percentage:>9.1f}%")
        nights_sold = nights_sold + channel_total["nights"]
        month_paid = month_paid + channel_total["paid"]
        month_commission = month_commission + channel_total["commission"]
        month_net = month_net + channel_total["net"]

    month_retained_percentage = 0.0
    if month_paid > 0:
        month_retained_percentage = month_net / month_paid * 100
    print(f"{'TOTAL':<17}{len(bookings):>9}{nights_sold:>8}{month_paid:>12.2f}{month_commission:>11.2f}"
          f"{month_net:>12.2f}{month_retained_percentage:>9.1f}%")

    available_room_nights = len(rooms) * days_in_month
    occupancy_rate = nights_sold / available_room_nights * 100
    level, recommendation = classify_occupancy(occupancy_rate)

    print(f"\nOccupancy: {occupancy_rate:.1f}% ({nights_sold} of {available_room_nights} room-nights), level {level}")
    print(f"Recommendation: {recommendation}")
    print(f"Commission paid to platforms this month: R$ {month_commission:.2f}")
    print(f"Tourism tax collected and passed on to the city hall: R$ {total_tourism_tax:.2f}")
    print(f"Channel that keeps the largest share of what was paid: {best_channel} ({best_retained_percentage:.1f}%)")


def simulate_direct_channel(bookings):
    print("\n--- SIMULATION: WHAT IF THEY BOOKED DIRECT? ---")
    print("Every Booking and Airbnb booking is made through WhatsApp instead, with no commission,")
    print("and the guest gets an incentive discount to accept the switch.")
    incentive = read_integer("Incentive discount (0 to 30%): ", 0, 30)

    current_net = 0.0
    simulated_net = 0.0
    moved_bookings = 0
    for booking in bookings:
        values = calculate_booking(booking)
        current_net = current_net + values["net_revenue"]
        if booking["channel"] in platform_channels:
            accommodation_with_incentive = values["accommodation_total"] * (100 - incentive) / 100
            direct_net = accommodation_with_incentive - values["breakfast_cost"] - cleaning_fee_per_booking
            simulated_net = simulated_net + direct_net
            moved_bookings = moved_bookings + 1
        else:
            simulated_net = simulated_net + values["net_revenue"]

    difference = simulated_net - current_net
    print(f"\nBookings moved to the direct channel: {moved_bookings}")
    print(f"Actual net revenue for the month: R$ {current_net:.2f}")
    print(f"Simulated net revenue: R$ {simulated_net:.2f}")
    print(f"Difference: R$ {difference:.2f}")

    if moved_bookings == 0:
        print("Conclusion: there are no platform bookings this month, nothing changes.")
    elif difference > 0:
        print("Conclusion: worth it. The incentive costs less than the commission saved.")
    else:
        print("Conclusion: not worth it. The incentive costs more than the commission saved.")

    for channel in platform_channels:
        print(f"On {channel}, any incentive below {commission_percentage(channel):.0f}% still leaves more money in the guesthouse.")


def show_menu():
    print("\n=== GUESTHOUSE: BOOKING BOOK ===")
    print(f"Month: {reference_month} | {len(rooms)} rooms")
    print("1. Register a booking")
    print("2. View this month's bookings")
    print("3. Monthly close by channel")
    print("4. Simulate: what if they booked direct?")
    print("0. Exit")


def run_booking_book():
    option = ""
    while option != "0":
        show_menu()
        option = input("Choose an option: ").strip()
        if option == "1":
            register_booking(monthly_bookings)
        elif option == "2":
            show_bookings(monthly_bookings)
        elif option == "3":
            close_month(monthly_bookings)
        elif option == "4":
            simulate_direct_channel(monthly_bookings)
        elif option == "0":
            print("Goodbye.")
        else:
            print("Invalid option. Choose a number from the menu.")


if __name__ == "__main__":
    run_booking_book()
