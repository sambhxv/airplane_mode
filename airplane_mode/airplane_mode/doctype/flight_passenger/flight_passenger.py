# Copyright (c) 2024, Ambibuzz Technologies LLP and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class FlightPassenger(Document):

	def before_save(self):
		self.set_full_name()

	def set_full_name(self):
		first_name = self.first_name
		last_ame = self.last_name

		self.full_name = (first_name if first_name else "") + (" "+last_ame if last_ame else "")
