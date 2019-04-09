# -*- coding: utf-8 -*-
from plone.dexterity.browser.view import DefaultView
from plone.dexterity.browser.edit import DefaultEditForm
from plone.dexterity.browser.add import DefaultAddForm, DefaultAddView
from z3c.form import interfaces
from zope.interface import implements, Interface
from zope.publisher.interfaces import IPublishTraverse
from zope import component
from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName

class EmbedContentView(DefaultView):

    def package_url(self):
        return '%s/@@contents/%s' % (self.context.absolute_url(), self.context.index_file)


class EmbedContentContentView(DefaultView):
    """ @@contents browser view to access zipfile's contents
        """
    implements(IPublishTraverse)

    def __init__(self, context, request):
        self.context = context
        self.request = request


    def __call__(self):
        """ This view has no template yet for non-traversing requests """
        pass

    def publishTraverse(self, request, name):
        path = name.split('/')
        obj = getattr(self.context, self.context.package_signature)
        for element in path:
            try:
                obj = obj[element]
            except Exception:
                return None
        return obj

class EmbedContentEditForm(DefaultEditForm):

    def updateWidgets(self):
        super(DefaultEditForm, self).updateWidgets()
        self.widgets['package_signature'].mode = interfaces.HIDDEN_MODE



class EmbedContentAddForm(DefaultAddForm):
    portal_type = 'EmbedContent'

    def update(self):
        DefaultAddForm.update(self)

    def updateWidgets(self):
        """ """
        DefaultAddForm.updateWidgets(self)




class EmbedContentAddView(DefaultAddView):
    form = EmbedContentAddForm
