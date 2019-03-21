# -*- coding: utf-8 -*-
from plone.dexterity.content import Container
from plone.supermodel import model
from zope import schema
from plone.namedfile.field import NamedFile


class IEmdbedView(model.Schema):
    """ Marker interface for EmdbedView
    """
    zip_file = NamedFile(title=(u'ZIP file'))

    htnl_source = schema.NamedFile(
        title=(u'HTML Package'),
    )
