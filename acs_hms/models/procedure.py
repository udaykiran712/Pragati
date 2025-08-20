# -- coding: utf-8 --

from odoo import api, fields, models ,_
from odoo.exceptions import UserError
from datetime import date, datetime, timedelta
from odoo.exceptions import ValidationError
from pytz import timezone
import pytz


class ProcedureGroupLine(models.Model):
    _name = "procedure.group.line"
    _description = "Procedure Group Line"
    _order = 'sequence'

    sequence = fields.Integer("Sequence", default=10)
    group_id = fields.Many2one('procedure.group', ondelete='restrict', string='Procedure Group')
    product_id = fields.Many2one('product.product', string='Procedure', ondelete='restrict', required=True)
    days_to_add = fields.Integer('Sessions',help="Days to add for next date")
    procedure_time = fields.Float(related='product_id.procedure_time', string='Procedure Time', readonly=True)
    price_unit = fields.Float(related='product_id.list_price', string='Price', readonly=True)


class ProcedureGroup(models.Model):
    _name = "procedure.group"
    _description = "Procedure Group"

    name = fields.Char(string='Group Name', required=True)
    line_ids = fields.One2many('procedure.group.line', 'group_id', string='Group lines')


class AcsPatientProcedure(models.Model):
    _name="acs.patient.procedure"
    _inherit = ['mail.thread', 'mail.activity.mixin', 'acs.hms.mixin', 'acs.documnt.mixin']
    _description = "Patient Procedure"
    _order = "id desc"

    STATES = {'cancel': [('readonly', True)], 'done': [('readonly', True)]}

    @api.depends('date', 'date_stop')
    def acs_get_duration(self):
        for rec in self:
            duration = 0.0
            if rec.date and rec.date_stop:
                diff = rec.date_stop - rec.date
                duration = (diff.days * 24) + (diff.seconds/3600)
            rec.duration = duration

    def _acs_get_attachemnts(self):
        attachments = super(AcsPatientProcedure, self)._acs_get_attachemnts()
        attachments += self.appointment_ids.mapped('attachment_ids')
        return attachments
    timer_started = fields.Boolean(string='Timer Started', default=False)
    start_time = fields.Datetime(string='Start Time')
    end_time = fields.Datetime(string='End Time')
    stop_button_clicked = fields.Boolean(default=False)
    name = fields.Char(string="Name", states=STATES, tracking=True)
    patient_id = fields.Many2one('hms.patient', string='Patient', required=True, states=STATES, tracking=True)
    product_id = fields.Many2one('product.product', string='Procedure', 
        change_default=True, ondelete='restrict', states=STATES, required=True)
    price_unit = fields.Float("Price", states=STATES, compute='_compute_price_unit')
    invoice_id = fields.Many2one('account.move', string='Invoice', states=STATES, copy=False)
    physician_id = fields.Many2one('hms.physician', ondelete='restrict', string='Physician', 
        index=True, states=STATES)
    state = fields.Selection([
        ('scheduled', 'Scheduled'),
        ('running', 'Running'),
        ('done', 'Done'),
        ('cancel', 'Canceled'),
    ], string='Status', default='scheduled', tracking=True)
    company_id = fields.Many2one('res.company', ondelete='restrict', states=STATES,
        string='Hospital', default=lambda self: self.env.company)
    date = fields.Datetime("Date", states=STATES)
    date_stop = fields.Datetime("End Date", states=STATES)
    duration = fields.Float('Duration', compute="acs_get_duration", store=True)
    therapy_room_id = fields.Many2one('therapy.rooms')
    therapist_id = fields.Many2one('hms.therapist')
    therapy_room_id = fields.Many2one('therapy.rooms', string="Therapy Room")
    sessions = fields.Integer(string="Sessions")
    diseas_id = fields.Many2one('hms.diseases', 'Disease', states=STATES)
    description = fields.Text(string="Description", states=STATES)
    treatment_id = fields.Many2one('hms.treatment', 'Treatment', states=STATES)
    appointment_ids = fields.Many2many('hms.appointment', 'acs_appointment_procedure_rel', 'appointment_id', 'procedure_id', 'Appointments', states=STATES)
    department_id = fields.Many2one('hr.department', ondelete='restrict', 
        domain=[('patient_department', '=', True)], string='Department', tracking=True, states=STATES)
    department_type = fields.Selection(related='department_id.department_type', string="Appointment Department", store=True)

    consumable_line_ids = fields.One2many('hms.consumable.line', 'procedure_id',
        string='Consumable Line', states=STATES, copy=False)
    acs_kit_id = fields.Many2one('acs.product.kit', string='Kit', states=STATES)
    acs_kit_qty = fields.Integer("Kit Qty", states=STATES, default=1)

    

    @api.onchange('date','date_stop')
    def _onchange_appointment_date_time(self):
        if self.date and self.date_stop:
            requested_start_time = self.date
            utc = pytz.utc
            ist = pytz.timezone('Asia/Kolkata')

            utc_start_datetime = self.date  
            requested_start_time = utc_start_datetime.astimezone(ist)
            utc_end_datetime = self.date_stop  
            requested_end_time = utc_end_datetime.astimezone(ist)
            
            
            overlapping_appointments = self.env['acs.patient.procedure'].search([
                ('therapist_id', '!=', False),
              
            ])
           
            booked_therapists = [] 
            booked_therapy_names = []
            for appointment in overlapping_appointments :
                for a in appointment:
                    if a.state != 'done':
                        utc_start_datetime = a.date  
                        start_date_ist = utc_start_datetime.astimezone(ist)
                        if a.date_stop :
                            utc_end_datetime = a.date_stop 
                            end_date_ist = utc_end_datetime.astimezone(ist)
                            if (start_date_ist <= requested_start_time <= end_date_ist) or (start_date_ist <= requested_end_time <= end_date_ist) or (requested_start_time <= start_date_ist <= requested_end_time) or (requested_start_time <=  end_date_ist <= requested_end_time):                         
                                if a.therapist_id.id not in booked_therapists:
                                    booked_therapists.append(a.therapist_id.id)
                                if a.therapy_room_id:
                                    booked_therapy_names.append(a.therapy_room_id.id)
                
            if booked_therapists or booked_therapy_names:
                domain_filter = {
                    'therapist_id': [('id', 'not in', booked_therapists)],
                    'therapy_room_id': [('id', 'not in', booked_therapy_names)]
                }
                return {
                    'domain': domain_filter
                }
            else:
                return {}


# **************************************************available therapist  above**********************
    
    
                
           
    def start_timer(self):
        self.timer_started = True
        self.start_time = fields.Datetime.now()

    def pause_timer(self):
        if self.timer_started:
            self.timer_started = False
            self.end_time = fields.Datetime.now()

    def stop_timer(self):
        if self.timer_started:
            self.timer_started = False
            self.end_time = fields.Datetime.now()
            self.stop_button_clicked = True
            
    def get_time(self):
        if self.timer_started:
            return fields.Datetime.now() - self.start_time
        elif self.end_time:
            return self.end_time - self.start_time
        else:
            return 'No time recorded'
    @api.model
    def default_get(self, fields):
        res = super(AcsPatientProcedure, self).default_get(fields)
        if self._context.get('acs_department_type'):
            department = self.env['hr.department'].search([('department_type','=',self._context.get('acs_department_type'))], limit=1)
            if department:
                res['department_id'] = department.id
        return res

    # @api.onchange('product_id')
    # def onchange_product(self):
    #     if self.product_id:
    #         self.price_unit = self.product_id.list_price


    # @api.depends('consumable_line_ids.subtotal')
    # def _compute_price_unit_from_kit(self):
    #     for line in self:
    #         line.price_unit = sum(line.consumable_line_ids.mapped('subtotal'))
    
    @api.depends('product_id')
    def _compute_price_unit(self):
        for line in self:
            cost_price = line.product_id.standard_price
            sale_price = line.product_id.list_price
            line.price_unit = sale_price


    @api.onchange('product_id','date')
    def onchange_date_and_product(self):
        if self.product_id and self.product_id.procedure_time and self.date:
            self.date_stop = self.date + timedelta(hours=self.product_id.procedure_time)

    def action_running(self):
        self.state = 'running'

    def action_schedule(self):
        self.state = 'scheduled'

    def action_done(self):
        if self.consumable_line_ids:
            self.consume_procedure_material()
        self.state = 'done'

    def action_cancel(self):
        self.state = 'cancel'

    def unlink(self):
        for rec in self:
            if rec.state not in ['scheduled','cancel']:
                raise UserError(_('Record can be deleted only in Canceled/Scheduled state.'))
        return super(AcsPatientProcedure, self).unlink()

    @api.model_create_multi
    def create(self, vals_list):
        for values in vals_list:
            values['name'] = self.env['ir.sequence'].next_by_code('acs.patient.procedure') or 'New Procedure'
        return super().create(vals_list)

    def get_procedure_invoice_data(self):
        product_data = [{
            'name': _("Patient Procedure Charges"),
        }]
        for rec in self:
            #Pass price if it is updated else pass 0
            #so if 0 is passed it will apply pricelist value properly.
            procedure_data = {'product_id': rec.product_id, 'price_unit': rec.price_unit}
            product_data.append(procedure_data)

            #Line for procedure Consumables
            # for consumable in rec.consumable_line_ids:
            #     product_data.append({
            #         'product_id': consumable.product_id,
            #         'quantity': consumable.qty,
            #         'lot_id': consumable.lot_id and consumable.lot_id.id or False,
            #     })
        return product_data

    def action_create_invoice(self):
        product_data = self.get_procedure_invoice_data()

        inv_data = {
            'physician_id': self.physician_id and self.physician_id.id or False,
            'hospital_invoice_type': 'procedure',
        }
        acs_context = {'commission_partner_ids':self.physician_id.partner_id.id}
        invoice = self.with_context(acs_context).acs_create_invoice(partner=self.patient_id.partner_id, patient=self.patient_id, product_data=product_data, inv_data=inv_data)
        self.invoice_id = invoice.id
        self.invoice_id.procedure_id = self.id        

    def acs_get_consume_locations(self):
        if not self.company_id.procedure_usage_location_id:
            raise UserError(_('Please define a procedure location where the consumables will be used.'))
        if not self.company_id.procedure_stock_location_id:
            raise UserError(_('Please define a procedure location from where the consumables will be taken.'))

        dest_location_id  = self.company_id.procedure_usage_location_id.id
        source_location_id  = self.company_id.procedure_stock_location_id.id
        return source_location_id, dest_location_id

    def consume_procedure_material(self):
        for rec in self:
            source_location_id, dest_location_id = rec.acs_get_consume_locations()
            for line in rec.consumable_line_ids.filtered(lambda s: not s.move_id):
                if line.product_id.is_kit_product:
                    move_ids = []
                    for kit_line in line.product_id.acs_kit_line_ids:
                        if kit_line.product_id.tracking!='none':
                            raise UserError("In Consumable lines Kit product with component having lot/serial tracking is not allowed.")

                        move = self.consume_material(source_location_id, dest_location_id,
                            {'product': kit_line.product_id, 'qty': kit_line.product_qty * line.qty})
                        move.procedure_id = rec.id
                        move_ids.append(move.id)
                    #Set move_id on line also to avoid 
                    line.move_id = move.id
                    line.move_ids = [(6,0,move_ids)]
                else:
                    move = self.consume_material(source_location_id, dest_location_id,
                        {'product': line.product_id, 'qty': line.qty, 'lot_id': line.lot_id and line.lot_id.id or False})
                    move.procedure_id = rec.id
                    line.move_id = move.id

    def view_invoice(self):
        invoices = self.mapped('invoice_id')
        action = self.acs_action_view_invoice(invoices)
        return action

    def action_show_details(self):
        self.ensure_one()
        action = self.env["ir.actions.actions"]._for_xml_id("acs_hms.action_acs_patient_procedure")
        action['context'] = {'default_patient_id': self.patient_id.id}
        action['res_id'] = self.id
        action['views'] = [(self.env.ref('acs_hms.view_acs_patient_procedure_form').id, 'form')]
        action['target'] = 'new'
        return action

    def get_acs_kit_lines(self):
        if not self.acs_kit_id:
            raise UserError("Please Select Kit first.")

        lines = []
        for line in self.acs_kit_id.acs_kit_line_ids:
            lines.append((0,0,{
                'product_id': line.product_id.id,
                'product_uom_id': line.product_id.uom_id.id,
                'qty': line.product_qty * self.acs_kit_qty,
            }))
        self.consumable_line_ids = lines

    @api.onchange('acs_kit_id')
    def _onchange_acs_kit_id(self):
        for record in self:
            if record.acs_kit_id:
                record.consumable_line_ids = [(5, 0, 0)]
                lines = []
                for line in self.acs_kit_id.acs_kit_line_ids:
                    lines.append((0,0,{
                        'product_id': line.product_id.id,
                        'product_uom_id': line.product_id.uom_id.id,
                        'qty': line.product_qty * self.acs_kit_qty,
                        'price_unit': line.unit_price,
                    }))
                record.consumable_line_ids = lines


    #method to create get invocie data and set passed invocie id.
    def acs_common_invoice_procedure_data(self, invoice_id=False):
        data = []
        if self.ids:
            data = self.get_procedure_invoice_data()
            if invoice_id:
                self.invoice_id = invoice_id.id
        return data


class StockMove(models.Model):
    _inherit = "stock.move"

    procedure_id = fields.Many2one('acs.patient.procedure', ondelete="cascade", string="Procedure")

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: