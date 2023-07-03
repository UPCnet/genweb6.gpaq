# -*- coding: utf-8 -*-
from Products.statusmessages.interfaces import IStatusMessage

from plone.app.registry.browser import controlpanel
from plone.supermodel import model
from z3c.form import button
from zope import schema
from zope.ramcache import ram

from genweb6.gpaq import _


class IGpaqSettings(model.Schema):

    tenant_id = schema.TextLine(
        title=_(u'TENANT_ID'),
        required=False,
    )

    client_id = schema.TextLine(
        title=_(u'CLIENT_ID'),
        required=False,
    )

    client_secret = schema.TextLine(
        title=_(u'CLIENT_SECRET'),
        required=False,
    )


class GpaqSettingsEditForm(controlpanel.RegistryEditForm):

    schema = IGpaqSettings
    label = _(u'Gpaq settings')

    def updateFields(self):
        super(GpaqSettingsEditForm, self).updateFields()

    def updateWidgets(self):
        super(GpaqSettingsEditForm, self).updateWidgets()

    @button.buttonAndHandler(_('Save'), name='save')
    def handleSave(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return

        ram.caches.clear()
        self.applyChanges(data)

        IStatusMessage(self.request).addStatusMessage(_("Changes saved"), "info")
        self.request.response.redirect(self.request.getURL())

    @button.buttonAndHandler(_("Cancel"), name='cancel')
    def handleCancel(self, action):
        IStatusMessage(self.request).addStatusMessage(_("Changes canceled."), "info")
        self.request.response.redirect(self.context.absolute_url() + '/' + self.control_panel_view)


class GpaqSettingsControlPanel(controlpanel.ControlPanelFormWrapper):
    form = GpaqSettingsEditForm
