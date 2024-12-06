# Copyright (c) 2024, Ambibuzz Technologies LLP and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class GatePass(Document):

    def on_trash(self):
        self.remove_link_gate_pass()

    def remove_link_gate_pass(self):
        frappe.db.set_value("Airplane Ticket", self.ticket, "gate_pass", "")
