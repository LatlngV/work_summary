# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class Password(models.TransientModel):
    _name = "latlng.password"
    _description = u"密码"

    password = fields.Char(string=u"密码", required=True)

    @api.multi
    def confirm(self):
        for record in self:
            if len(record.password) < 6:
                return {
                    "warning": {
                        "title": _(u"发生错误"),
                        "message": _(u"密码的长度不能少于 6 位！"),
                    },
                }
            if record.password == "220722":
                return {
                    "type": "ir.actions.act_window",
                    "name": u"巡线软件问题",
                    "res_model": "latlng.patrol_problem",
                    "view_type": "form",
                    "target": "main",
                    "view_mode": "list,form",
                }
            else:
                return {
                    "warning": {
                        "title": _(u"发生错误"),
                        "message": _(u"密码不正确！"),
                    },
                }
