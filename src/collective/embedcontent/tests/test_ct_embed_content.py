# -*- coding: utf-8 -*-
from collective.embedcontent.testing import COLLECTIVE_EMBEDCONTENT_INTEGRATION_TESTING  # noqa
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.dexterity.interfaces import IDexterityFTI
from zope.component import createObject
from zope.component import queryUtility

import unittest


try:
    from plone.dexterity.schema import portalTypeToSchemaName
except ImportError:
    # Plone < 5
    from plone.dexterity.utils import portalTypeToSchemaName


class EmbedContentIntegrationTest(unittest.TestCase):

    layer = COLLECTIVE_EMBEDCONTENT_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

    def test_ct_embed_content_schema(self):
        fti = queryUtility(IDexterityFTI, name='EmbedContent')
        schema = fti.lookupSchema()
        schema_name = portalTypeToSchemaName('EmbedContent')
        self.assertEqual(schema_name, schema.getName())

    def test_ct_embed_content_fti(self):
        fti = queryUtility(IDexterityFTI, name='EmbedContent')
        self.assertTrue(fti)

    def test_ct_embed_content_factory(self):
        fti = queryUtility(IDexterityFTI, name='EmbedContent')
        factory = fti.factory
        obj = createObject(factory)


    def test_ct_embed_view_adding(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        obj = api.content.create(
            container=self.portal,
            type='EmbedContent',
            id='embed_view',
        )


    def test_ct_embed_content_globally_addable(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        fti = queryUtility(IDexterityFTI, name='EmbedContent')
        self.assertTrue(
            fti.global_allow,
            u'{0} is not globally addable!'.format(fti.id)
        )

    def test_ct_embed_content_filter_content_type_false(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        fti = queryUtility(IDexterityFTI, name='EmbedContent')
        portal_types = self.portal.portal_types
        parent_id = portal_types.constructContent(
            fti.id,
            self.portal,
            'embed_content_id',
            title='EmbedContent container',
         )
        self.parent = self.portal[parent_id]
        obj = api.content.create(
            container=self.parent,
            type='Document',
            title='My Content',
        )
        self.assertTrue(
            obj,
            u'Cannot add {0} to {1} container!'.format(obj.id, fti.id)
        )
