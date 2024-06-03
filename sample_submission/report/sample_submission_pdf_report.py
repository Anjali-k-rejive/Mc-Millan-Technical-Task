from odoo import models, fields, api

class SampleSubmissionReport(models.TransientModel):
    _name = 'sample.submission.report.wizard'
    _description = 'Sample Submission Report'

    date_from = fields.Date(string='Date From')
    date_to = fields.Date(string='Date To')

    def action_sample_pdf_report(self):
        domain = []
        if self.date_from:
            domain.append(('date_submission', '>=', self.date_from))
        if self.date_to:
            domain.append(('date_submission', '<=', self.date_to))

        submissions = self.env['sample.submission'].search(domain)
        sample_data = submissions.read(['date_submission', 'customer_id', 'reference', 'price'])
        data = {
            'submissions': sample_data if sample_data else [],
        }

        return self.env.ref('sample_submission.action_report_pdf_sample_submission').report_action(self, data=data)

    def action_xlsx_report(self):
        domain = []
        if self.date_from:
            domain.append(('date_submission', '>=', self.date_from))
        if self.date_to:
            domain.append(('date_submission', '<=', self.date_to))

        submissions = self.env['sample.submission'].search(domain)
        sample_data = submissions.read(['date_submission', 'customer_id', 'reference', 'price'])
        for sub in sample_data:
            sub['customer_id'] = sub['customer_id'][1] if sub['customer_id'] else ''
        data = {
            'submissions': sample_data if sample_data else [],
        }

        return self.env.ref('sample_submission.action_report_xlsx_sample_submission').report_action(self, data=data)

