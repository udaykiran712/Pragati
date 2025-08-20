# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError
import uuid


class PatientLabTest(models.Model):
    _name = "patient.laboratory.test"
    _inherit = ['mail.thread', 'mail.activity.mixin', 'acs.hms.mixin', 'portal.mixin', 'acs.documnt.mixin', 'acs.qrcode.mixin']
    _description = "Patient Laboratory Test"
    _order = 'date_analysis desc, id desc'

    @api.model
    def _get_disclaimer(self):
        return self.env.user.sudo().company_id.acs_laboratory_disclaimer or ''

    STATES = {'cancel': [('readonly', True)], 'done': [('readonly', True)]}

    name = fields.Char(string='Test ID', help="Lab result ID", readonly="1",copy=False, index=True, tracking=True)
    test_id = fields.Many2one('acs.lab.test', string='Test', required=True, ondelete='restrict', states=STATES, tracking=True)
    patient_id = fields.Many2one('hms.patient', string='Patient', required=True, ondelete='restrict', states=STATES, tracking=True)
    user_id = fields.Many2one('res.users',string='Lab User', default=lambda self: self.env.user, states=STATES)
    physician_id = fields.Many2one('hms.physician',string='Prescribing Doctor', help="Doctor who requested the test", ondelete='restrict', states=STATES)
    lab_physician_id = fields.Many2one('hms.physician',string='Pathology Doctor', help="Doctor who Approved the test", ondelete='restrict', states=STATES)

    diagnosis = fields.Text(string='Diagnosis', states=STATES)
    critearea_ids = fields.One2many('lab.test.critearea', 'patient_lab_id', string='Test Cases', copy=True, states=STATES)
    date_requested = fields.Datetime(string='Request Date', states=STATES)
    date_analysis = fields.Datetime(string='Test Date', default=fields.Datetime.now, states=STATES)
    request_id = fields.Many2one('acs.laboratory.request', string='Test Request', ondelete='restrict', states=STATES)
    laboratory_id = fields.Many2one('acs.laboratory', related="request_id.laboratory_id", string='Laboratory', readonly=True, store=True)
    report = fields.Text(string='Test Report', states=STATES)
    note = fields.Text(string='Extra Info', states=STATES)
    sample_ids = fields.Many2many('acs.patient.laboratory.sample', 'test_lab_sample_rel', 'test_id', 'sample_id', string='Test Samples', states=STATES)
    company_id = fields.Many2one('res.company', ondelete='restrict', 
        string='Company', default=lambda self: self.env.company, states=STATES)
    state = fields.Selection([
        ('draft','Draft'),
        ('done','Done'),
        ('cancel','Cancel'),
    ], string='Status',readonly=True, default='draft', tracking=True)
    consumable_line_ids = fields.One2many('hms.consumable.line', 'patient_lab_test_id',
        string='Consumable Line', states=STATES)
    disclaimer = fields.Text("Dislaimer", states=STATES, default=_get_disclaimer)
    collection_center_id = fields.Many2one('acs.laboratory', string='Collection Center', related="request_id.collection_center_id", states=STATES)
    parent_test_id = fields.Many2one('patient.laboratory.test', string='Parent Test', ondelete='cascade', copy=False)
    child_test_ids = fields.One2many('patient.laboratory.test', 'parent_test_id', string='Child Tests', copy=False)

    #Just to make object selectable in selction field this is required: Waiting Screen
    acs_show_in_wc = fields.Boolean(default=True)

    _sql_constraints = [
        ('name_company_uniq', 'unique (name,company_id)', 'Test Name must be unique per company !')
    ]

    def _track_subtype(self, init_values):
        self.ensure_one()
        if 'state' in init_values and self.state == 'done':
            return self.env.ref('acs_laboratory.mt_lab_test_done')
        return super(PatientLabTest, self)._track_subtype(init_values)

    def _compute_display_name(self):
        for rec in self:
            name = rec.name or '-'
            if rec.test_id:
                name += ' [' + rec.test_id.name + ']'
            rec.display_name = name

    def _subscribe_physician(self):
        done_subtype = self.env.ref('acs_laboratory.mt_lab_test_done').id
        comment_subtype = self.env.ref('mail.mt_comment').id
        for rec in self:
            if rec.physician_id.partner_id and rec.physician_id.partner_id.id not in rec.message_partner_ids.ids:
                rec.message_subscribe(partner_ids=[rec.physician_id.partner_id.id], subtype_ids=[done_subtype,comment_subtype])

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            vals['name'] = self.env['ir.sequence'].next_by_code('patient.laboratory.test')
        res = super().create(vals_list)
        for record in res:
            record.unique_code = uuid.uuid4()
            record._subscribe_physician()
        return res

    def write(self, values):
        for sample_id in self.sample_ids:
            if sample_id.state not in ['examine', 'collect']:
                raise UserError(_("Patient Lab Sample is not collected yet."))
        if 'physician_id' in values:
            self._subscribe_physician()
        return super(PatientLabTest, self).write(values)

    def unlink(self):
        for rec in self:
            if rec.state not in ['draft']:
                raise UserError(_("Lab Test can be delete only in Draft state."))
        return super(PatientLabTest, self).unlink()

    @api.onchange('request_id')
    def onchange_request_id(self):
        if self.request_id and self.request_id.date:
            self.date_requested = self.request_id.date

    def action_lab_test_send(self):
        '''
        This function opens a window to compose an email, with the template message loaded by default
        '''
        self.ensure_one()
        template_id = self.env['ir.model.data']._xmlid_to_res_id('acs_laboratory.acs_lab_test_email', raise_if_not_found=False)

        ctx = {
            'default_model': 'patient.laboratory.test',
            'default_res_id': self.ids[0],
            'default_use_template': bool(template_id),
            'default_template_id': template_id,
            'default_composition_mode': 'comment',
            'force_email': True
        }
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'mail.compose.message',
            'views': [(False, 'form')],
            'view_id': False,
            'target': 'new',
            'context': ctx,
        }

    @api.onchange('test_id')
    def on_change_test(self):
        test_lines = []
        if self.test_id:
            gender = self.patient_id.gender
            for line in self.test_id.critearea_ids:
                test_lines.append((0,0,{
                    'sequence': line.sequence,
                    'name': line.name,
                    'normal_range': line.normal_range_female if gender=='female' else line.normal_range_male,
                    'lab_uom_id': line.lab_uom_id and line.lab_uom_id.id or False,
                    'remark': line.remark,
                    'display_type': line.display_type,
                }))
            self.critearea_ids = test_lines

    def action_done(self):
        for sample_id in self.sample_ids:
            if sample_id.state not in ['examine']:
                raise UserError(_("Patient Lab Sample is not Examined yet."))
        self.consume_lab_material()
        self.state = 'done'
    #     self.notify_physician()

    # def notify_physician(self):
    #     for test in self:
    #         if test.physician_id:
    #             action_id = self.env.ref('acs_laboratory.patient_laboratory_test_view').id

    #             activity = self.env['mail.activity'].create({
    #                 'activity_type_id': 4,  # 4 represents a To Do activity
    #                 'res_id': test.id,
    #                 'res_model_id': self.env.ref('acs_laboratory.patient_laboratory_test_view').id,
    #                 'date_deadline': fields.Date.today(),  # Set deadline to today
    #                 'user_id': test.physician_id.user_id.id,
    #                 'summary': 'Lab results uploaded for test: %s' % test.name,
    #                 'note': 'Lab results uploaded for test: %s' % test.name,
    #                 'display_name': 'Lab results uploaded',
    #                 'res_name': test.name,
    #                 # 'activity_type_icon': '<i class="fa fa-flask"/>',  # Example icon for the activity
    #                 # 'action_id': action_id,
    #             })
    #             activity.action_done() 
    #             related_record = self.env[activity.res_model_id.model].browse(activity.res_id)
    #             related_record.write({'active': False}) 
    def action_cancel(self):
        self.state = 'cancel'

    def action_draft(self):
        self.state = 'draft'

    def acs_get_consume_locations(self):
        if not self.company_id.laboratory_usage_location_id:
            raise UserError(_('Please define a location where the consumables will be used during the Laboratory test in company.'))
        if not self.company_id.laboratory_stock_location_id:
            raise UserError(_('Please define a Laboratory location from where the consumables will be taken.'))

        dest_location_id  = self.company_id.laboratory_usage_location_id.id
        source_location_id  = self.company_id.laboratory_stock_location_id.id
        return source_location_id, dest_location_id

    def consume_lab_material(self):
        for rec in self:
            source_location_id, dest_location_id = rec.acs_get_consume_locations()
            for line in rec.consumable_line_ids.filtered(lambda s: not s.move_id):
                if line.product_id.is_kit_product:
                    move_ids = []
                    for kit_line in line.product_id.acs_kit_line_ids:
                        if kit_line.product_id.tracking!='none':
                            raise UserError("In Consumable lines Kit product with component having lot/serial tracking is not allowed. Please remove such kit product from consumable lines.")
                        move = self.consume_material(source_location_id, dest_location_id,
                            {'product': kit_line.product_id, 'qty': kit_line.product_qty * line.qty})
                        move.lab_test_id = rec.id
                        move_ids.append(move.id)
                    #Set move_id on line also to avoid issue
                    line.move_id = move.id
                    line.move_ids = [(6,0,move_ids)]
                else:
                    move = self.consume_material(source_location_id, dest_location_id,
                        {'product': line.product_id, 'qty': line.qty, 'lot_id': line.lot_id and line.lot_id.id or False,})
                    move.lab_test_id = rec.id
                    line.move_id = move.id

    def _compute_access_url(self):
        super(PatientLabTest, self)._compute_access_url()
        for rec in self:
            rec.access_url = '/my/lab_results/%s' % (rec.id)

    def action_view_lab_samples(self):
        action = self.env["ir.actions.actions"]._for_xml_id("acs_laboratory.action_acs_patient_laboratory_sample")
        action['domain'] = [('id','in',self.sample_ids.ids)]
        action['context'] = {'search_default_today': False}
        return action

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: