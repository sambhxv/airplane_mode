# Copyright (c) 2024, Ambibuzz Technologies LLP and contributors
# For license information, please see license.txt

from frappe.website.website_generator import WebsiteGenerator

class AirplaneFlight(WebsiteGenerator):

    def on_submit(self):
        self.update_status_to_completed()

    def update_status_to_completed(self):
        self.status = "Completed"
