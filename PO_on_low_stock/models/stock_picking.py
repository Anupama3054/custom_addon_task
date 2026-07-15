from odoo import models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    def button_validate(self):
        res=super().button_validate()
        product=self.move_ids.product_id.product_tmpl_id
        product.auto_purchase()

        return res