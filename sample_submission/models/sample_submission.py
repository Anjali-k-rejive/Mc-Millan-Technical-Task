from odoo import models, fields, api, _
from odoo.exceptions import UserError


class SampleSubmission(models.Model):
    _name = 'sample.submission'
    _description = 'Sample Submission'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'reference'

    reference = fields.Char(string='Sample Sequence Number', required=True, copy=False, readonly=True,
                            default=lambda self: _('New'))
    customer_id = fields.Many2one('res.partner', string='Customer', required=True, tracking=True)
    date_submission = fields.Date(string='Date of Submission', required=True, default=fields.Date.today,tracking=True)
    description = fields.Text(string='Description', tracking=True)
    price = fields.Float(string='Price', compute='_compute_price', tracking=True, store=True)
    discount = fields.Float(string='Discount', tracking=True)
    vat = fields.Char(string='VAT', related="customer_id.vat", tracking=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('pending', 'Pending'),
        ('doing', 'Doing'),
        ('completed', 'Completed')
    ], string='Stage', default='draft', tracking=True)
    material_required_ids = fields.One2many('material.required', 'sample_id', string='Materials Required',
                                            tracking=True)
    is_invoiced = fields.Boolean(string='Invoiced', default=False, tracking=True)

    @api.depends('material_required_ids.product_id', 'material_required_ids.quantity')
    def _compute_price(self):
        for record in self:
            total_price = 0.0
            for line in record.material_required_ids:
                total_price += line.product_id.list_price * line.quantity
            record.price = total_price


    @api.model
    def create(self, vals):
        if vals.get('reference', _('New')) == _('New'):
            vals['reference'] = self.env['ir.sequence'].next_by_code('sample.submission') or _('New')
        return super(SampleSubmission, self).create(vals)

    def action_open_material_wizard(self):
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'material.wizard',
            'view_mode': 'form',
            'view_id': self.env.ref('sample_submission.view_material_wizard_form').id,
            'target': 'new',
            'context': {
                'default_submission_id': self.id,
            }
        }

    def action_generate_invoice(self):

        self.ensure_one()
        if self.state != 'completed':
            raise UserError("The stage must be 'completed' to generate an invoice.")
        if self.is_invoiced:
            raise UserError("This submission has already been invoiced.")

        return {
            'name': 'Confirm Invoice Generation',
            'type': 'ir.actions.act_window',
            'res_model': 'sample.submission.invoice.confirm.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_sample_submission_id': self.id,
                'default_reference': self.reference,
                'default_price': self.price,
                'default_discount': self.discount,
                'default_vat': self.vat,
            }
        }
