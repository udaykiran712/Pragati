from odoo import models, fields, api, _
from odoo.exceptions import UserError


class AccountMove(models.Model):
    _inherit = 'account.move'

    state = fields.Selection(
        [
            ('draft', 'Draft'),
            ('submitted', 'Submitted'),
            ('approved', 'Approved'),
            ('posted', 'Posted'),
            ('cancel', 'Cancelled'),
        ],
        string='Status',
        required=True,
        tracking=True,
        help="The state of the journal entry",
        ondelete={
            'draft': 'set default',
            'submitted': 'set default',
            'approved': 'set default',
        }
    )

    department_id = fields.Many2one('hr.department', string='Department')
    approval_level_1 = fields.Many2one('res.users', string='Approver Level 1')
    approval_level_2 = fields.Many2one('res.users', string='Approver Level 2')
    approval_level_3 = fields.Many2one('res.users', string='Approver Level 3')

    approval_level_1_filled = fields.Boolean(
        string="Approval Level 1 Filled",
        compute="_compute_approver_filled",
        store=False,
    )
    approval_level_2_filled = fields.Boolean(
        string="Approval Level 2 Filled",
        compute="_compute_approver_filled",
        store=False,
    )
    approval_level_3_filled = fields.Boolean(
        string="Approval Level 3 Filled",
        compute="_compute_approver_filled",
        store=False,
    )

    approval_1_approved = fields.Boolean(string="Approval 1 Approved", default=False)
    approval_2_approved = fields.Boolean(string="Approval 2 Approved", default=False)
    approval_3_approved = fields.Boolean(string="Approval 3 Approved", default=False)

    current_approver_id = fields.Many2one(
        'res.users',
        string='Current Approver',
        compute="_compute_current_approver",
        store=False,
    )

    @api.depends('approval_level_1', 'approval_level_2', 'approval_level_3',
                 'approval_1_approved', 'approval_2_approved', 'approval_3_approved', 'state')
    def _compute_current_approver(self):
        for record in self:
            if record.state != 'submitted':
                record.current_approver_id = False
                continue
            if record.approval_level_1 and not record.approval_1_approved:
                record.current_approver_id = record.approval_level_1
            elif record.approval_level_2 and not record.approval_2_approved:
                record.current_approver_id = record.approval_level_2
            elif record.approval_level_3 and not record.approval_3_approved:
                record.current_approver_id = record.approval_level_3
            else:
                record.current_approver_id = False

    @api.depends('approval_level_1', 'approval_level_2', 'approval_level_3')
    def _compute_approver_filled(self):
        for record in self:
            record.approval_level_1_filled = bool(record.id and record.approval_level_1)
            record.approval_level_2_filled = bool(record.id and record.approval_level_2)
            record.approval_level_3_filled = bool(record.id and record.approval_level_3)

    @api.onchange('department_id')
    def _onchange_department_id(self):
        for record in self:
            if record.department_id:
                record.approval_level_1 = record.department_id.approver1
                record.approval_level_2 = record.department_id.approver2
                record.approval_level_3 = record.department_id.approver3
            else:
                record.approval_level_1 = False
                record.approval_level_2 = False
                record.approval_level_3 = False

    def action_submit(self):
        self.ensure_one()

        if not self.partner_id:
            raise UserError(_("You must specify a Customer before submitting."))

        if not self.line_ids:
            raise UserError(_("You need to add a line before submitting."))

        if not self.department_id or not (
                self.approval_level_1 or self.approval_level_2 or self.approval_level_3
        ):
            raise UserError(_("Select a department and at least one approver before submitting."))
        if self.state != 'draft':
            raise UserError(_("Only draft records can be submitted."))
        self.state = 'submitted'

        # Schedule activities for approvers
        if self.approval_level_1:
            self.with_user(self.approval_level_1).activity_schedule(
                activity_type_id=self.env.ref('mail.mail_activity_data_todo').id,
                user_id=self.approval_level_1.id,
                note=_("Please review and approve record %s.") % self.name,
                date_deadline=fields.Date.today(),
            )
        if self.approval_level_2:
            self.with_user(self.approval_level_2).activity_schedule(
                activity_type_id=self.env.ref('mail.mail_activity_data_todo').id,
                user_id=self.approval_level_2.id,
                note=_("Please review and approve record %s.") % self.name,
                date_deadline=fields.Date.today(),
            )
        if self.approval_level_3:
            self.with_user(self.approval_level_3).activity_schedule(
                activity_type_id=self.env.ref('mail.mail_activity_data_todo').id,
                user_id=self.approval_level_3.id,
                note=_("Please review and approve record %s.") % self.name,
                date_deadline=fields.Date.today(),
            )

    def action_post(self):
        for record in self:
            if record.state != 'approved':
                raise UserError(_("You must wait for all approvers' approval before confirmation."))
        return super(AccountMove, self).action_post()

    def action_approve(self):
        self.ensure_one()
        if self.env.user != self.current_approver_id:
            raise UserError(_("You are not authorized to approve at this stage."))
        if self.current_approver_id == self.approval_level_1:
            self.approval_1_approved = True
        elif self.current_approver_id == self.approval_level_2:
            self.approval_2_approved = True
        elif self.current_approver_id == self.approval_level_3:
            self.approval_3_approved = True
        self._check_all_approved()

    def _check_all_approved(self):
        for record in self:
            approved = all([
                (not record.approval_level_1 or record.approval_1_approved),
                (not record.approval_level_2 or record.approval_2_approved),
                (not record.approval_level_3 or record.approval_3_approved)
            ])
            if approved:
                record.state = 'approved'
