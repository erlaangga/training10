# -*- coding: utf-8 -*
from odoo import models, fields, api
import datetime
from openid import store

class Penumpang(models.Model):
    _name = "penumpang.transportasi"
    
    name = fields.Char("Name",size=32, help="Passenger's name")
    born_date = fields.Date('Born Date')
    weight = fields.Float("Weight")
    height = fields.Float("Height")
    state = fields.Selection([('general','General'),('member','Member')], 'State', default="general")
    id_number = fields.Char("ID Number", size=32, required=1)
    schedule_ids = fields.Many2many("jadwal.bus", string="Bus Schedule", copy=False)
    age = fields.Integer("Age", compute="_compute_age")
    
    @api.depends("born_date")
    def _compute_age(self):
        for rec in self:
            born_date = rec.born_date
            if born_date:
                rec.age = (datetime.datetime.now() - datetime.datetime.strptime(born_date,"%Y-%m-%d")).days/365
        
class Bus(models.Model):
    _name = "transportasi.bus"
    
    name = fields.Char("Name",size=24, help="Bus' name")
    code = fields.Char("Code",size=12, help="Bus' code", required=True)
    capacity = fields.Integer("Capacity", help="Seat or accomodation capability")
    image = fields.Binary("Image")
    price = fields.Float("Price")
    state = fields.Selection([('ok','OK'),('maintenance','Maintenance'),('deprecated','Deprecated')], "Bus Status", default="ok")
    schedule_line = fields.One2many("jadwal.bus", "bus_id", "Bus")
    
class Jadwal(models.Model):
    _name = "jadwal.bus"
    
    name = fields.Char("Name", help="Schedule Name", default="New", readonly=True)
    schedule_time = fields.Datetime("Schedule Time", required=True)
    bus_id = fields.Many2one("transportasi.bus","Bus", required=True)
    departure_time = fields.Datetime("Departure Time")
    arrival_time = fields.Datetime("Arrival Time")
    driver_id = fields.Many2one("res.partner", "Driver", help="Driver of the bus")
    passenger_line = fields.Many2many("penumpang.transportasi", string="Passengers")
    passenger_count = fields.Integer("Passengers", compute="_compute_passenger")
    income = fields.Float("Income", compute="_compute_money", store=True)
    sub_total = fields.Float("Sub Total", compute="_compute_money", store=True)
    price = fields.Float("Price")
    expense = fields.Float("Expense")
    state = fields.Selection([('draft','Draft'),('ok','OK'),('delay','Delay'),('done','Done'),('cancel','Cancelled')], "State", default="draft")
    note = fields.Text("Note")
    
    @api.multi
    def _compute_passenger(self):
        for rec in self:
            rec.passenger_count = len(rec.passenger_line)
    
    @api.depends("price","passenger_line")
    def _compute_money(self):
        for rec in self:
            passenger_count = len(rec.passenger_line)
            if passenger_count > 0:
                income = passenger_count * rec.price
                rec.income = income
                rec.sub_total_income = income - rec.expense
    
    @api.onchange("bus_id")
    def onchange_bus(self):
        self.price = self.bus_id.price
    
    @api.multi
    def act_run(self):
        if self.departure_time and self.schedule_time:
            deltime = datetime.datetime.strptime(self.departure_time,"%Y-%m-%d %H:%M:%S") - datetime.datetime.strptime(self.schedule_time,"%Y-%m-%d %H:%M:%S")
            if deltime.total_seconds() > 600:
                self.state = 'delay'
            else:
                self.state = 'ok'
        
    @api.multi
    def act_done(self):
        self.state = 'done'
    
    @api.multi
    def act_cancel(self):
        self.state = 'cancel'
        
    @api.model
    def create(self, vals):
        vals.update({'name':self.env['ir.sequence'].next_by_code("sequence.bus.schedule")})
        return super(Jadwal, self).create(vals)
    
    @api.multi
    def print_excel(self):
        datas = {}
        datas.update({'bus':self.bus_id.name, 'schedule_time':self.schedule_time, 'departure_time':self.departure_time, 'arrival_time':self.arrival_time, 'company_id':self.env.user.company_id.name})
        return {
                'type': 'ir.actions.report.xml',
                'report_name': 'report_schedule_xls',
                'context': {u'lang': u'id_ID', u'tz': u'Asia/Jakarta', "company_id":self.env.user.company_id.name},
                'nodestroy': True,
                'datas': datas,
                'data':datas,
            }
    
    @api.multi
    def print_pdf(self):
        return self.env['report'].get_action(self, "belajar_odoo.report_schedule_document")
        