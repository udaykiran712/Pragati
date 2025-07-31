# -*- coding: utf-8 -*-
{
    'name' : 'Internal Tansaction',
    'summary': 'Send SMS notification to Employee and Customer.',
    
    'depends' : ['account','base'],
    
    'data': [
        'views/account_views.xml',
        'views/ledger_payments_views.xml',
        'views/bill_wise_adjustments.xml',
        'security/ir.model.access.csv',
        'security/internal_trans_security.xml',
        'data/data.xml',
        'data/ir_sequence_data.xml',
        ],
    'assets': {
        'web.assets_backend': [
            'gft_inter_account/static/src/js/search_bar.js',  # Corrected path
        ],
    },

}