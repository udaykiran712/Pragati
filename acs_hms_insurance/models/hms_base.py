# -*- coding: utf-8 -*-
from datetime import datetime
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, AccessError, UserError, RedirectWarning, Warning


class ACSPatient(models.Model):
    _inherit = 'hms.patient'

    def _rec_count(self):
        rec = super(ACSPatient, self)._rec_count()
        for rec in self:
            rec.claim_count = len(rec.claim_ids)

    claim_ids = fields.One2many('hms.insurance.claim', 'patient_id',string='Claims')
    claim_count = fields.Integer(compute='_rec_count', string='# Claims')
    insurance_ids = fields.One2many('hms.patient.insurance', 'patient_id', string='Insurance')

    def action_insurance_policy(self):
        action = self.env["ir.actions.actions"]._for_xml_id("acs_hms_insurance.action_hms_patient_insurance")
        action['domain'] = [('patient_id', '=', self.id)]
        action['context'] = {
            'default_patient_id': self.id,
        }
        return action

    def action_claim_view(self):
        action = self.env["ir.actions.actions"]._for_xml_id("acs_hms_insurance.action_insurance_claim")
        action['domain'] = [('patient_id', '=', self.id)]
        action['context'] = {
            'default_patient_id': self.id,
        }
        return action


class ACSAppointment(models.Model):
    _inherit = 'hms.appointment'

    READONLY_STATES = {'cancel': [('readonly', True)], 'done': [('readonly', True)]}

    insurance_id = fields.Many2one('hms.patient.insurance', string='Insurance Policy', states=READONLY_STATES)
    claim_id = fields.Many2one('hms.insurance.claim', string='Claim', states=READONLY_STATES)
    insurance_company_id = fields.Many2one('hms.insurance.company', related='insurance_id.insurance_company_id', string='Insurance Company', readonly=True, store=True)
    app_insurance_percentage = fields.Float(related='insurance_id.app_insurance_percentage', string="Insured Percentage", readonly=True)

    def create_invoice(self):
        res = super(ACSAppointment, self).create_invoice()
        if self.invoice_id and self.insurance_id and (self.insurance_id.app_insurance_limit >= self.invoice_id.amount_total or self.insurance_id.app_insurance_limit==0):
            insurace_invoice = self.invoice_id.acs_create_insurace_invoice(self.insurance_id, self.insurance_id.app_insurance_type, 
                self.insurance_id.app_insurance_amount, self.insurance_id.app_insurance_percentage, 
                self, 'appointment', 'appointment_id', self.insurance_id.create_claim)
            if insurace_invoice and insurace_invoice.claim_id:
                self.claim_id = insurace_invoice.claim_id.id
        return res

    def create_consumed_prod_invoice(self):
        res = super(ACSAppointment, self).create_consumed_prod_invoice()
        if self.consumable_invoice_id and self.insurance_id and (self.insurance_id.app_insurance_limit >= self.consumable_invoice_id.amount_total or self.insurance_id.app_insurance_limit==0):
            insurace_invoice = self.consumable_invoice_id.acs_create_insurace_invoice(self.insurance_id, self.insurance_id.app_insurance_type, 
                self.insurance_id.app_insurance_amount, self.insurance_id.app_insurance_percentage, 
                self, 'appointment', 'appointment_id', self.insurance_id.create_claim)
            if insurace_invoice and insurace_invoice.claim_id:
                self.claim_id = insurace_invoice.claim_id.id
        return res

    @api.onchange('patient_id')
    def onchange_patient_id(self):
        super(ACSAppointment, self).onchange_patient_id()
        allow_appointment_insurances = self.patient_id.insurance_ids.filtered(lambda x: x.allow_appointment_insurance)
        pricelist_id = insurance_id = False
        if self.patient_id and allow_appointment_insurances:
            insurance = allow_appointment_insurances[0]
            insurance_id = insurance.id
            pricelist_id = insurance.pricelist_id and insurance.pricelist_id.id or False
    
        self.insurance_id = insurance_id
        self.pricelist_id = pricelist_id


class Invoice(models.Model):
    _inherit = 'account.move'

    insurance_id = fields.Many2one('hms.patient.insurance', string='Insurance Policy')
    claim_id = fields.Many2one('hms.insurance.claim', 'Claim')
    insurance_company_id = fields.Many2one('hms.insurance.company', related='claim_id.insurance_company_id', string='Insurance Company', readonly=True)
    claim_sheet_id = fields.Many2one('acs.claim.sheet', string='Claim Sheet')
    patient_invoice_id = fields.Many2one('account.move', string='Patient Invoice')
    patient_invoice_amount = fields.Monetary(related="patient_invoice_id.amount_total", string='Patient Invoice Amount', store=True)

    #ACS: Hook method to avoid error of spit invocie on auto invoice.
    def acs_check_auto_spliting_possibility(self, insurance_id):
        return True

    def acs_create_insurace_invoice(self, insurance, insurance_type, insurance_amount, insurance_percentage, acs_object, inv_type, rec_field, create_claim=False):
        can_be_splited = self.acs_check_auto_spliting_possibility(insurance)
        claim_id = False
        insurance_invoice_id = False
        if can_be_splited:
            if insurance.patient_share_in_invoice:
                insurance_amount += self.acs_get_patientshare_amount(insurance)

            split_context = {
                'active_model':'account.move', 
                'active_id': self.id,
                'insurance_id': insurance.id,
                'insurance_type': insurance_type,
                'insurance_amount': insurance_amount,
            }

            wiz_id = self.env['split.invoice.wizard'].with_context(split_context).create({
                'split_selection': 'invoice',
                'percentage': insurance_percentage,
                'partner_id': insurance.insurance_company_id.partner_id.id if insurance.insurance_company_id.partner_id else self.partner_id.id,
            })
            insurance_invoice_id = wiz_id.split_record()
            insurance_invoice_id.write({
                'insurance_id': insurance.id,
                rec_field: acs_object.id,
                'ref': acs_object.name,
                'invoice_origin': acs_object.name,
                'hospital_invoice_type': inv_type,
                'patient_invoice_id': self.id,
            })

            if wiz_id.update_partner and not self.insurance_id:
                self.insurance_id = insurance.id

            if insurance_invoice_id and create_claim:
                claim_id = self.env['hms.insurance.claim'].create({
                    'patient_id': self.patient_id.id,
                    'insurance_id': insurance.id,
                    'claim_for': inv_type,
                    rec_field: acs_object.id,
                    'amount_requested': insurance_invoice_id.amount_total,
                })
                insurance_invoice_id.claim_id = claim_id.id
        return insurance_invoice_id

    def acs_get_patientshare_amount(self, insurance):
        amount = 0
        Rule = self.env['acs.insurance.policy.rule']
        for line in self.invoice_line_ids.filtered(lambda x: x.product_id):
            matching_rule = False
            product_tmpl_id = line.product_id.product_tmpl_id.id
            product_categ_id = line.product_id.categ_id.id
            if insurance.policy_rule_ids:
                rule_ids = insurance.policy_rule_ids.ids
                matching_rule = Rule.search([('id','in',rule_ids),
                    ('product_id','=',product_tmpl_id)], limit=1)
                if not matching_rule:
                    matching_rule = Rule.search([('id','in',rule_ids),
                    ('product_category_id','=',product_categ_id)], limit=1)

            if not matching_rule and insurance.insurance_company_id.policy_rule_ids:
                company_rule_ids = insurance.insurance_company_id.policy_rule_ids.ids
                matching_rule = Rule.search([('id','in', company_rule_ids),
                    ('product_id','=',product_tmpl_id)], limit=1)
                if not matching_rule:
                    matching_rule = Rule.search([('id','in', company_rule_ids),
                    ('product_category_id','=',product_categ_id)], limit=1)

            if matching_rule:
                if matching_rule.rule_type == 'percentage':
                    amount += (matching_rule.percentage * line.price_subtotal)/100
                elif matching_rule.rule_type == 'amount':
                    amount += matching_rule.amount
        return amount


class AccountPayment(models.Model):
    _inherit = 'account.payment'

    claim_id = fields.Many2one('hms.insurance.claim', 'Claim')
    insurance_company_id = fields.Many2one('hms.insurance.company', related='claim_id.insurance_company_id', string='Insurance Company', readonly=True)

class Attachments(models.Model):
    _inherit = "ir.attachment"

    patient_id = fields.Many2one('hms.patient', 'Patient')
    claim_id = fields.Many2one('hms.insurance.claim', 'Claim')


class product_template(models.Model):
    _inherit = "product.template"

    hospital_product_type = fields.Selection(selection_add=[('insurance_plan', 'Insurance Plan')])

class ACSPrescriptionOrder(models.Model):
    _inherit = 'prescription.order'

    insurance_id = fields.Many2one('hms.patient.insurance', string='Insurance Policy')
    claim_id = fields.Many2one('hms.insurance.claim', string='Claim')
    insurance_company_id = fields.Many2one('hms.insurance.company', related='insurance_id.insurance_company_id', string='Insurance Company', readonly=True, store=True)
    pha_insurance_percentage = fields.Float(related='insurance_id.pha_insurance_percentage', string="Insured Percentage", readonly=True)

    @api.onchange('patient_id')
    def onchange_patient_id(self):
        allow_pharmacy_insurance = self.patient_id.insurance_ids.filtered(lambda x: x.allow_pharmacy_insurance)
        if self.patient_id and allow_pharmacy_insurance:
            insurance = allow_pharmacy_insurance[0]
            self.insurance_id = insurance.id

    #Maneged it in hms_pharmacy
    # def create_invoice(self):
    #     res = super(ACSPrescriptionOrder, self).create_invoice()
    #     if self.invoice_id and self.insurance_id and (self.insurance_id.pha_insurance_limit >= self.invoice_id.amount_total or self.insurance_id.pha_insurance_limit==0):
    #         insurace_invoice = self.invoice_id.acs_create_insurace_invoice(self.insurance_id, self.insurance_id.pha_insurance_type, 
    #             self.insurance_id.pha_insurance_amount, self.insurance_id.pha_insurance_percentage, 
    #             self, 'pharmacy', 'prescription_id', self.insurance_id.pha_create_claim)
    #         if insurace_invoice and insurace_invoice.claim_id:
    #             self.claim_id = insurace_invoice.claim_id.id
