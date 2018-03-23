from odoo.addons.report_xlsx.report.report_xlsx import ReportXlsx

class PartnerXlsx(ReportXlsx):

    def generate_xlsx_report(self, workbook, data, models):
        for obj in models:
            report_name = obj.name
            # One sheet by partner
            sheet = workbook.add_worksheet(report_name[:31])
            bold = workbook.add_format({'bold': True})
            sheet.write(0, 0, obj.name, bold)


PartnerXlsx('report.res.partner.xlsx',
            'res.partner')