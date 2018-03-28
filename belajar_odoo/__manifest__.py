# -*- coding: utf-8 -*-
{
    'name' : 'Belajar Odoo',
    'version':'1.0',
    'summary':'Latihan membuat modul',
    'description': """
Modul Belajar Odoo
==================
Ini adalah sebuah modul yang digunakan untuk latihan membuat sebuah modul
    """,
    'author':'Erlangga',
    'website':'https://erlaangga.github.io',
    'depends':['base', 'report', "report_xlsx"],
    'data':[
            'security/transport_security.xml',
            'security/ir.model.access.csv',
            'data/transport_data.xml',
            'report/report_schedule.xml',
            'report/reports.xml',
            'wizard/bus_maintain_wizard.xml',
            'views/transportasi_view.xml',
            'views/partner_view.xml',
            ],
            
}
