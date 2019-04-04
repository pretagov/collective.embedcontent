# ============================================================================
# DEXTERITY ROBOT TESTS
# ============================================================================
#
# Run this robot test stand-alone:
#
#  $ bin/test -s collective.embedcontent -t test_embed_content.robot --all
#
# Run this robot test with robot server (which is faster):
#
# 1) Start robot server:
#
# $ bin/robot-server --reload-path src collective.embedcontent.testing.COLLECTIVE_EMBEDCONTENT_ACCEPTANCE_TESTING
#
# 2) Run robot tests:
#
# $ bin/robot /src/collective/embedcontent/tests/robot/test_embed_view.robot
#
# See the http://docs.plone.org for further details (search for robot
# framework).
#
# ============================================================================

*** Settings *****************************************************************

Resource  plone/app/robotframework/selenium.robot
Resource  plone/app/robotframework/keywords.robot

Library  Remote  ${PLONE_URL}/RobotRemote

Test Setup  Open test browser
Test Teardown  Close all browsers


*** Test Cases ***************************************************************

Scenario: As a site administrator I can add a EmbedContent
  Given a logged-in site administrator
    and an add EmbedContent form
   When I type 'My EmbedContent' into the title field
    and I submit the form
   Then a EmbedContent with the title 'My EmbedContent' has been created

Scenario: As a site administrator I can view a EmbedContent
  Given a logged-in site administrator
    and a EmbedContent 'My EmbedContent'
   When I go to the EmbedContent view
   Then I can see the EmbedContent title 'My EmbedContent'


*** Keywords *****************************************************************

# --- Given ------------------------------------------------------------------

a logged-in site administrator
  Enable autologin as  Site Administrator

an add EmbedContent form
  Go To  ${PLONE_URL}/++add++EmbedContent

a EmbedContent 'My EmbedContent'
  Create content  type=EmbedContent  id=my-embed_content  title=My EmbedContent

# --- WHEN -------------------------------------------------------------------

I type '${title}' into the title field
  Input Text  name=form.widgets.IBasic.title  ${title}

I submit the form
  Click Button  Save

I go to the EmbedContent view
  Go To  ${PLONE_URL}/my-embed_content
  Wait until page contains  Site Map


# --- THEN -------------------------------------------------------------------

a EmbedContent with the title '${title}' has been created
  Wait until page contains  Site Map
  Page should contain  ${title}
  Page should contain  Item created

I can see the EmbedContent title '${title}'
  Wait until page contains  Site Map
  Page should contain  ${title}
