# Copyright (c) 2024, Ambibuzz Technologies LLP and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class Payment(Document):
    def on_submit(self):
        self.status = "Paid"
        self.receipt_number = frappe.generate_hash(self.name, 10)
