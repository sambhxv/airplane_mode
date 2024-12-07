# Copyright (c) 2024, Ambibuzz Technologies LLP and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from datetime import timedelta

class FlightCrew(Document):
    def before_save(self):
        self.check_crew_member_slot()
        self.check_crew_member_schedule()

    def before_submit(self):
        self.check_status_before_submit()

    def check_crew_member_schedule(self):
        crew_schedule = False
        departure_date = self.departure_date
        departure_day = departure_date.strftime("%A")
        departure_time = self.departure_time
        duration_of_flight = self.duration_of_flight
        duration_in_timedelta = timedelta(seconds=duration_of_flight)
        crew_member = self.crew_member
        crew_member_doc = frappe.get_doc("Crew Member", crew_member)
        crew_member_schedule = crew_member_doc.working_schedule
        for row in crew_member_schedule:
            from_time = row.from_time
            to_time = (
                row.to_time
                if row.to_time > row.from_time
                else row.to_time + timedelta(hours=24)
            )
            working_day = row.working_day
            if working_day == departure_day:
                if from_time <= departure_time <= to_time:
                    if from_time < departure_time + duration_in_timedelta < to_time:
                        crew_schedule = True

        if crew_schedule:
            pass
        else:
            frappe.throw(
                """The "Departure Time" or The "Flight Duration" does not match the crew member's schedule!"""
            )

    def check_crew_member_slot(self):
        crew_member = self.crew_member
        flight = self.flight
        check_slot = frappe.get_list(
            "Flight Crew",
            filters={
                "name": ["!=", self.name],
                "crew_member": crew_member,
                "flight": flight,
            },
            fields=["name"],
        )
        if check_slot:
            frappe.throw(
                """The "Flight" is already scheduled with the selected "Crew Member"!"""
            )

    def check_status_before_submit(self):
        if self.status == "Scheduled" or self.status == "Ongoing":
            frappe.throw(
                f"""You cannot submit the with "Scheduled" or "Ongoing" Status!"""
            )
