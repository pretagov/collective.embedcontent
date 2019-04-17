# -*- coding: utf-8 -*-
from plone.dexterity.browser.view import DefaultView
from zope.interface import implements, Interface
from zope.publisher.interfaces import IPublishTraverse
from Products.Five import BrowserView
from BTrees.OOBTree import OOBTree
from plone.app.standardtiles.existingcontent import uuidToObject
from plone.uuid.interfaces import IUUID
from zExceptions import Unauthorized
from plone.tiles.tile import Tile
from plone.app.tiles.browser.edit import DefaultEditView, DefaultEditForm
from plone.app.tiles.browser.add import DefaultAddView, DefaultAddForm
from plone.app.tiles.browser.delete import DefaultDeleteView, DefaultDeleteForm
from plone.dexterity.utils import createContentInContainer
from zope.lifecycleevent import ObjectModifiedEvent, ObjectCreatedEvent
from plone.namedfile.utils import get_contenttype
from plone.app.textfield.value import RichTextValue
from plone.namedfile.file import NamedBlobFile
import zope.event
import urllib

def embedContentPackageUrl(content):
    randomID = getattr(content, 'contentHash', None)
    return '%s/@@contents/%s/%s' % (content.absolute_url(), randomID, content.index_file)

class EmbedContentView(DefaultView):

    def package_url(self):
        return embedContentPackageUrl(self.context)

    def content(self):
        return self

class PublishableString(str):
    """Zope will publish this since it has a __doc__ string"""

    def __init__(self, data):
        self.data = data

    def __str__(self):
        return self.data



class EmbedContentContentView(BrowserView):
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
        for element in path[3:]:
            try:
                zipTree = zipTree[urllib.unquote(element)]
            except Exception:
                return None
        if isinstance(zipTree, OOBTree):
            return self
        request.RESPONSE.setHeader('content-type', zipTree.content_type)
        return PublishableString(zipTree)


class EmbedContentTileEditForm(DefaultEditForm):

    def extractData(self):
        embed_content_id = '%s-%s-EmbedContent' % (self.tileType.__name__, self.tileId)
        embed_content = getattr(self.context, embed_content_id, None)
        if not embed_content:
            embed_content = createContentInContainer(self.context.aq_parent, "EmbedContent", title=embed_content_id)
            setattr(self.context, embed_content_id, embed_content)
        embed_content.html_content = RichTextValue(self.request.get('%s.html_content' % self.tileType.__name__))
        embed_content.index_file = self.request.get('%s.index_file' % self.tileType.__name__)
        if self.request.get('%s.package_content' % self.tileType.__name__):
            package_file = self.request.get('%s.package_content' % self.tileType.__name__)
            package_file.seek(0)
            filename = package_file.filename
            contenttype = get_contenttype(filename=filename)
            data = package_file.read()
            embed_content.package_content = NamedBlobFile(data, contenttype, unicode(filename))
        else:
            action = self.request.get('%s.package_content.action' % self.tileType.__name__)
            if action == 'remove':
                embed_content.package_content = None
        zope.event.notify(ObjectModifiedEvent(embed_content))
        data, errors =  DefaultEditForm.extractData(self)
        # Remove blob from data as it is not supported by tile
        if 'package_content' in data:
            del data['package_content']
        return (data,errors)

    def getContent(self):
        content = DefaultEditForm.getContent(self)
        embed_content_id = '%s-%s-EmbedContent' % (self.tileType.__name__, self.tileId)
        embed_content = getattr(self.context, embed_content_id, None)
        if embed_content:
            content['package_content'] = embed_content.package_content
            content['html_content'] = embed_content.html_content
            content['index_file'] = embed_content.index_file
        return content


class EmbedContentTileEdit(DefaultEditView):
    form = EmbedContentTileEditForm


class EmbedContentTileDeleteForm(DefaultDeleteForm):

    def extractData(self):
        embed_content_id = '%s-%s-EmbedContent' % (self.tileType.__name__, self.tileId)
        embed_content = getattr(self.context, embed_content_id, None)
        if embed_content:
            parent = self.context.aq_parent
            parent.manage_delObjects(embed_content.id)
        data, errors = DefaultDeleteForm.extractData(self)
        # Remove blob from data as it is not supported by tile
        if 'package_content' in data:
            del data['package_content']
        return (data, errors)

class EmbedContentTileDelete(DefaultDeleteView):
    form = EmbedContentTileDeleteForm

class EmbedContentTile(Tile):
    """ A tile for mosaic representing a embed content """

    @property
    def context_content(self):
        embed_content_id = '%s-%s-EmbedContent' % (self.__name__, self.id)
        embed_content = getattr(self.context, embed_content_id, None)
        content = {'package_content':'','html_content':'','index_file':'','package_url':''}
        if embed_content:
            content['package_content'] = embed_content.package_content
            content['html_content'] = embed_content.html_content
            content['index_file'] = embed_content.index_file
            content['package_url'] = embedContentPackageUrl(embed_content)
        return content


