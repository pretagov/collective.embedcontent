# -*- coding: utf-8 -*-
from plone.dexterity.browser.view import DefaultView
from zope.interface import implements, Interface
from zope.publisher.interfaces import IPublishTraverse
from Products.Five import BrowserView
from BTrees.OOBTree import OOBTree
from z3c.form import form, button
from plone.tiles.tile import Tile
from plone.app.tiles.browser import edit as tileedit
from plone.app.tiles.browser import delete as tiledelete
from plone.dexterity.browser import add as dexterityadd
from plone.dexterity.browser import edit as dexterityedit
from plone.dexterity.utils import createContentInContainer
from plone.app.textfield.value import RichTextValue
from plone.namedfile.file import NamedBlobFile
import urllib
from AccessControl.SecurityInfo import ClassSecurityInfo
from z3c.form import interfaces
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary
from plone.app.blob.field import BlobWrapper
from zipfile import  ZipFile
from plone.namedfile.utils import get_contenttype
from .. import _
import os

def generateUniqueIDForPackageFile(fileObj):
    return str(hash(fileObj))

def getEmbedContentPackageUrl(content):
    randomID = getattr(content, 'contentHash', None)
    return '%s/@@contents/%s/%s' % (content.absolute_url(), randomID, content.index_file)

def getTopLevelFiles(zipTree):
    return [key for key in zipTree.iterkeys() if not isinstance(zipTree[key],OOBTree)]

def guessIndexFile(content):
    top_level_files = getTopLevelFiles(content.zipTree)
    if content.index_file not in top_level_files:
        html_files = [filename for filename in top_level_files if filename.endswith('html') or filename.endswith('htm') ]
        if 'index.html' in html_files:
            content.index_file = 'index.html'
            return
        elif 'index.htm' in html_files:
            content.index_file = 'index.htm'
            return
        elif html_files:
            content.index_file = html_files[0]
        elif top_level_files:
            content.index_file = top_level_files[0]

def extractPackageContent(treeRoot, zip_blob):
    """
        Extract package content into ZOB Tree
    """
    zipfile = ZipFile(zip_blob.open('r'))
    parent_dict = {}
    for path in sorted(zipfile.namelist()):
        if path.endswith('/'):
            # create directory
            path = path[:-1]
            foldername = path.split(os.sep)[-1]
            parent_folder_name = '/'.join(path.split(os.sep)[:-1])
            parent = parent_dict[parent_folder_name] if parent_folder_name in parent_dict else treeRoot
            parent.insert(foldername, OOBTree())
            parent_dict[path] = parent[foldername]
        else:
            # create file
            filename = path.split(os.sep)[-1]
            parent_folder_name = '/'.join(path.split(os.sep)[:-1])
            parent = parent_dict[parent_folder_name] if parent_folder_name in parent_dict else treeRoot
            data = zipfile.read(path)
            blob = BlobWrapper(get_contenttype(filename=filename))
            file_obj = blob.getBlob().open('w')
            file_obj.write(data)
            file_obj.close()
            blob.setFilename(filename)
            parent.insert(filename, blob)

def onContentUpdated(obj):
    if obj.package_content:
        new_hash = generateUniqueIDForPackageFile(obj.package_content)
        old_hash = getattr(obj,'contentHash',None)
        if new_hash == old_hash:
            return
        setattr(obj, 'contentHash', new_hash)
        zipTree = getattr(obj,'zipTree', OOBTree())
        zipTree.clear()
        extractPackageContent(zipTree, obj.package_content)
        setattr(obj, 'zipTree', zipTree)
    else:
        setattr(obj, 'zipTree', OOBTree())
    guessIndexFile(obj)


class EmbedContentAddForm(dexterityadd.DefaultAddForm):
    portal_type = 'EmbedContent'

    def updateWidgets(self):
        dexterityadd.DefaultAddForm.updateWidgets(self)
        self.widgets['index_file'].mode = interfaces.HIDDEN_MODE

    def createAndAdd(self, data):
        obj = dexterityadd.DefaultAddForm.createAndAdd(self,data)
        if obj.package_content:
            content_hash = generateUniqueIDForPackageFile(obj.package_content)
            setattr(obj, 'contentHash', content_hash)
            zipTree = OOBTree()
            extractPackageContent(zipTree, obj.package_content)
            setattr(obj, 'zipTree', zipTree)
            guessIndexFile(obj)
        return obj

class EmbedContentAddView(dexterityadd.DefaultAddView):
    form = EmbedContentAddForm


class EmbedContentEditForm(dexterityedit.DefaultEditForm):

    def updateFields(self):
        dexterityedit.DefaultEditForm.updateFields(self)
        top_level_files  = getTopLevelFiles(self.context.zipTree)
        terms = [SimpleTerm(value=file, token=file, title=file) for file in top_level_files]
        self.fields["index_file"].field.vocabulary = SimpleVocabulary(terms)

    def applyChanges(self, data):
        dexterityedit.DefaultEditForm.applyChanges(self,data)
        onContentUpdated(self.context)

class EmbedContentView(DefaultView):

    def package_url(self):
        return getEmbedContentPackageUrl(self.context)

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

    security = ClassSecurityInfo()

    def __init__(self, context, request):
        self.context = context
        self.request = request


    def __call__(self):
        """ This view has no template yet for non-traversing requests """
        pass

    security.declareProtected('collective.embedcontent.ReadEmbedContent', 'publishTraverse')
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


class EmbedContentTileEditForm(tileedit.DefaultEditForm):

    @button.buttonAndHandler(_('Save'), name='save')
    def handleSave(self, action):
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
        onContentUpdated(embed_content)
        tileedit.DefaultEditForm.handleSave(self,action)

    @button.buttonAndHandler(_(u'Cancel'), name='cancel')
    def handleCancel(self, action):
        tileedit.DefaultEditForm.handleCancel(self,action)

    def extractData(self):
        data, errors =  tileedit.DefaultEditForm.extractData(self)
        # Remove blob from data as it is not supported by tile
        if 'package_content' in data:
            del data['package_content']
        return (data,errors)

    def getContent(self):
        content = tileedit.DefaultEditForm.getContent(self)
        embed_content_id = '%s-%s-EmbedContent' % (self.tileType.__name__, self.tileId)
        embed_content = getattr(self.context, embed_content_id, None)
        if embed_content:
            content['package_content'] = embed_content.package_content
            content['html_content'] = embed_content.html_content
            content['index_file'] = embed_content.index_file
        return content


class EmbedContentTileEdit(tileedit.DefaultEditView):
    form = EmbedContentTileEditForm


class EmbedContentTileDeleteForm(tiledelete.DefaultDeleteForm):

    def extractData(self):
        embed_content_id = '%s-%s-EmbedContent' % (self.tileType.__name__, self.tileId)
        embed_content = getattr(self.context, embed_content_id, None)
        if embed_content:
            parent = self.context.aq_parent
            parent.manage_delObjects(embed_content.id)
        data, errors = tiledelete.DefaultDeleteForm.extractData(self)
        # Remove blob from data as it is not supported by tile
        if 'package_content' in data:
            del data['package_content']
        return (data, errors)

class EmbedContentTileDelete(tiledelete.DefaultDeleteView):
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
            content['package_url'] = getEmbedContentPackageUrl(embed_content)
        return content


