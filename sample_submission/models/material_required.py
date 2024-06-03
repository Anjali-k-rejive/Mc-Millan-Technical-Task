from odoo import models, fields

class MaterialRequired(models.Model):
    _name = 'material.required'
    _description = 'Material Required'

    sl_no = fields.Integer(string='Sl No', readonly=True)
    product_id = fields.Many2one('product.product', string='Material', required=True)
    quantity = fields.Float(string='Quantity', required=True)
    remarks = fields.Text(string='Remarks')
    sample_id = fields.Many2one('sample.submission', string='Sample Submission')