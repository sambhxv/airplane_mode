# Copyright (c) 2024, Ambibuzz Technologies LLP and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import getdate
from datetime import timedelta


class Agreement(Document):
    def validate(self):
        if self.contract_start and self.contract_end:
            contract_start_date = getdate(self.contract_start)
            contract_end_date = getdate(self.contract_end)
            if contract_end_date < contract_start_date + timedelta(days=365):
                frappe.throw(
                    _(
                        "Contract end date must be at least one year after the Contract start date."
                    ),
                    title=_("Invalid contract dates"),
                )

        if self.shop:
            shop_doc = frappe.get_doc("Shop", self.shop)
            if shop_doc.status == "Unavailable":
                frappe.throw(
                    _("Shop {0} is not available.").format(shop_doc.shop_name),
                    title=_("Shop already rented"),
                )

    def after_insert(self):
        if self.shop:
            shop_doc = frappe.get_doc("Shop", self.shop)
            shop_doc.status = "Unavailable"
            shop_doc.tenant_details = self.tenant
            shop_doc.contract_expiry = self.contract_end
            shop_doc.save(ignore_permissions=True)
            frappe.msgprint(
                _("Shop {0} has been 'rented'.").format(shop_doc.shop_name),
                alert=True,
            )
