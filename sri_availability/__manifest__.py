{
    "name": "Sri Availability",
    "version": "18.0.0.1.0",
    "category": "Inventory",
    "license": "AGPL-3",
    "summary": "Calculate stock picking based on product quantity and unit of measure",
    "description": """
This module provides functionality to calculate stock picking based on the product quantity and unit of measure.
    """,
    "author": "Ahmed Hassan",
    "website": "",
    "depends": [
        "stock",
        "sale",
        "product",
        "account",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/stock_picking_views.xml",
        "reports/report_template.xml",
        "reports/report_action.xml",
    ],
    "installable": True,
    "application": False,
    "auto_install": False,
}