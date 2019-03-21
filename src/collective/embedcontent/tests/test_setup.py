# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from collective.embedcontent.testing import COLLECTIVE_EMBEDCONTENT_INTEGRATION_TESTING  # noqa
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID

import unittest


no_get_installer = False


try:
    from Products.CMFPlone.utils import get_installer
except Exception:
    no_get_installer = True


class TestSetup(unittest.TestCase):
    """Test that collective.embedcontent is properly installed."""

    layer = COLLECTIVE_EMBEDCONTENT_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = get_installer(self.portal, self.layer['request'])

    def test_product_installed(self):
        """Test if collective.embedcontent is installed."""
        self.assertTrue(self.installer.is_product_installed(
            'collective.embedcontent'))

    def test_browserlayer(self):
        """Test that ICollectiveEmbedcontentLayer is registered."""
        from collective.embedcontent.interfaces import (
            ICollectiveEmbedcontentLayer)
        from plone.browserlayer import utils
        self.assertIn(
            ICollectiveEmbedcontentLayer,
            utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = COLLECTIVE_EMBEDCONTENT_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.installer = get_installer(self.portal, self.layer['request'])
        roles_before = api.user.get_roles(TEST_USER_ID)
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.installer.uninstall_product('collective.embedcontent')
        setRoles(self.portal, TEST_USER_ID, roles_before)

    def test_product_uninstalled(self):
        """Test if collective.embedcontent is cleanly uninstalled."""
        self.assertFalse(self.installer.is_product_installed(
            'collective.embedcontent'))

    def test_browserlayer_removed(self):
        """Test that ICollectiveEmbedcontentLayer is removed."""
        from collective.embedcontent.interfaces import \
            ICollectiveEmbedcontentLayer
        from plone.browserlayer import utils
        self.assertNotIn(
            ICollectiveEmbedcontentLayer,
            utils.registered_layers())
