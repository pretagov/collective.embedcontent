# -*- coding: utf-8 -*-
from plone.dexterity.content import Container
from plone.supermodel import model
from zope import schema
from plone.namedfile.field import NamedBlobFile
from plone.app.textfield import RichText
from z3c.form.interfaces import IObjectFactory
from z3c.form.object import FactoryAdapter, getIfName
from zope.component import queryUtility
from plone.app.vocabularies.catalog import CatalogSource
from zope.component.interfaces import IFactory, implements
import zope.component

class IEmbedContent(model.Schema):
    """ Marker interface for EmbedContent
    """

    html_content = RichText(
        title=(u'HTML Content'),
        description=(u'HTML content'),
        required=False,
    )

    package_content = NamedBlobFile(
        title=(u'Package Content'),
        description=(u'Package content'),
        required=False,
    )

    index_file = schema.TextLine(
        title=(u'Index file'),
        description=(u'Index file in package content'),
        default=(u'index.html'),
        required=False,
    )

