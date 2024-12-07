# Copyright (c) 2024, Ambibuzz Technologies LLP and contributors
# For license information, please see license.txt

import frappe
from frappe.website.website_generator import WebsiteGenerator
from frappe import _

class Shop(WebsiteGenerator):
    def before_save(self):
        if self.status == "Available":
            self.tenant_details = None
            self.contract_expiry = None
            frappe.msgprint(
                _(
                    "Shop available."
                ),
                alert=True,
            )
