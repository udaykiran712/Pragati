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
    'name': 'Base - Hospital Management System ( HMS by AlmightyCS )',
    'summary': 'Hospital Management System Base for further flows',
    'description': """
        Hospital Management System for managing Hospital and medical facilities flows
        Medical Flows ACS HMS

        This module helps you to manage your hospitals and clinics which includes managing
        Patient details, Doctor details, Prescriptions, Treatments, Appointments with concerned doctors,
        Invoices for the patients. You can also define the medical alerts of a patient and get warining in appointment,treatments and prescriptions. It includes all the basic features required in Health Care industry.
        
        healthcare services healthcare administration healthcare management health department 
        hospital management information system hospital management odoo hms odoo medical alert

        Ce module vous aide à gérer vos hôpitaux et vos cliniques, ce qui inclut la gestion
         Détails du patient, détails du médecin, prescriptions, traitements, rendez-vous avec les médecins concernés,
         Factures pour les patients. Il comprend toutes les fonctionnalités de base requises dans l'industrie des soins de santé.
        
        services de santé administration des soins de santé gestion des soins de santé département de la santé
         système d'information de gestion hospitalière gestion hospitalière odoo hms odoo

        Système de gestion hospitalière pour la gestion des flux d'hôpitaux et d'installations médicales
         Flux médicaux ACS HMS

        نظام إدارة المستشفيات لإدارة تدفقات المستشفيات والمرافق الطبية
        التدفقات الطبية ACS HMS

        هذه الوحدة تساعدك على إدارة مستشفيات وعياداتك التي تشمل الإدارة
        تفاصيل المريض ، تفاصيل الطبيب ، الوصفات الطبية ، العلاجات ، المواعيد مع الأطباء المعنيين ،
        ويشمل جميع الميزات الأساسية المطلوبة في صناعة الرعاية الصحية.فواتير للمرضى.

        خدمات الرعاية الصحية إدارة الرعاية الصحية إدارة الصحة الصحية
        إدارة مستشفى إدارة معلومات نظام إدارة

        Hospital Management System zur Verwaltung von Krankenhaus- und medizinischen Abläufen
         Medizinische Strömungen ACS HMS

        Dieses Modul hilft Ihnen bei der Verwaltung Ihrer Krankenhäuser und Kliniken, einschließlich der Verwaltung
         Angaben zum Arzt, Angaben zum Arzt, Rezepte, Behandlungen, Termine mit betroffenen Ärzten,
         Rechnungen für die Patienten. Es enthält alle grundlegenden Funktionen, die in der Gesundheitsbranche erforderlich sind.

        Gesundheitsdienste Gesundheitsverwaltung Gesundheitsmanagement Gesundheitsabteilung
         Krankenhaus-Management-Informationssystem Krankenhaus-Management odoo hms odoo

        
        Sistema de gestión hospitalaria para la gestión de flujos hospitalarios e instalaciones médicas.
         Flujos medicos ACS HMS

        This module helps you to manage your hospitals and clinics which includes managing
        Patient details, Doctor details, Prescriptions, Treatments, Appointments with concerned doctors,
        Invoices for the patients. It includes all the basic features required in Health Care industry.

        servicios de salud administración de la salud administración de la salud departamento de salud
         gestión hospitalaria sistema de información gestión hospitalaria odoo hms odoo
    """,
    'version': '1.0.15',
    'category': 'Industry',
    'author': 'Almighty Consulting Solutions Pvt. Ltd.',
    'support': 'info@almightycs.com',
    'website': 'https://www.almightycs.com',
    'license': 'OPL-1',
    'depends': ['account', 'stock', 'hr', 'product_expiry'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',

        'report/paper_format.xml',
        'report/report_layout.xml',
        'report/report_invoice.xml',

        'data/sequence.xml',
        'data/mail_template.xml',
        'data/company_data.xml',

        'views/hms_base_views.xml',
        'views/patient_view.xml',
        'views/physician_view.xml',
        'views/product_view.xml',
        'views/drug_view.xml',
        'views/account_view.xml',
        'views/res_config_settings.xml',
        'views/stock_view.xml',
        'views/menu_item.xml',
    ],
    'demo': [
        'demo/company_demo.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'acs_hms_base/static/src/scss/report.scss'
        ],
        "web.assets_common": [
            "acs_hms_base/static/src/js/acs.js",
            'acs_hms_base/static/src/scss/acs.scss',
        ],
    },
    'images': [
        'static/description/hms_almightycs_cover.jpg',
    ],
    'installable': True,
    'application': True,
    'sequence': 1,
    'price': 36,
    'currency': 'USD',
}

#   Disclaimer: We Collect following information for analytics and improving our product/services.
#   Number of Users, Patients, Dr, Appointments, Prescriptions, Laboratory, Radiology, 
#       Surgery, Hospitalization and other medical records (Only Count)
#   Company Name, List of installed modules, DB key, email, mobile and url (to match customer data to update details.)
#   Only if related modules are installed those data will be fetched.
#   We do not sale this information or pulish customer details anywhere without having approval from customer
#   This same detail get used for our monthly subscription users also.
#   Privay Policy: https://www.almightycs.com/privacy-policy

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: