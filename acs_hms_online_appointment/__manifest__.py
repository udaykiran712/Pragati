# -*- coding: utf-8 -*-
#╔══════════════════════════════════════════════════════════════════════╗
#║                                                                      ║
#║                  ╔═══╦╗       ╔╗  ╔╗     ╔═══╦═══╗                   ║
#║                  ║╔═╗║║       ║║ ╔╝╚╗    ║╔═╗║╔═╗║                   ║
#║                  ║║ ║║║╔╗╔╦╦══╣╚═╬╗╔╬╗ ╔╗║║ ╚╣╚══╗                   ║
#║                  ║╚═╝║║║╚╝╠╣╔╗║╔╗║║║║║ ║║║║ ╔╬══╗║                   ║
#║                  ║╔═╗║╚╣║║║║╚╝║║║║║╚╣╚═╝║║╚═╝║╚═╝║                   ║
#║                  ╚╝ ╚╩═╩╩╩╩╩═╗╠╝╚╝╚═╩═╗╔╝╚═══╩═══╝                   ║
#║                            ╔═╝║     ╔═╝║                             ║
#║                            ╚══╝     ╚══╝                             ║
#║                  SOFTWARE DEVELOPED AND SUPPORTED BY                 ║
#║                ALMIGHTY CONSULTING SOLUTIONS PVT. LTD.               ║
#║                      COPYRIGHT (C) 2016 - TODAY                      ║
#║                      https://www.almightycs.com                      ║
#║                                                                      ║
#╚══════════════════════════════════════════════════════════════════════╝
{
    'name' : 'HMS Online Appointment',
    'summary' : 'Allow patients to Book an Appointment on-line from portal',
    'description' : """HMS Website Portal to Book an Appointment online. acs hms medical Allow patients to Book an Appointment online from portal""",
    'version': '1.1.14',
    'category': 'Industry',
    'author': 'Almighty Consulting Solutions Pvt. Ltd.',
    'website': 'https://www.almightycs.com',
    'license': 'OPL-1',
    'depends' : ['acs_hms_portal','website_payment','account_payment'],
    'data' : [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/data.xml',
        'data/website_page.xml',
        'views/hms_base_view.xml',
        'views/schedule_views.xml',
        'views/template.xml',
        'views/res_users.xml',
        'views/res_config_settings_views.xml',
        'wizard/appointment_scheduler_wizard.xml',
        'wizard/payment_link_views.xml',
        'views/menu_item.xml',
    ],
    'assets': {
        'web.assets_frontend': [        
            'acs_hms_online_appointment/static/src/js/payment_form.js',
            'acs_hms_online_appointment/static/src/js/hms_portal.js',
            'acs_hms_online_appointment/static/src/scss/custom.scss',
        ]
    },
    'images': [
        'static/description/acs_hms_online_booking_almightycs_cover.jpg',
    ],
    'installable': True,
    'application': True,
    'sequence': 1,
    'price': 70,
    'currency': 'USD',
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: