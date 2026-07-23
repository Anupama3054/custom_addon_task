# -*- coding: utf-8 -*-
from odoo import models, api,tools


class IrUiMenu(models.Model):
    _inherit = 'ir.ui.menu'

    # @api.model
    # def _visible_menu_ids(self, debug=False):
    #     visible_menu_ids = super()._visible_menu_ids(debug)
    #     print(visible_menu_ids)
    #
    #     restricted_menus = self.env.user.hidden_menu_ids.ids
    #     print(restricted_menus)
    #
    #     visible_menu_ids = visible_menu_ids-set(restricted_menus)
    #     print(visible_menu_ids)
    #
    #     return visible_menu_ids
    @api.model
    @tools.ormcache('self.env.uid', 'debug', 'self.env.lang',
                    'self.env.user.hidden_menu_ids')
    def load_menus(self, debug):
        res=super().load_menus(debug)
        print(333333333, res)
        return res


    def _filter_visible_menus(self):
        visible_menu_ids = super()._filter_visible_menus()
        print(visible_menu_ids.ids)

        restricted_menus = self.env.user.hidden_menu_ids
        print(restricted_menus)
        print( restricted_menus)
        print( visible_menu_ids.ids)
        visible_menu_ids = visible_menu_ids-restricted_menus

        return visible_menu_ids
