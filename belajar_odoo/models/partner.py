from odoo import models, fields, api
import datetime

class ResPartner(models.Model):
    _inherit = "res.partner"
    
    driver = fields.Boolean("Driver")
    born_date = fields.Date("Born Date")
    age = fields.Integer("Age", compute="_compute_age")
    
    _sql_constraints = [('check_born_date', 'check(born_date <= CURRENT_DATE)','Born date must be before today')]
    
    @api.multi
    def _compute_age(self):
        for rec in self:
            born_date = rec.born_date
            if born_date:
                rec.age = (datetime.datetime.now() - datetime.datetime.strptime(born_date,"%Y-%m-%d")).days/365
