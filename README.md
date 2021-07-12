# Tutorial aqa-core (Gherkin)


## Installation
> https://pypi.org/project/aqa-core/


## Feature Testing Setup
### Feature Testing Layout
#### aqa-core works with three types of files:
1. feature files written by your Business Analyst / Sponsor / whoever with your behaviour scenarios in it, and
2. a “steps” directory with Python step implementations for the scenarios.
3. optionally some environmental controls (code to run before and after steps, scenarios, features or the whole shooting match).

#### These files are typically stored in a directory called “features”. The minimum requirement for a features directory is:
- features/
- features/everything.feature
- features/steps/
- features/steps/steps.py

#### A more complex directory might look like:
- features/
- features/signup.feature
- features/login.feature
- features/account_details.feature
- features/environment.py
- features/steps/
- features/steps/website.py
- features/steps/utils.py


## Features
#### Features are composed of scenarios. They may optionally have a description, a background and a set of tags. In its simplest form a feature looks like:
```Feature
Feature: feature name

  Scenario: some scenario
      Given some condition
       Then some result is expected.
```

#### In all its glory it could look like:
```Feature
@tags @tag
Feature: feature name
  description
  further description

  Background: some requirement of this test
    Given some setup condition
      And some other setup action

  Scenario: some scenario
      Given some condition
       When some action is taken
       Then some result is expected.

  Scenario: some other scenario
      Given some other condition
       When some action is taken
       Then some other result is expected.

  Scenario: ...
```

#### The feature name should just be some reasonably descriptive title for the feature being tested, like “the message posting interface”. The following description is optional and serves to clarify any potential confusion or scope issue in the feature name. The description is for the benefit of humans reading the feature text.
#### The Background part and the Scenarios will be discussed in the following sections.


## Steps
#### Steps take a line each and begin with a keyword - one of “given”, “when”, “then”, “and” or “but”.
#### In a formal sense the keywords are all Title Case, though some languages allow all-lowercase keywords where that makes sense.
#### Steps should not need to contain significant degree of detail about the mechanics of testing; that is, instead of:
```Step
Given a browser client is used to load the URL "http://website.example/website/home.html"
```

#### the step could instead simply say:
```Step
Given we are looking at the home page
```
#### Steps are implemented using Python code which is implemented in the “steps” directory in Python modules (files with Python code which are named “name.py”.) The naming of the Python modules does not matter. All modules in the “steps” directory will be imported by aqa-core at startup to discover the step implementations.


### Given, When, Then (And, But)
#### aqa-core doesn’t technically distinguish between the various kinds of steps. However, we strongly recommend that you do! These words have been carefully selected for their purpose, and you should know what the purpose is to get into the BDD mindset.


### Given
#### The purpose of givens is to put the system in a known state before the user (or external system) starts interacting with the system (in the When steps). Avoid talking about user interaction in givens. If you had worked with usecases, you would call this preconditions.

#### Examples:
- Create records (model instances) / set up the database state.
- It’s ok to call directly into your application model here.
- Log in a user (An exception to the no-interaction recommendation. Things that “happened earlier” are ok).

#### You might also use Given with a multiline table argument to set up database records instead of fixtures hard-coded in steps. This way you can read the scenario and make sense out of it without having to look elsewhere (at the fixtures).


### When
#### Each of these steps should describe the key action the user (or external system) performs. This is the interaction with your system which should (or perhaps should not) cause some state to change.

#### Examples:
- Interact with a web page (Requests/Twill/Selenium interaction etc should mostly go into When steps).
- Interact with some other user interface element.
- Developing a library? Kicking off some kind of action that has an observable effect somewhere else.


### Then
#### Here we observe outcomes. The observations should be related to the business value/benefit in your feature description. The observations should also be on some kind of output - that is something that comes out of the system (report, user interface, message) and not something that is deeply buried inside it (that has no business value).

#### Examples:
- Verify that something related to the Given+When is (or is not) in the output
- Check that some external system has received the expected message (was an email with specific content sent?)

#### While it might be tempting to implement Then steps to just look in the database - resist the temptation. You should only verify outcome that is observable for the user (or external system) and databases usually are not.


### And, But
#### If you have several givens, whens or thens you could write:
```Example
Scenario: Multiple Givens
  Given one thing
  Given an other thing
  Given yet an other thing
   When I open my eyes
   Then I see something
   Then I don't see something else
```

#### Or you can make it read more fluently by writing:
```Example
Scenario: Multiple Givens
  Given one thing
    And an other thing
    And yet an other thing
   When I open my eyes
   Then I see something
    But I don't see something else
```

#### The two scenarios are identical to aqa-core - steps beginning with “and” or “but” are exactly the same kind of steps as all the others. They simply mimic the step that preceeds them.


## Environmental Controls
#### The environment.py module may define code to run before and after certain events during your testing:
```Example
before_step(context, step), after_step(context, step)
    These run before and after every step.
    
before_scenario(context, scenario), after_scenario(context, scenario)
    These run before and after each scenario is run.
    
before_feature(context, feature), after_feature(context, feature)
    These run before and after each feature file is exercised.
    
before_tag(context, tag), after_tag(context, tag)
    These run before and after a section tagged with the given name. 
    They are invoked for each tag encountered in the order they’re found 
    in the feature file. See controlling things with tags.
    
before_all(context), after_all(context)
    These run before and after the whole shooting match.
```

#### The feature, scenario and step objects represent the information parsed from the feature file. They have a number of attributes:
```Example
keyword
    “Feature”, “Scenario”, “Given”, etc.
name
    The name of the step (the text after the keyword.)
tags
    A list of the tags attached to the section or step. See controlling things with tags.
filename and line
    The file name (or “<string>”) and line number of the statement.
```

#### A common use-case for environmental controls might be to set up a web server and browser to run all your tests in. For example:
```Example
# -- FILE: features/environment.py
from behave import fixture, use_fixture
from behave4my_project.fixtures import wsgi_server
from selenium import webdriver

@fixture
def selenium_browser_chrome(context):
    # -- HINT: @behave.fixture is similar to @contextlib.contextmanager
    context.browser = webdriver.Chrome()
    yield context.browser
    # -- CLEANUP-FIXTURE PART:
    context.browser.quit()

def before_all(context):
    use_fixture(wsgi_server, context, port=8000)
    use_fixture(selenium_browser_chrome, context)
    # -- HINT: CLEANUP-FIXTURE is performed after after_all() hook is called.

def before_feature(context, feature):
    model.init(environment='test')
```

```Example
# -- FILE: behave4my_project/fixtures.py
# ALTERNATIVE: Place fixture in "features/environment.py" (but reuse is harder)
from behave import fixture
import threading
from wsgiref import simple_server
from my_application import model
from my_application import web_app

@fixture
def wsgi_server(context, port=8000):
    context.server = simple_server.WSGIServer(('', port))
    context.server.set_app(web_app.main(environment='test'))
    context.thread = threading.Thread(target=context.server.serve_forever)
    context.thread.start()
    yield context.server
    # -- CLEANUP-FIXTURE PART:
    context.server.shutdown()
    context.thread.join()
```

#### Of course, if you wish, you could have a new browser for each feature, or to retain the database state between features or even initialise the database for each scenario.


# Example project with aqa-core package
## 1. Directory
```Example
|project_directory/
|...resources/
|......LOCATORS.json - Contains information about pages and their elements
|......Chrome.json - Contains information about Chrome browser (necessary for setup driver)
|......Galaxy_A71.json - Contains information about Android device (necessary for setup driver)
|......iPhone_Xr_Black.json - Contains information about iOS device (necessary for setup driver)
|...scripts/
|......iOS.sh - simple script to run iOS test cases
|......Android.sh - simple script to run Android test cases
|......Web.sh - simple script to run Web test cases
|...features/
|.......steps/
|...........signup.py
|...........login.py
|.......signup.feature
|.......login.feature
|.......environment.py
```

## 2. LOCATORS.json
```Example
{
  "pages": [
    {
      "pageName": "Start page",
      "pageDescription": "After We install and open Application, We navigate to Start Page",
      "pageLocators": [
        {
          "locatorName": "Sign Up button",
          "locatorDescription": "Sign Up button on Start page",
          "checkOpeningPage": true,
          "Web": { "locatorBy": "xpath", "locatorValue": "//button/span/h6[text()=\"Sign Up\"]", "locatorDynamic": false },
          "Android": { "locatorBy": "xpath", "locatorValue": "//android.view.ViewGroup[@content-desc=\"signUp\"]", "locatorDynamic": false },
          "iOS": { "locatorBy": "xpath", "locatorValue": "//XCUIElementTypeOther[@name=\"signUp\"]", "locatorDynamic": false }
        },
        {
          "locatorName": "Log In button",
          "locatorDescription": "Log In button on Start page",
          "checkOpeningPage": true,
          "Web": { "locatorBy": "xpath", "locatorValue": "//button/span/h6[text()=\"Log In\"]", "locatorDynamic": false },
          "Android": { "locatorBy": "xpath", "locatorValue": "//android.view.ViewGroup[@content-desc=\"login\"]", "locatorDynamic": false },
          "iOS": { "locatorBy": "xpath", "locatorValue": "//XCUIElementTypeOther[@name=\"login\"]", "locatorDynamic": false }
        }
      ]
    }
  ]
}
```

## 3. Chrome.json
```Example
{
    "platformName": "Web",
    "url": "https://qa.example.app/",
    "fullScreen": true,
    "browserName": "Chrome",
    "width": "1024",
    "height": "768", 
}
```

## 4. Galaxy_A71.json
```Example
{
  "platformName": "Android",
  "udid": "RZ8R202R3JM",
  "appWaitActivity": "*",
  "appPackage": "com.example.qa",
  "deviceName": "SM-A715F",
  "platformVersion": "10",
  "app": "Absolute Path/test.apk",
  "noReset": true,
  "fullReset": false,
  "appium": "http://localhost:4723/wd/hub",
  "url": "https://qa.example.app/"
}
```

## 5. iPhone_Xr_Black.json
```Example
{
  "deviceName": "Ivan's iPhone",
  "platformName": "iOS",
  "platformVersion": "14.3",
  "udid": "00008020-000E5CAC3E8A402E",
  "automationName": "XCUITest",
  "app": "com.qa.example",
  "noReset": true,
  "fullReset": false,
  "appium": "http://localhost:4723/wd/hub",
  "url": "https://qa.example.app/"
}
```

## 6. iOS.sh
```Example
#!/bin/sh
export platformParams="resources/iPhone_Xr_Black.json"
rm -rf ios_allure_result
behave --no-capture -f allure_behave.formatter:AllureFormatter -o ios_allure_result features/
unset platformParams
allure serve ios_allure_result
```

## 7. Android.sh
```Example
#!/bin/sh
export platformParams="resources/Galaxy_A71.json"
rm -rf android_allure_result
behave --no-capture -f allure_behave.formatter:AllureFormatter -o android_allure_result features/
unset platformParams
allure serve android_allure_result
```

## 8. Web.sh
```Example
#!/bin/sh
export platformParams="resources/Chrome.json"
rm -rf web_allure_result
behave --no-capture -f allure_behave.formatter:AllureFormatter -o web_allure_result features/
unset platformParams
allure serve web_allure_result
```

## 9. Example environment.py
```Example
from allure.allure import screenshot
from drivers.driver_factory import get_driver
from pages.page_storage import PageStorage
import json
import os


locators_os = os.getenv('locators')
locators_path = locators_os if locators_os is not None else 'resources/LOCATORS.json'


def before_all(context):
    with open(str(os.getenv('platformParams'))) as capability:
        capabilities = json.load(capability)
    context.driver = get_driver(capabilities)
    context.driver.open_app()
    context.pages = PageStorage()
    context.pages.loader.set_driver(context.driver).set_file(locators_path)


def after_all(context):
    context.driver.close_app()


def before_feature(context, feature):
    context.driver.open_app()


def after_feature(context, feature):
    pass


def before_scenario(context, scenario):
    context.driver.reopen_app()


def after_scenario(context, scenario):
    pass


def before_step(context, step):
    screenshot(
        context.driver.get_screenshot_as_png(),
        'Before Screenshot'
    )


def after_step(context, step):
    screenshot(
        context.driver.get_screenshot_as_png(),
        'After Screenshot'
    )
```

## 10. signup.feature
```Example
Feature: 1. Sign Up


    @sign_up @smoke @regression @Web @Android @iOS
  Scenario: Navigate to Sign up page
    Then Start page is open
    When Navigate to Sign Up page
    Then Sign Up page is open
```

## 11. signup.py
```Example
from behave import given, when, then
from steps.steps_wrapper import step_wrapper as wrapper


@when('Navigate to Sign Up page')
@wrapper(step_name='Navigate to Sign Up page')
def step_impl(context):
    context.driver.click(context.pages.get('Start page').get_locator('Sign Up button'))


@then('Start page is open')
@wrapper(step_name='Start page is open')
def step_impl(context):
    context.pages.get('Start page').is_open()


@then('Sign Up page is open')
@wrapper(step_name='Sign Up page is open')
def step_impl(context):
    context.pages.get('Start page').is_close()
```