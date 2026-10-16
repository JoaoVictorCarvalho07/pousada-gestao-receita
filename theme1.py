breakfast_cost_per_guest_per_night = 18.00
cleaning_fee_per_booking = 70.00
extra_guest_fee_per_night = 60.00
tourism_tax_per_guest_per_night = 4.00
deposit_percentage = 30.0

guest_name = input("Guest name: ")
booking_channel = input("Booking channel (Booking, Airbnb, Own website, WhatsApp direct): ")
commission_percentage = float(input("Channel commission percentage (%): "))
nightly_rate = float(input("Room nightly rate (R$): "))
number_of_nights = int(input("Number of nights: "))
included_guests = int(input("Guests included in the rate (up to 2): "))
extra_guests = int(input("Extra guests (above 2): "))

number_of_guests = included_guests + extra_guests
guest_nights = number_of_guests * number_of_nights

room_charges = nightly_rate * number_of_nights
extra_guest_charge = extra_guest_fee_per_night * extra_guests * number_of_nights
accommodation_total = room_charges + extra_guest_charge
tourism_tax_total = tourism_tax_per_guest_per_night * guest_nights
amount_paid = accommodation_total + tourism_tax_total
deposit_amount = amount_paid * deposit_percentage / 100
balance_due_at_checkin = amount_paid - deposit_amount

commission_amount = accommodation_total * commission_percentage / 100
breakfast_cost = breakfast_cost_per_guest_per_night * guest_nights
total_cost = commission_amount + breakfast_cost + cleaning_fee_per_booking
net_revenue = accommodation_total - total_cost

net_revenue_per_night = net_revenue / number_of_nights
net_revenue_per_guest = net_revenue / number_of_guests
retained_percentage = net_revenue / amount_paid * 100

print("\n--- BOOKING QUOTE ---")
print(f"Guest: {guest_name}")
print(f"Channel: {booking_channel}")
print(f"Stay: {number_of_nights} night(s) for {number_of_guests} guest(s), {extra_guests} of them extra")

print("\nWHAT THE GUEST PAYS")
print(f"Room charges: R$ {room_charges:.2f}")
print(f"Extra guest: R$ {extra_guest_charge:.2f}")
print(f"Tourism tax: R$ {tourism_tax_total:.2f}")
print(f"Total: R$ {amount_paid:.2f}")
print(f"Deposit to confirm ({deposit_percentage:.0f}%): R$ {deposit_amount:.2f}")
print(f"Balance due at check-in: R$ {balance_due_at_checkin:.2f}")

print("\nWHAT LEAVES THE GUESTHOUSE CASH BOX")
print(f"Channel commission ({commission_percentage:.1f}%): R$ {commission_amount:.2f}")
print(f"Breakfast: R$ {breakfast_cost:.2f}")
print(f"Cleaning: R$ {cleaning_fee_per_booking:.2f}")
print(f"Tourism tax passed on to the city hall: R$ {tourism_tax_total:.2f}")

print("\nWHAT IS LEFT")
print(f"Guesthouse net revenue: R$ {net_revenue:.2f}")
print(f"Per night: R$ {net_revenue_per_night:.2f}")
print(f"Per guest: R$ {net_revenue_per_guest:.2f}")
print(f"Share kept of the amount paid: {retained_percentage:.1f}%")
