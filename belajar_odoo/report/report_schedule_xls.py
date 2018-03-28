from odoo.addons.report_xlsx.report.report_xlsx import ReportXlsx
from docutils.nodes import title

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

class ScheduleXlsx(ReportXlsx):

    def generate_xlsx_report(self, workbook, data, models):
        row = 2
        col = 0

        # Add a bold format to use to highlight cells.
        bold = {'bold': 1}
        border = {'border': 1}
        title_dict = bold
        title_dict.update(border)
        title_dict.update()
        title_format = workbook.add_format(title_dict)
        content_format = workbook.add_format(border)
        bold_format = workbook.add_format(bold)
        # Add a number format for cells with money.
        money_format = workbook.add_format({'num_format': '$#,##0','border': 1})
        # Add an Excel date format.
        date_format = workbook.add_format({'num_format': 'mmmm d yyyy', 'border': 1})
        # Create a format to use in the merged range.
        merge_format = workbook.add_format({
            'bold': 1,
            'align': 'center',
            'valign': 'vcenter',
            'fg_color': 'yellow'})
        
        for obj in models:
            sheet = workbook.add_worksheet(obj.name)
            # merge column
            sheet.merge_range("A1:F1", obj.name, merge_format)
            # Adjust the column width.
            sheet.set_column("A:A", 30)
            # Adjust the row width.
            sheet.set_row(0, 20)
            sheet.set_column(1, 1, 15)
            # Write some data headers.
            sheet.write("A2", "Bus", title_format)
            sheet.write("B2", "Schedule", title_format)
            sheet.write("C2", "Driver", title_format)
            sheet.write("D2", "Departure Time", title_format)
            sheet.write("E2", "Arrival Time", title_format)
            sheet.write("F2", "State", title_format)
            
            sheet.write("A3", obj.bus_id.name, content_format)
            sheet.write("B3", obj.schedule_date, content_format)
            sheet.write("C3", obj.driver_id.name, content_format)
            sheet.write("D3", obj.schedule_date, content_format)
            sheet.write("E3", obj.schedule_date, content_format)
            sheet.write("F3", obj.state, content_format)
             


ScheduleXlsx('report.bus.schedule.xlsx',
            'jadwal.bus')