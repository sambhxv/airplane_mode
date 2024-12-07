# Copyright (c) 2024, Ambibuzz Technologies LLP and contributors
# For license information, please see license.txt

import frappe
from frappe.website.website_generator import WebsiteGenerator

class AirplaneFlight(WebsiteGenerator):

	def on_submit(self):
		self.status = "Completed"

	def on_cancle(self):
		self.status='Cancelled'

	def update_gate_number(doc, method):
		new_gate_number = doc.gate_number
		tickets = frappe.get_all("Airplane Ticket", filters={"flight": doc.name}, fields=["name"])
		for ticket in tickets:
			ticket_doc = frappe.get_doc("Airplane Ticket", ticket["name"])
			ticket_doc.gate_number = new_gate_number
			ticket_doc.save()
		frappe.msgprint(f"Gate number updated in all linked tickets for flight {doc.name}.")
