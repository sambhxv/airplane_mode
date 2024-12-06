import frappe

def execute():
    tickets = frappe.get_all("Airplane Ticket", fields=["name", "seat"])
    for ticket in tickets:
        if ticket.seat:
            continue
        assigned_seat = assign_seat(ticket)
        frappe.db.set_value("Airplane Ticket", ticket.name, "seat", assigned_seat)
        frappe.db.commit()

def assign_seat(ticket):
    return f"Seat-{ticket.name[-4:]}"
