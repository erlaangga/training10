from odoo import models, fields, api

class BusMaintain(models.TransientModel):
    _name = "bus.maintain.wizard"
    
    bus_ids = fields.Many2many("transportasi.bus", string="Bus")
    
    @api.model
    def default_get(self, fields):
        res = super(BusMaintain, self).default_get(fields)
        return {
#                 'bus_ids':[[6,False,self.env['transportasi.bus'].search(['|',('state','=','ok'),'|',('state','=','deprecated'),('state','!=','maintenance')]).ids]],
                    'bus_ids':[[6,False,self.env['transportasi.bus'].search(['|',('state','in',('ok','deprecated')),('state','!=','maintenance')]).ids]],
            }
    
    @api.multi
    def act_maintain(self):
        for bus_id in self.bus_ids:
            bus_id.state = 'maintenance'
    
    @api.model
    def create(self, vals):
        
        return super(BusMaintain, self).create(vals)