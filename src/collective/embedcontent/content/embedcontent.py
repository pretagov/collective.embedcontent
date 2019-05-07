# -*- coding: utf-8 -*-
from plone.supermodel import model
from zope import schema
from plone.namedfile.field import NamedBlobFile
from plone.app.textfield import RichText
from zope.schema.interfaces import IVocabularyFactory
from zope.interface import provider
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


items = [ ('index', u'Index HTML')]
terms = [ SimpleTerm(value=pair[0], token=pair[0], title=pair[1]) for pair in items ]
indexFileVocabulary = SimpleVocabulary(terms)

class IEmbedContent(model.Schema):
    """ Interface for EmbedContent
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

    index_file = schema.Choice(
        title=(u'Index file'),
        description=(u'Index file in package content'),
        vocabulary=indexFileVocabulary,
        required=False,
    )


