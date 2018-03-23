from odoo import models, fields, api

class RemovePassenger(models.TransientModel):
    _name = "remove.passenger.wizard"
    
    passenger_ids = fields.Many2many("penumpang.transportasi")
    schedule_id = fields.Many2one('jadwal.bus', string="Schedule")
    
    @api.model
    def default_get(self, fields):
        res = super(RemovePassenger, self).default_get(fields)
        return {
            "schedule_id":self._context['active_id']
            }
    
    @api.multi
    def act_remove(self):
        for rec in self:
            rec.schedule_id.passenger_ids