Integration tests
=================

    >>> import transaction
    >>> browser = get_browser(layer)
    >>> portal = layer['portal']
    >>> memberName = 'siteManager'
    >>> portal.portal_membership.addMember(
    ...         memberName,
    ...         memberName,
    ...         ('Member', 'Manager',),
    ...         '',
    ...         {'fullname': 'Site Manager', 'email': memberName+'@dummy.fr',}
    ...         )
    >>> transaction.commit()

Log in with Site Manager access rights:

    >>> portal_url = portal.absolute_url()
    >>> browser.open(portal_url)
    >>> browser.getLink('Log in').click()
    >>> browser.getControl('Login Name').value = 'siteManager'
    >>> browser.getControl('Password').value = 'siteManager'
    >>> browser.getControl('Log in').click()

HTML embed content
------------------

Add a new EmbedContent with HTML content:

    >>> portal_url = portal.absolute_url()
    >>> browser.open(portal_url)
    >>> browser.getLink('EmbedContent').click()
    >>> browser.getControl('Title').value = 'testcontent1'
    >>> browser.getControl(name='form.widgets.html_content').value = '<html><head></head><body>Test HTML Content</body></html>'
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
    >>> browser.getControl(name='form.widgets.package_content').add_file(open(zip_file), 'application/zip',  'Plone.zip')
    >>> browser.getControl(name='form.widgets.index_file').value = 'Plone.html'
    >>> browser.getControl('Save').click()

ZIP content is display in browser

    >>> 'The standard schema fields' in browser.contents
    True

RandomID is included in the iframe source

    >>> import re
    >>> match = re.search("http://nohost/plone/testcontent2/@@contents/([-+]?[0-9]+)/Plone.html",browser.contents)
    >>> match != None
    True
    >>> randomID1 = match.groups()[0]

Replace ZIP content

    >>> browser.getLink('Edit').click()
    >>> import os
    >>> zip_file = os.path.join(os.path.dirname(__file__), "pretagov.zip")
    >>> browser.getControl(name='form.widgets.package_content').add_file(open(zip_file), 'application/zip',  'pretagov.zip')
    >>> browser.getControl(name='form.widgets.index_file').value = 'pretagov.html'
    >>> browser.getControl('Save').click()
    >>> 'PretaGov is an approved supplier' in browser.contents
    True

RandomID is included in the iframe source

    >>> import re
    >>> match = re.search("http://nohost/plone/testcontent2/@@contents/([-+]?[0-9]+)/pretagov.html",browser.contents)
    >>> match != None
    True
    >>> randomID2 = match.groups()[0]

RandomID change
    >>> randomID1 != randomID2
    True
