{
    "name": "Kiosks Management",
    "version": "1.0",
    "depends": ["base", "account"],  # 'account' for invoicing , "web_google_maps"
    "author": "Marugu",
    "website": "https://yourwebsite.com",
    "category": "Government",
    "license": "LGPL-3",
    "summary": "Manage kiosks, vendors, licensing, and payments",
    "description": "Track kiosk rentals, sales, and licensing with automated renewals and payments.",
    "data":[
        "security/ir.model.access.csv",  # Security file
        "views/vendor_views.xml",       # UI for Vendors
        "views/license_view.xml",      # UI for Licenses
        "views/kiosk_views.xml",        # UI for Kiosks
        "views/menu.xml",
        "data/reminder_cron.xml",
        "data/email_template.xml",
        ],
    'assets': {
        'web.assets_backend': [
            'kiosks/static/src/css/kiosk_styles.css',
            'kiosks/static/src/img/small.png',
            'kiosks/static/src/img/medium.png',
            'kiosks/static/src/img/large.png',
        ],
    },
    'images': ['kiosks/static/description/icon.png'],
    'icon' : 'kiosks/static/description/icon.png',
    "installable": True,
    "application": True,
    "auto_install": False,
}
