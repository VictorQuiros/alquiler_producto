from odoo import models, fields, api
from datetime import timedelta

class AlquilerProducto(models.Model):
    _name = 'alquiler.producto'
    _description = 'Gestión de Alquiler de Productos'
    
    customer_id = fields.Many2one(
        'res.partner',
        string='Cliente',
        required=True
    )
    
    product_id = fields.Many2one(
        'product.product',
        string='Producto',
        required=True
    )
    
    start_date = fields.Date(
        string='Fecha de Inicio',
        required=True
    )
    
    end_date = fields.Date(
        string='Fecha de Fin',
        compute='_compute_end_date',
        store=True
    )
    
    status = fields.Selection(
        [('rented', 'En alquiler'), ('returned', 'Entregado'), ('not_returned', 'No entregado')],
        string='Estado',
        compute='_compute_status',
        store=True,
        default='rented'
    )
    
    notes = fields.Text(
        string='Observaciones'
    )

    @api.onchange('product_id')
    def _onchange_product_id(self):
        if self.product_id and self.product_id.qty_available <= 0:
            self.product_id = False
            return {
                'warning': {
                    'title': "Producto no disponible",
                    'message': "El producto seleccionado no está disponible para alquiler."
                }
            }

    @api.depends('start_date')
    def _compute_end_date(self):
        for record in self:
            if record.start_date:
                record.end_date = record.start_date + timedelta(days=30)
            else:
                record.end_date = False

    @api.depends('end_date')
    def _compute_status(self):
        for record in self:
            if record.end_date and record.end_date < fields.Date.today() and record.status == 'rented':
                record.status = 'not_returned'

# Asignar permisos de acceso basados en roles de usuario
class AlquilerProductoAccess(models.Model):
    _inherit = 'res.users'

    def _get_groups(self):
        res = super(AlquilerProductoAccess, self)._get_groups()
        group_sales = self.env.ref('sales_team.group_sale_salesman')
        if group_sales in self.groups_id:
            res.append(('edit', 'alquiler.producto'))
        else:
            res.append(('read_only', 'alquiler.producto'))
        return res

# Definir un cron job para actualizar el estado de los préstamos
class AlquilerProductoCron(models.Model):
    _name = 'alquiler.producto.cron'

    @api.model
    def _update_status(self):
        records = self.env['alquiler.producto'].search([('status', '=', 'rented')])
        for record in records:
            record._compute_status()
