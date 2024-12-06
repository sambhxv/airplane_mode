# Copyright (c) 2024, Ambibuzz Technologies LLP and contributors
# For license information, please see license.txt

import frappe
import random
from frappe.model.document import Document

class AirplaneTicket(Document):
    def before_save(self):
        if self.is_new():
            self.check_airplane_capacity()
            self.generate_seat()

    def validate(self):
        self.check_gate_pass()
        self.remove_duplicate_add_ons()
        self.calculate_total_amount()

    def before_submit(self):
        self.check_the_status_equal_to_booked()

    def check_the_status_equal_to_booked(self):
        if self.status != "Boarded":
            frappe.throw(
                f'Please Set The Status To "Boarded" Before Submitting The Document!'
            )

    def remove_duplicate_add_ons(self):
        unique_items = {}
        unique_data = []
        add_ons = self.add_ons

        if add_ons:
            for item in add_ons:
                item_name = item.item
                if item_name not in unique_items:
                    unique_items[item_name] = True
                    unique_data.append(item)
        self.add_ons = unique_data

    def calculate_total_amount(self):
        flight_price = self.flight_price if self.flight_price else 0
        add_ons = self.add_ons
        total_add_on_amount = 0

        if add_ons:
            for item in add_ons:
                total_add_on_amount += item.amount if item.amount else 0

        self.total_amount = flight_price + total_add_on_amount

    def generate_seat(self):
        random_integer = random.randint(1, 100)
        random_alphabet = random.choice("ABCDE")
        seat = f"{random_integer}{random_alphabet}"
        self.seat = seat

    def check_airplane_capacity(self):
        airplane_flight = self.flight
        flight_name = frappe.db.get_value(
            "Airplane Flight", airplane_flight, "airplane"
        )
        flight_capacity = frappe.db.get_value("Airplane", flight_name, "capacity")
        get_all_tickets = frappe.get_list(
            "Airplane Ticket",
            filters={"flight": airplane_flight},
            fields=["name"],
        )
        if len(get_all_tickets) >= flight_capacity:
            frappe.throw("All The Tickets of The Selected Flight Has Been Booked!")

    def check_gate_pass(self):
        if self.status == "Boarded" and (
            self.gate_pass == None or self.gate_pass == ""
        ):
            frappe.throw(
                """You cannot get "Boarded" without the "Gate Pass" please create one!"""
            )
