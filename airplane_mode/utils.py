import frappe
from datetime import datetime, timedelta

def send_rent_reminders():
        today = datetime.now().date()

        payments = frappe.get_all(
            "Payment",
            filters={"status": ["in", ["Pending", "Overdue"]]},
            fields=["tenant_name", "rent_amount", "payment_date", "status"],
        )
        reminders_sent = 0
        for payment in payments:
            payment_date = datetime.strptime(payment["payment_date"], "%Y-%m-%d").date()

            if payment_date <= today + timedelta(days=3):
                reminder_message = (
                    f"Dear {payment['tenant_name']},\n\n"
                    f"This is a reminder that your rent payment of ₹{payment['rent_amount']} "
                    f"is due on {payment_date}. Please ensure the payment is made promptly to avoid penalties.\n\n"
                    "Thank you,\nAirport Shop Management"
                )
                tenant_email = frappe.db.get_value(
                    "Tenant", payment["tenant_name"], "email"
                )
                if tenant_email:
                    frappe.sendmail(
                        recipients=[tenant_email],
                        subject="Rent Payment Reminder",
                        message=reminder_message,
                    )
                    reminders_sent += 1
        frappe.log(f"{reminders_sent} rent reminders sent.")
