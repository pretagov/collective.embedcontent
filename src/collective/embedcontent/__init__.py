# -*- coding: utf-8 -*-
"""Init and utils."""
from zope.i18nmessageid import MessageFactory
from Products.CMFCore.permissions import setDefaultRoles

_ = MessageFactory('collective.embedcontent')
setDefaultRoles('collective.embedcontent: Edit EmbedContent', ('Manager', 'Owner',))
