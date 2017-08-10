# -*- coding: utf-8 -*-

from odoo import api, fields, models
from datetime import datetime
import time


class WorkLog(models.Model):
    _name = "latlng.work_log"
    _description = u"工作日志"
    _rec_name = "title"

    title = fields.Char(string=u"标题", required=True)
    start_date = fields.Date(string=u"开始日期", required=True)
    end_date = fields.Date(string=u"结束日期", required=True)
    total_day = fields.Integer(string=u"工时(天数)", compute="_compute_total_day", store=True)

    @api.depends("start_date", "end_date")
    def _compute_total_day(self):
        for record in self:
            if record.start_date and record.end_date:
                end = datetime.strptime(record.end_date, "%Y-%m-%d")
                start = datetime.strptime(record.start_date, "%Y-%m-%d")
                time_stamp = (int(time.mktime(end.timetuple())) - int(time.mktime(start.timetuple()))) + 24 * 60 * 60
                record.total_day = time_stamp / 24 / 60 / 60

    @api.constrains("start_date", "end_date")
    def _constraint_date(self):
        for record in self:
            end = datetime.strptime(record.end_date, "%Y-%m-%d")
            start = datetime.strptime(record.start_date, "%Y-%m-%d")
            if int(time.mktime(end.timetuple())) <= int(time.mktime(start.timetuple())):
                raise ValueError(u"结束日期不能小于开始日期！")
