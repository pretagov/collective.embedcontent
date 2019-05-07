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
    >>> memberName = 'userManager'
    >>> portal.portal_membership.addMember(
    ...         memberName,
    ...         memberName,
    ...         ('Member',),
    ...         '',
    ...         {'fullname': 'Site Member', 'email': memberName+'@dummy.fr',}
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
    >>> 'Test HTML Content' in browser.contents
    True
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
    >>> 'http://nohost/plone/testcontent2/@@contents/([-+]?[0-9]+)/pretagov.html' in browser.contents
    True
    >>> browser.getLink('EmbedContent').click()
    >>> browser.getControl('Title').value = 'testcontent2'
    >>> import os
    >>> zip_file = os.path.join(os.path.dirname(__file__), "Plone.zip")
    >>> browser.getControl(name='form.widgets.package_content').add_file(open(zip_file), 'application/zip',  'Plone.zip')
    >>> browser.getControl('Save').click()

Index file is automatically updated

    >>> content = portal['testcontent2']
    >>> content.index_file =='Plone.html'
    True

ZIP content is display in browser

    >>> 'The standard schema fields' in browser.contents
    True

RandomID is included in the iframe source

    >>> randomID1 = content.contentHash
    >>> import re
    >>> match = re.search("http://nohost/plone/testcontent2/@@contents/([-+]?[0-9]+)/Plone.html",browser.contents)
    >>> match != None
    True


Index file listing with top level files
    >>> browser.getLink('Edit').click()
    >>> browser.getControl(name='form.widgets.index_file:list').options == ['Plone.html', 'yet_another.html']
    True

Replace ZIP content

    >>> browser.getLink('Edit').click()
    >>> import os
    >>> zip_file = os.path.join(os.path.dirname(__file__), "pretagov.zip")
    >>> browser.getControl(name='form.widgets.package_content').add_file(open(zip_file), 'application/zip',  'pretagov.zip')
    >>> browser.getControl('Save').click()
    >>> 'PretaGov is an approved supplier' in browser.contents
    True

Index file is automatically updated

    >>> content = portal['testcontent2']
    >>> content.index_file =='pretagov.html'
    True

RandomID is included in the iframe source

    >>> import re
    >>> match = re.search("http://nohost/plone/testcontent2/@@contents/([-+]?[0-9]+)/pretagov.html",browser.contents)
    >>> match != None
    True
    >>> randomID2 = content.contentHash

RandomID change

    >>> randomID1 != randomID2
    True

Adding tile with embed content

    >>> browser.open('{0}/@@add-tile'.format(portal_url))
    >>> browser.getControl(name='tiletype').value = ['collective.embedcontent.tile']
    >>> browser.getControl(name='form.button.Create').click()
    >>> import os
    >>> zip_file = os.path.join(os.path.dirname(__file__), "Plone.zip")
    >>> browser.getControl(name='collective.embedcontent.tile.html_content').value = '<html><head></head><body>Test HTML Content</body></html>'
    >>> browser.getControl(name='collective.embedcontent.tile.package_content').add_file(open(zip_file), 'application/zip',  'Plone.zip')
    >>> browser.getControl('Save').click()

ZIP content is display in tile

    >>> 'The standard schema fields' in browser.contents
    True



Security testing

    >>> from Products.CMFCore.utils import getToolByName
    >>> wf_tool = getToolByName(portal, 'portal_workflow')
    >>> content = portal['testcontent2']
    >>> wf_tool.getInfoFor(content,'review_state')
    'private'
    >>> browser.open(content.absolute_url())
    >>> 'PretaGov is an approved supplier' in browser.contents
    True
    >>> browser.getLink('Log out').click()
    >>> browser.getLink('Log in').click()
    >>> browser.getControl('Login Name').value = 'userManager'
    >>> browser.getControl('Password').value = 'userManager'
    >>> browser.getControl('Log in').click()
    >>> browser.open(content.absolute_url())
    Traceback (most recent call last):
    ...
    Unauthorized: You are not authorized to access this resource.


