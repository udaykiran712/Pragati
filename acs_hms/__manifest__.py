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
    'name': 'Clinic - Hospital Management System ( HMS by AlmightyCS )',
    'summary': 'Hospital Management System for managing Hospital and medical facilities flows',
    'description': """
        Hospital Management System for managing Hospital and medical facilities flows
        Medical Flows ACS HMS Clinic Management Manage Clinic

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
    'version': '1.3.37',
    'category': 'Industry',
    'author': 'Almighty Consulting Solutions Pvt. Ltd.',
    'support': 'info@almightycs.com',
    'website': 'https://www.almightycs.com',
    'live_test_url': 'https://www.youtube.com/watch?v=hiumJoDEHxI',
    'license': 'OPL-1',
    'depends': ['acs_hms_base', 'web_timer_widget', 'website', 'digest','account'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',

        'report/patient_cardreport.xml',
        'report/report_medical_advice.xml',
        'report/report_prescription.xml',
        'report/appointment_report.xml',
        'report/evaluation_report.xml',
        'report/treatment_report.xml',
        'report/procedure_report.xml',
        'report/medicines_label_report.xml',

        'data/sequence.xml',
        'data/mail_template.xml',
        'data/hms_data.xml',
        'data/digest_data.xml',
        
        'wizard/cancel_reason_view.xml',
        'wizard/pain_level_view.xml',
        'wizard/reschedule_appointments_view.xml',
        'wizard/updating_therapy_room_therapist_views.xml',

        'views/hms_base_views.xml',
        'views/hms_consumable_line.xml',
        'views/patient_view.xml',
        'views/physician_view.xml',
        'views/evaluation_view.xml',
        'views/appointment_view.xml',
        'views/diseases_view.xml',
        'views/medicament_view.xml',
        'views/prescription_view.xml',
        'views/medication_view.xml',
        'views/treatment_view.xml',
        'views/procedure_view.xml',
        'views/resource_cal.xml',
        'views/medical_alert.xml',
        'views/account_view.xml',
        'views/product_kit_view.xml',
        'views/template.xml',
        'views/res_config_settings_views.xml',
        'views/digest_view.xml',
        'views/res_users.xml',
        'views/menu_item.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'acs_hms/static/src/js/hms_graph_field.js',
            'acs_hms/static/src/js/hms_graph_field.xml',
            'acs_hms/static/src/js/hms_graph_field.scss',
            'acs_hms/static/src/scss/custom.scss',
        ]
    },
    'demo': [
        'demo/doctor_demo.xml',
        'demo/patient_demo.xml',
        'demo/appointment_demo.xml',
        'demo/medicament_demo.xml',
    ],
    'images': [
        'static/description/hms_almightycs_cover.gif',
    ],
    'installable': True,
    'application': True,
    'sequence': 1,
    'price': 36,
    'currency': 'USD',
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: