# Copyright (c) 2024, Ambibuzz Technologies LLP and contributors
# For license information, please see license.txt

import frappe


def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    chart = get_chart(data)
    summary = get_summary(data)
    return columns, data, None, chart, summary


def get_columns():
    return [
        {
            "fieldname": "airline",
            "label": "Airline",
            "fieldtype": "Link",
            "options": "Airline",
            "width": "200",
        },
        {
            "fieldname": "revenue",
            "label": "Revenue",
            "fieldtype": "Currency",
            "width": "200",
        },
    ]


def get_data(filters):
    data = frappe.db.sql(
        """ 
            SELECT
                all_airlines.name AS airline,
                COALESCE(SUM(ticket.total_amount), 0) AS revenue
            FROM
                (SELECT name FROM `tabAirline`) AS all_airlines
                LEFT JOIN `tabAirplane` AS airplane ON all_airlines.name = airplane.airline
                LEFT JOIN `tabAirplane Flight` AS flight ON airplane.name = flight.airplane
                LEFT JOIN `tabAirplane Ticket` AS ticket ON flight.name = ticket.flight
            GROUP BY
                all_airlines.name
            ORDER BY
                revenue DESC;
        """,
        as_dict=True,
    )

    return data


def get_chart(data):
    return {
        "data": {
            "labels": [d["airline"] for d in data],
            "datasets": [
                {
                    "name": "Revenue By Airline",
                    "values": [d["revenue"] for d in data],
                },
            ],
        },
        "type": "donut",
    }


def get_summary(data):
    total_revenue = 0
    for item in data:
        total_revenue += item["revenue"]

    return [
        {
            "label": "Total Revenue",
            "value": total_revenue,
        }
    ]
