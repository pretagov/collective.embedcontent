# -*- coding: utf-8 -*-
from plone.dexterity.browser.view import DefaultView
from plone.dexterity.browser.edit import DefaultEditForm
from plone.dexterity.browser.add import DefaultAddForm, DefaultAddView
from z3c.form import interfaces

class EmbedContentView(DefaultView):
    pass


class EmbedContentEditForm(DefaultEditForm):

    def updateWidgets(self):
        super(DefaultEditForm, self).updateWidgets()
        self.widgets['package_signature'].mode = interfaces.HIDDEN_MODE



class EmbedContentAddForm(DefaultAddForm):
    portal_type = 'EmbedContent'

    def update(self):
        DefaultAddForm.update(self)
        import pdb
        pdb.set_trace()

    def updateWidgets(self):
        """ """
        DefaultAddForm.updateWidgets(self)
        import pdb
        pdb.set_trace()



class EmbedContentAddView(DefaultAddView):
    form = EmbedContentAddForm
