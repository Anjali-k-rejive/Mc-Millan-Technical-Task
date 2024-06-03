from odoo import models



class SampleSubmissionXlsxReport(models.AbstractModel):
    _name = 'report.sample_submission.report_xlsx_sample_submission'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, submissions):
        sheet = workbook.add_worksheet('Sample Submissions')
        title = "Sample Submission Report"
        date_format = workbook.add_format({'num_format': 'dd/mm/yyyy'})
        bold = workbook.add_format({'bold': True, 'align': 'center', 'valign': 'vcenter'})
        sheet.set_column('A:A',20)
        sheet.set_column('B:B',40)
        sheet.set_column('C:C',40)
        sheet.set_column('D:D',20)


        # Write title
        sheet.merge_range('B1:D1', title, bold, )

        # Write headers
        headers = ['Date', 'Customer', 'Reference', 'Price']
        for col, header in enumerate(headers):
            sheet.write(2, col, header, bold)

        # Write data rows
        row = 3

        for sub in data['submissions']:
            sheet.write(row, 0, sub['date_submission'], date_format)
            sheet.write(row, 1, sub['customer_id'])
            sheet.write(row, 2, sub['reference'])
            sheet.write(row, 3, sub['price'])
            row += 1