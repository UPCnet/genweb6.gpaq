# -*- coding: utf-8 -*-
from Products.Five.browser import BrowserView

from plone.dexterity.content import Item
from plone.supermodel import model
from zope import schema
from zope.interface import implementer

from genweb6.core.utils import json_response
from genweb6.gpaq import _
from genweb6.gpaq.api.report import get_embed_params_for_single_report

import json


class IDashboard(model.Schema):

    workspace_id = schema.TextLine(
        title=_(u'WORKSPACE_ID'),
        required=True,
    )

    report_id = schema.TextLine(
        title=_(u"REPORT_ID"),
        required=True,
    )


@implementer(IDashboard)
class Dashboard(Item):

    @property
    def b_icon_expr(self):
        return "bar-chart-fill"


class View(BrowserView):
    pass


class GetEmbedInfo(BrowserView):

    @json_response
    def __call__(self):
        embed = get_embed_params_for_single_report(self.context.workspace_id, self.context.report_id)
        if embed:
            return json.loads(embed)
