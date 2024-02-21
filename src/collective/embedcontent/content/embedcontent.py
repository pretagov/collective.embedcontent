# -*- coding: utf-8 -*-
from plone.supermodel import model
from zope import schema
from plone.namedfile.field import NamedBlobFile
from plone.app.textfield import RichText
from zope.schema.interfaces import IVocabularyFactory
from zope.interface import provider
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary
# from plone.tiles.directives import ignore_querystring
from zope.interface import Interface

items = [ ('index.html', u'Index HTML')]
terms = [ SimpleTerm(value=pair[0], token=pair[0], title=pair[1]) for pair in items ]
indexFileVocabulary = SimpleVocabulary(terms)

class IEmbedContent(model.Schema):
    """ Interface for EmbedContent
    """

    html_content = schema.SourceText(
        title=(u'Pasted HTML Content'),
        description=(u'Paste your HTML snippet directly to have it appear inside an iframe on your tile.'),
        required=False,
    )

    package_content = NamedBlobFile(
        title=(u'Or Upload HTML Content'),
        description=(u'Upload an HTML file or Zip of HTML (with resources) which will appear in your tile'),
        required=False,
    )

    index_file = schema.Choice(
        title=(u'HTML file to view'),
        description=(u'If your Zip contains more than one HTML file pick which HTML file should be viewed inside your tile'),
        vocabulary=indexFileVocabulary,
        required=False,
    )


class IEmbedContentTile(model.Schema):
    """ Interface for EmbedContent
    """

    html_content = schema.SourceText(
        title=(u'Pasted HTML Content'),
        description=(u'Paste your HTML snippet directly to have it appear inside an iframe on your tile.'),
        required=False,
    )
