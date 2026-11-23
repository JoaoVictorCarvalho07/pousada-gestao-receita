"""Regras de negócio da pousada de 8 quartos.

A fórmula veio de theme2.py (fechamento interativo de outubro/2026). O que mudou
para o lote em CSV está em README.md, seção "Adaptações em relação ao theme2.py".
Diária, hóspede extra, desconto por duração, comissão, café, limpeza, taxa de
turismo (repasse) e receita líquida seguem calculate_booking daquele arquivo.
"""

from calendar import monthrange

N_ROOMS = 8
STANDARD_CAPACITY = 2
MAX_GUESTS = 4
BREAKFAST = 18.00
CLEANING = 70.00
EXTRA_GUEST_FEE = 60.00
TOURISM_TAX = 4.00

CHANNELS = ["Booking", "Airbnb", "Own website", "WhatsApp direct"]
COMMISSION = {
    "Booking": 15.0,
    "Airbnb": 14.0,
    "Own website": 3.0,
    "WhatsApp direct": 0.0,
}
ROOMS = {
    1: {"type": "Standard", "nightly_rate": 250.00},
    2: {"type": "Standard", "nightly_rate": 250.00},
    3: {"type": "Standard", "nightly_rate": 250.00},
    4: {"type": "Standard", "nightly_rate": 250.00},
    5: {"type": "Superior", "nightly_rate": 320.00},
    6: {"type": "Superior", "nightly_rate": 320.00},
    7: {"type": "Superior", "nightly_rate": 320.00},
    8: {"type": "Suite", "nightly_rate": 420.00},
}

# Fechamento conhecido de outubro/2026, produzido pelo caderno embutido em theme2.py.
OCTOBER_REFERENCE = {
    "source_file": "reservas_2026-10.csv",
    "year": 2026,
    "month": 10,
    "bookings": 39,
    "nights": 134,
    "occupancy_percent": 54.0,
    "net_revenue": 27234.12,
    "commission": 3535.08,
}


class ReconciliationError(Exception):
    """O lote fechou, mas não bate com o fechamento conhecido de outubro."""


def discount_percentage(number_of_nights):
    if number_of_nights >= 7:
        return 15.0
    if number_of_nights >= 3:
        return 8.0
    return 0.0


def commission_percentage(channel):
    return COMMISSION[channel]


def extra_guests(number_of_guests):
    if number_of_guests > STANDARD_CAPACITY:
        return number_of_guests - STANDARD_CAPACITY
    return 0


def calculate_booking(booking):
    nightly_rate = ROOMS[booking["room"]]["nightly_rate"]
    nights = booking["nights"]
    guests = booking["guests"]

    room_charges = nightly_rate * nights
    extra_guest_charge = EXTRA_GUEST_FEE * extra_guests(guests) * nights
    discount_pct = discount_percentage(nights)
    discount_amount = (room_charges + extra_guest_charge) * discount_pct / 100
    accommodation_total = room_charges + extra_guest_charge - discount_amount
    tourism_tax_total = TOURISM_TAX * guests * nights
    amount_paid = accommodation_total + tourism_tax_total
    commission_pct = commission_percentage(booking["channel"])
    commission_amount = accommodation_total * commission_pct / 100
    breakfast_cost = BREAKFAST * guests * nights
    net_revenue = accommodation_total - commission_amount - breakfast_cost - CLEANING

    return {
        "room_type": ROOMS[booking["room"]]["type"],
        "nightly_rate": nightly_rate,
        "room_charges": room_charges,
        "extra_guest_charge": extra_guest_charge,
        "discount_percentage": discount_pct,
        "discount_amount": discount_amount,
        "accommodation_total": accommodation_total,
        "tourism_tax_total": tourism_tax_total,
        "amount_paid": amount_paid,
        "commission_percentage": commission_pct,
        "commission_amount": commission_amount,
        "breakfast_cost": breakfast_cost,
        "cleaning_fee": CLEANING,
        "net_revenue": net_revenue,
    }


def available_room_nights(year, month):
    return N_ROOMS * monthrange(year, month)[1]


def occupancy_percent(nights_sold, year, month):
    return nights_sold / available_room_nights(year, month) * 100
