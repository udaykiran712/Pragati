# -*- encoding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class AccountMove(models.Model):
    _name = 'account.move'
    _inherit = ['account.move','acs.whatsapp.mixin']

    def action_post(self):
        res = super(AccountMove, self).action_post()
        for rec in self:
            if rec.hospital_invoice_type=='pharmacy' and rec.partner_id.mobile:
                template = self.env.user.sudo().company_id.acs_pharmacy_order_template_id
                if rec.partner_id.mobile and template:
                    rendered = self.env['mail.render.mixin']._render_template(template.body_message, rec._name, [rec.id])
                    msg = rendered[rec.id]
                    rec.send_whatsapp(msg, rec.partner_id.mobile, rec.partner_id, template=template)
        return res

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: