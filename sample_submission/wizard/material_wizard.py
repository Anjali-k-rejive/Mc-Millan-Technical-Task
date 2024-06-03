from odoo import models, fields, api


class MaterialWizard(models.TransientModel):
    _name = 'material.wizard'
    _description = 'Material Wizard'

    sl_no = fields.Integer(string='Sl No', readonly=True, )
    product_id = fields.Many2one('product.product', string='Material', required=True)
    quantity = fields.Float(string='Quantity', required=True)
    remarks = fields.Text(string='Remarks')

    def create_materials(self):
        active_id = self.env.context.get('active_id')
        if active_id:
            material_sl_no = self.env['sample.submission'].browse(active_id)
            max_sl_no = max(material_sl_no.material_required_ids.mapped('sl_no'), default=0)
            self.env['material.required'].create({
                'sl_no': max_sl_no + 1,
                'product_id': self.product_id.id,
                'quantity': self.quantity,
                'remarks': self.remarks,
                'sample_id': active_id,
            })
        return {'type': 'ir.actions.act_window_close'}
