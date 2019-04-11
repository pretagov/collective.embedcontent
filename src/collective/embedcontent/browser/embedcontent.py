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
from BTrees.OOBTree import OOBTree

class EmbedContentView(DefaultView):

    def package_url(self):
        return '%s/@@contents/%s' % (self.context.absolute_url(), self.context.index_file)


class PublishableString(str):
    """Zope will publish this since it has a __doc__ string"""

    def __init__(self, data):
        self.data = data

    def __str__(self):
        return self.data



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
        path =  request.URL[len(self.context.absolute_url()):].split('/')
        zipTree = getattr(self.context,'zipTree', None)
        for element in path[2:]:
            try:
                zipTree = zipTree[element]
            except Exception:
                return None
        if isinstance(zipTree, OOBTree):
            return self
        request.RESPONSE.setHeader('content-type', zipTree.content_type)
        return PublishableString(zipTree)

class EmbedContentEditForm(DefaultEditForm):
    pass



class EmbedContentAddForm(DefaultAddForm):
    portal_type = 'EmbedContent'


class EmbedContentAddView(DefaultAddView):
    form = EmbedContentAddForm
