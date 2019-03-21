# ============================================================================
# DEXTERITY ROBOT TESTS
# ============================================================================
#
# Run this robot test stand-alone:
#
#  $ bin/test -s collective.embedcontent -t test_emdbed_view.robot --all
#
# Run this robot test with robot server (which is faster):
#
# 1) Start robot server:
#
# $ bin/robot-server --reload-path src collective.embedcontent.testing.COLLECTIVE_EMBEDCONTENT_ACCEPTANCE_TESTING
#
# 2) Run robot tests:
#
# $ bin/robot /src/collective/embedcontent/tests/robot/test_emdbed_view.robot
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

Scenario: As a site administrator I can add a Emdbed View
  Given a logged-in site administrator
    and an add Emdbed View form
   When I type 'My Emdbed View' into the title field
    and I submit the form
   Then a Emdbed View with the title 'My Emdbed View' has been created

Scenario: As a site administrator I can view a Emdbed View
  Given a logged-in site administrator
    and a Emdbed View 'My Emdbed View'
   When I go to the Emdbed View view
   Then I can see the Emdbed View title 'My Emdbed View'


*** Keywords *****************************************************************

# --- Given ------------------------------------------------------------------

a logged-in site administrator
  Enable autologin as  Site Administrator

an add Emdbed View form
  Go To  ${PLONE_URL}/++add++Emdbed View

a Emdbed View 'My Emdbed View'
  Create content  type=Emdbed View  id=my-emdbed_view  title=My Emdbed View

# --- WHEN -------------------------------------------------------------------

I type '${title}' into the title field
  Input Text  name=form.widgets.IBasic.title  ${title}

I submit the form
  Click Button  Save

I go to the Emdbed View view
  Go To  ${PLONE_URL}/my-emdbed_view
  Wait until page contains  Site Map


# --- THEN -------------------------------------------------------------------

a Emdbed View with the title '${title}' has been created
  Wait until page contains  Site Map
  Page should contain  ${title}
  Page should contain  Item created

I can see the Emdbed View title '${title}'
  Wait until page contains  Site Map
  Page should contain  ${title}
