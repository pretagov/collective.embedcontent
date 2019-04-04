# -*- coding: utf-8 -*-
from plone.dexterity.content import Container
from plone.supermodel import model
from zope import schema
from plone.namedfile.field import NamedBlobFile
from plone.app.textfield import RichText

class IEmbedContent(model.Schema):
    """ Marker interface for EmbedContent
    """
    package_content = NamedBlobFile(
        title=(u'Package Content'),
        description=(u'Package content'),
        required=False,
    )


    htnl_content = RichText(
        title=(u'HTML Content'),
        description=(u'HTML content'),
        required=False,
    )
