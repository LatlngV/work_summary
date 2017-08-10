# -*- coding: utf-8 -*-

from odoo import api, fields, models


class PatrolProblem(models.Model):
    _name = "latlng.patrol_problem"
    _description = u"巡线软件问题"
    _rec_name = "title"

    title = fields.Char(string=u"标题", required=True)
    create_date = fields.Datetime(string=u"创建日期", default=fields.Datetime.now(), readonly=True)
    fonder = fields.Many2one("res.users", string=u"创建人", default=lambda self: self.env.user, readonly=True)
    problem_count = fields.Integer(string=u"问题数量", compute="_compute_problem_count")
    problem_line = fields.One2many("latlng.problem_detail", "patrol_problem", required=True)

    @api.depends("problem_line")
    def _compute_problem_count(self):
        """
            计算问题数量
        """
        for record in self:
            record.problem_count = len(record.problem_line)

    @api.multi
    def action_print_report(self):
        """
            打印报表
        """
        return self.env["report"].get_action(self, "report_patrol_problem_view")


class ProblemDetail(models.Model):
    _name = "latlng.problem_detail"
    _description = u"问题详情"

    number = fields.Integer(string=u"序号", default=1, required=True)
    name = fields.Char(string=u"问题", required=True)
    detail = fields.Text(string=u"问题详情", required=True)
    complete = fields.Boolean(string=u"是否完成", default=False)
    complete_date = fields.Datetime(string=u"完成时间", compute="_compute_complete_date", stroe=True)
    principal = fields.Char(string=u"负责人", required=True)
    patrol_problem = fields.Many2one("latlng.patrol_problem", string=u"巡线软件问题")

    @api.depends("complete")
    def _compute_complete_date(self):
        """
            计算当前时间日期
        """
        for record in self:
            if record.complete:
                record.complete_date = fields.Datetime.now()

    @api.model
    def create(self, vals):
        problem_id = self.env["latlng.problem_detail"].search([])
        for record in problem_id:
            print record
        return super(ProblemDetail, self).create(vals)
