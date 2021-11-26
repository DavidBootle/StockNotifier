# StockNotifier
Uses Selenium WebDriver to check webpages for keywords, then send an email if the keyword is found.

Meant to be an improved sequel to my SeleniumStockChecker project which is not currently functional.

# How It Works
The program is intended to be used for autonomously checking webpages, rather than constantly reloading yourself. Want to know when something is in stock? Set it up to check that webpage and notify you when 'Out of Stock' disappears off the page.

Stock Notifier can check multiple websites at once. See [site configs](#site-configs) for how to set this up. The program will test each site in order, then wait for the amount of time given in the [waitTime](#wait-time) parameter, which can be set in the program configuation. It then repeats this loop, referred to from here on as the *site loop*, over and over.

Each site you want to check requires a site configuration in the `sites` directory. Each of these configurations is managed by a **site manager**, which loads the page and performs a test. The site manager is in charge of figuring out whether testing condidtions are met and sending emails, and also handling all related errors. When run, the main program (`app.py`) will create a site manager for each site configuration, and then loop through these site managers in the site loop. If a site manager encounters a fatal error while testing, it will be removed from the site loop and notify the emails listed in the configuration that it has failed. If there are no more site managers in the site loop, the program will exit.

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
    },
    "waitTime": 10
}
```
You must fill out all of these properties in order for the app to function.

### `smtpServer`
This project sends emails directly using SMTP. As such, it needs SMTP server information in order to connect and send emails.

The `url` paramter is the url of the server. This will generally be given to you by whatever SMTP server you are using. Similarily, the `login`, `password`, and `port` parameters will also be given to you by your SMTP service.

### `sendFrom`
This controls what email address and display name the messages will be sent with. Make sure this is a valid sending address on your SMTP server. The `emailAddress` parameter controls the email address, and the `displayName` parameter controls the display name.

### `waitTime`
The `waitTime` parameter is an optional parameter. If set, the program will wait for the specified amount of seconds every site loop. If not set, the program does not wait and immediately repeats the loop.

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

The `sendURL` parameter can be used to override which link is sent in the email when success is triggered. By default, the link sent is the `url` parameter.

# Running
Run the program by running `app.py` with Python 3.10.