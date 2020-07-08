.. This README is meant for consumption by humans and pypi. Pypi can render rst files so please do not use Sphinx features.
   If you want to learn more about writing documentation, please check out: http://docs.plone.org/about/documentation_styleguide.html
   This text does not appear on pypi or github. It is a comment.

=======================
collective.embedcontent
=======================

Collective.embedcontent provides a way to install a zip or single html file of content into a plone site. 

Features
--------

- Content is displayed inside an iframe in a content view or in a mosaic tile.
- The iframe will dymaically resize vertically to fit the loaded content to avoid scroll bars.
- Content is not filtered like pasted html in the visual editor. This allows for
  - subsites authored by other tools such newsletter software. Linked html works but need to be relative.
  - social media JS embed codes

Notes
-----
- Note this does increase the likelyhood of harmful JS code existing on your site
  so be aware of who is allowed access to add embeded content.
- It doesn't currently have a way to just display part of the html content. You will need to ensure
  it is designed just display "content" and doesn't have its own headers and footers.
- Since its an iframe any content must use its own css. This can also lead to content that doesn't
  fit the site theme.

Examples
--------

This add-on can be seen in action at the following sites:
- https://www.mhcs.health.nsw.gov.au (frontpage twitter and facebook tiles and under Media > Newsletters)



Installation
------------

Install collective.embedcontent by adding it to your buildout::

    [buildout]

    ...

    eggs =
        collective.embedcontent


and then running ``bin/buildout``

Once installed and activated on your site there is an EmbedContent content type you can add anywhere in your site.


Contribute
----------

- Issue Tracker: https://github.com/collective/collective.embedcontent/issues
- Source Code: https://github.com/collective/collective.embedcontent


License
-------

The project is licensed under the GPLv2.
