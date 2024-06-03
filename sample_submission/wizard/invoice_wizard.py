from odoo import models, fields, api

class SampleSubmissionInvoiceConfirmWizard(models.TransientModel):
    _name = 'sample.submission.invoice.confirm.wizard'
    _description = 'Confirm Invoice Generation Wizard'

    sample_submission_id = fields.Many2one('sample.submission', string='Sample Submission', required=True)
    reference = fields.Char(string='Reference')
    price = fields.Float(string='Price')
    discount = fields.Float(string='Discount')
    vat = fields.Char(string='VAT')

    def action_confirm(self):
        self.ensure_one()
        sample_submission = self.sample_submission_id

        # Create the invoice
        invoice_vals = {
            'partner_id': self.env.user.partner_id.id,
            'move_type': 'out_invoice',
            'invoice_line_ids': [(0, 0, {
                'name': sample_submission.reference,
                'quantity': 1,
                'price_unit': sample_submission.price,
                'discount': sample_submission.discount,

            })],
        }
        invoice = self.env['account.move'].create(invoice_vals)

        # Mark the sample submission as invoiced
        sample_submission.is_invoiced = True

        return {'type': 'ir.actions.act_window_close'}