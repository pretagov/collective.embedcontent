# -*- coding: utf-8 -*-

from Products.CMFCore.CMFBTreeFolder import manage_addCMFBTreeFolder
from Products.CMFPlone.interfaces import IHideFromBreadcrumbs
from zope.interface import directlyProvides

from Acquisition import aq_inner
from zope.component import getAdapter
from Products.CMFPlone.interfaces import IUserGroupsSettingsSchema
from plone import api

def afterContentCreated(obj, event):
    #manage_addCMFBTreeFolder(obj, id='plomino_documents')
    #directlyProvides(obj.documents, IHideFromBreadcrumbs)
    #for i in ['resources', 'scripts']:
    #    manage_addCMFBTreeFolder(obj, id=i)
    import pdb
    pdb.set_trace()

def afterContentModified(obj, event):
    """
    """
    import pdb
    pdb.set_trace()

