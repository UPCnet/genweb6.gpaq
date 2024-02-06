# -*- coding: utf-8 -*-
from Products.Five.browser import BrowserView

from plone.dexterity.content import Item
from plone.dexterity.interfaces import IDexteritySchema
from plone.supermodel import model
from plone.supermodel import model
from zope import schema
from zope.interface import implementer

from genweb6.core.utils import json_response
from genweb6.gpaq import _
from genweb6.gpaq.api.report import get_embed_params_for_single_report

import json


class IDashboard(model.Schema, IDexteritySchema):

    workspace_id = schema.TextLine(
        title=_(u'WORKSPACE_ID'),
        required=True,
    )

    report_id = schema.TextLine(
        title=_(u"REPORT_ID"),
        required=True,
    )

    model.fieldset('Filtres',
                   label=_(u'Filtres opcionals'),
                   description=_(u'Tant el nom de la pàgina, els filtres i els valors han de ser escrits exactament com apareixen en el report de Power BI.'),
                   fields=['filter_page',
                           'filter_search_key_1', 'filter_search_value_1',
                           'filter_search_key_2', 'filter_search_value_2'])

    filter_page = schema.TextLine(
        title=_(u"Pàgina"),
        description=_(u"Omplir amb el nom d'una pestanya en cas es requereixi que el report s'obri per defecte en aquesta pàgina."),
        required=False,
    )

    filter_search_key_1 = schema.TextLine(
        title=_(u"Filtre"),
        description=_(u"Omplir amb el nom de l'objecte visual a filtrar (slicer)."),
        required=False,
    )

    filter_search_value_1 = schema.TextLine(
        title=_(u"Valors"),
        description=_(u"Incloure el valor a filtrar, si són varis han d'anar separats per comes."),
        required=False,
    )

    filter_search_key_2 = schema.TextLine(
        title=_(u"Filtre"),
        description=_(u"Omplir amb el nom de l'objecte visual a filtrar (slicer)."),
        required=False,
    )

    filter_search_value_2 = schema.TextLine(
        title=_(u"Valors"),
        description=_(u"Incloure el valor a filtrar, si són varis han d'anar separats per comes."),
        required=False,
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
            return {'embed': json.loads(embed),
                    'filters': {
                        'page': self.context.filter_page,
                        'search_key_1': self.context.filter_search_key_1,
                        'search_value_1': self.context.filter_search_value_1.split(',') if self.context.filter_search_value_1 else [],
                        'search_key_2': self.context.filter_search_key_2,
                        'search_value_2': self.context.filter_search_value_2.split(',') if self.context.filter_search_value_2 else [],
                    }}
