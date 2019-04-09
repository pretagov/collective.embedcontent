# -*- coding: utf-8 -*-
"""Module where all interfaces, events and exceptions live."""
from zope import interface
from zope.publisher.interfaces.browser import IDefaultBrowserLayer


class ICollectiveEmbedcontentLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""
