Integration tests
=================

    >>> browser = get_browser(layer)

HTML embed content
------------------

Add a new EmbedContent with HTML content:

    >>> portal = layer['portal']
    >>> portal_url = portal.absolute_url()
    >>> browser.open(portal_url)
    >>> browser.url
    'http://nohost/plone'
    >>> browser.getLink('EmbedContent').click()
    >>> browser.getControl('Title').value = 'testcontent1'
    >>> browser.getControl('HTML content').value = '<html><head></head><body>Test HTML Content</body></html>'
    >>> browser.getControl('Save').click()

HTML content is display in browser

   >>> 'Test HTML Content' in browser.contents
   True


ZIP embed content
------------------

Add a new EmbedContent with ZIP content:

    >>> portal = layer['portal']
    >>> portal_url = portal.absolute_url()
    >>> browser.open(portal_url)
    >>> browser.url
    'http://nohost/plone'
    >>> browser.getLink('EmbedContent').click()
    >>> browser.getControl('Title').value = 'testcontent2'
    >>> import os
    >>> zip_file = os.path.join(os.path.dirname(__file__), "Plone.zip")
    >>> browser.getControl('Package content').add_file(open(zip_file), 'application/zip',  'Plone.zip')
    >>> browser.getControl('Save').click()

ZIP content is display in browser

   >>> 'The standard schema fields' in browser.contents
   True

Replace ZIP content
