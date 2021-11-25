# StockNotifier
Uses Selenium WebDriver to check webpages for keywords, then send an email if the keyword is found.

Meant to be an improved sequel to my SeleniumStockChecker project which is not currently functional.

# Requirements
- Python 3.10
- Envelopes
- Selenium
- Firefox
- geckodriver

# Install
First, install Python 3.10 if you haven't already. Then clone the repository. Once cloned, install Selenium and Evnelopes.

```bash
pip install selenium
pip install envelopes
```

Firefox is used as the webdriver for this project. Make sure to have the latest version of Firefox. Then, download the latest version of **geckodriver**. Place the geckodriver executable somewhere in your PATH.

## config.json
This project needs some configuration before running. 

Open `config.json` in the root of the repository. It should look like this:

```json
{
    "smtpServer": {
        "url": "",
        "login": "",
        "password": "",
        "port": 465
    },
    "sendFrom": {
        "displayName": "",
        "emailAddress": ""
    }
}
```
You must fill out all of these properties in order for the app to function.

### `smtpServer`
This project sends emails directly using SMTP. As such, it needs SMTP server information in order to connect and send emails.

The `url` paramter is the url of the server. This will generally be given to you by whatever SMTP server you are using. Similarily, the `login`, `password`, and `port` parameters will also be given to you by your SMTP service.

### `sendFrom`
This controls what email address and display name the messages will be sent with. Make sure this is a valid sending address on your SMTP server. The `emailAddress` parameter controls the email address, and the `displayName` parameter controls the display name.

## Site Configs
The main focus of the project is of course to test sites for various conditions. Here's how to set this up. 

Create a `sites` directory in the root of the repository. In the directory, create JSON files with the following structure:

```json
{
    "name": "",
    "url": "",
    "elementXPath": "",
    "testType": "",
    "compareValue": "",
    "sendTo": [
        {
            "emailAddress": "",
            "displayName": ""
        }
    ],
    "reloadTime": 0,
    "waitTime": 0,
    "sendURL": ""
}
```
The `name` parameter is what you want the configuration to be referred to by the program. For example, if you are checking for a Playstation 5, then you might put that as its name. The name will show up whenever the test succeeds for the configuration, or if it encounters an error. This helps differentiate it from other configurations that are running at the same time.

The `url` paramter is the url that the program should check.

The `elementXPath` parameter is the XPath of the element that tests will be run on within the page.

The `testType` parameter determines what kind of test will be performed. The types of tests are listed below:
- `element_does_not_contain_text`: This test looks at the element (given by the XPath), and checks its innerHTML. If the innerHTML does not contain the value of the `compareValue` parameter, then success is triggered.

The `criteriaValue` parameter is used in conjunction with the `testType` parameter. See above.

The `sendTo` parameter is a list of objects, where each object should contain two parameters: `emailAddress` and `displayName`. These blocks specify the recipients who will be emailed when success is triggered. For each block, `emailAddress` is required, but `displayName` is optional. If not set, the email address will be used instead.

The `reloadTime` parameter specifies how often the webpage should be reloaded, in seconds.

The `waitTime` parameter specifies how long the program should wait when trying to detect the element (given by the `elementXPath` parameter). For pages that take a while to load, setting this value too low will cause the program to stop because it cannot find the element. The wait time should always be less than the reload time for optimal performance.

The `sendURL` parameter can be used to override which link is sent in the email when success is triggered. By default, the link sent is the `url` parameter.

# Running
Run the program by running `app.py` with Python 3.10.