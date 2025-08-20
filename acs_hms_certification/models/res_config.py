# -*- encoding: utf-8 -*-
from odoo import api, fields, models,_


class ResCompany(models.Model):
    _inherit = "res.company"

    acs_certificate_qrcode = fields.Boolean(string="Print Authetication QrCode on Certificate", default=True)

    @api.model_create_multi
    def create(self, vals_list):
        res = super().create(vals_list)
        for record in res:
            record.acs_create_sequence(name='Certificate Management', code='certificate.management', prefix='CRT')
        return res


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    acs_certificate_qrcode = fields.Boolean(related='company_id.acs_certificate_qrcode', string="Print Authetication QrCode on Certificate", readonly=False)
 