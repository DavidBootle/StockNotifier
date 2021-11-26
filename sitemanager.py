from selenium import webdriver
from selenium.common import exceptions as selenium_exceptions
from selenium.webdriver.common.by import By
from emailmanager import EmailManager
import sys
from pathlib import Path
import json

class SiteManager:

    name: str
    url: str
    element_xpath: str
    test_type: str
    compare_value: any
    send_to: list[dict[str, str]]
    send_url: str

    disabled = False
    test_met = False

    def __init__(self, driver: webdriver.Firefox, config_path: Path, email_manager: EmailManager):
        self.driver = driver
        self.email_manager = email_manager

        # load config file
        with config_path.open() as config_file:
            try:
                config: dict = json.load(config_file)
                self.load_config(config, config_path.name)
            except json.decoder.JSONDecodeError as error:
                print(f"ERROR: site configuration '{config_path.name}' is not valid JSON. See message below for decoder response.")
                print("Message:", error)
                sys.exit()
        
        # set test
        self.set_test()

    def run(self) -> bool:
        '''Runs one test. Returns False if the site_manager is disabled, otherwise returns True.'''
        if self.disabled:
            return False
        else:
            self.test()
            return True if not self.disabled else False

    def load_config(self, config: dict, file_name: str):
        self._validate_config_parameter(config, 'name', file_name)
        self._validate_config_parameter(config, 'url', file_name)
        self._validate_config_parameter(config, 'elementXPath', file_name)
        self._validate_config_parameter(config, 'testType', file_name)
        self._validate_config_parameter(config, 'compareValue', file_name)
        self._validate_config_parameter(config, 'sendTo', file_name)
        
        if type(config['sendTo']) != list:
            print(f"ERROR: site configuarion '{file_name}' is invalid. Parameter 'sendTo' must be a list. See documentation for more details.")
            sys.exit()
        if len(config['sendTo']) == 0:
            print(f"WARNING: site configuration '{file_name} has no sendTo values. No notification will be sent!")
        for index, obj in enumerate(config['sendTo']):
            if not obj.get("emailAddress"):
                print(f"ERROR: site configuarion '{file_name}' is invalid. 'sendTo' block {index + 1} is missing required parameter 'emailAddress'. See documentation for more details.")
                sys.exit()
        
        self.name = config['name']
        self.url = config['url']
        self.element_xpath = config['elementXPath']
        self.test_type = config['testType']
        self.compare_value = config['compareValue']
        self.send_to = config['sendTo']
        self.send_url = config['sendURL'] if config.get('sendURL') else config['url']
    
    def _validate_config_parameter(self, config: dict, parameter: str, file_name: str):
        if not config.get(parameter):
            print(f"ERROR: site configuarion '{file_name}' is missing required parameter '{parameter}'. See documentation for more details.")
            sys.exit()
    
    def set_test(self):
        '''Sets self.test to the correct function depending on test type.'''
        match self.test_type:
            case 'element_does_not_contain_text':
                # checks the element to see if the element's text contains the compare value. If not, it triggers the success response.
                self.test = self.element_does_not_contain_text_test
            case _:
                self.failure_response(f"[ERROR] Site '{self.name}' is configured with a test type that is not valid. Please check the documentation for a list of valid test types.")
                self.stop()

    def element_does_not_contain_text_test(self):
        '''Tests if the element's text contains the compare value. If not, it triggers the success response.'''

        try:
            self.driver.get(self.url) # gets the page
            element = self.driver.find_element(By.XPATH, self.element_xpath) # tries to find the given element
            text: str = element.get_attribute('innerHTML') # gets the text of the element
            if self.compare_value not in text: # if the compare value is contained within the text of the element, then it activates the success response
                self.success_response()
            else: # otherwise it activates the normal response
                self.normal_response()
        except Exception as error:
            self.failure_from_error(error)

    def failure_from_error(self, exception: Exception):
        '''This method handles how the program should respond to excpetions of various types raised during tests.'''
        message_start = f"[ERROR] Test failed for '{self.name}'. "
        message_end = ''

        send_email = True

        match type(exception):
            case selenium_exceptions.NoSuchElementException:
                message_end = "The element could not be found on the page. This could be because the time the page takes to load exceeds the page wait time, or that your XPath is invalid. Check your configuration."
            case selenium_exceptions.WebDriverException:
                message_end = f"A WebDriverException occurred. This is most likely because it failed to get the page. Check your network settings! The error message is printed below:\n{exception.msg}"
                send_email = False
            case _ as error:
                message_end = f"A {type(exception)} occurred. Error output message: {str(exception)}"
        
        self.failure_response(message_start + message_end, send_email)
    
    def failure_response(self, message: str, send_email: bool = True):
        '''This function defines how the program should respond to an error.''' 
        subject = f'Error Notification for "{self.name}"'
        email_message = f'''
        This is an error notification for the site "{self.name}". An error was encountered while testing, and testing for this site has been stopped.

        Error Message: {message}
        '''
        if send_email:
            for recipient in self.send_to:
                self.email_manager.send_email(recipient['emailAddress'], recipient['displayName'], subject, email_message)
        print(message)
        self.stop()
    
    def success_response(self):
        '''This function triggers when the test criteria are met. It should stop the webdriver and send an email.'''
        if self.test_met: # if the test has already been met, do not send another email
            print(f"Site '{self.name}' triggered success response again. Testing will continue.")
        else: # if this is the first time the test has been met, send emails
            subject = f'Stock Notification for "{self.name}"'
            message = f"{self.name} was triggered! View the link: {self.send_url}"
            for recipient in self.send_to:
                self.email_manager.send_email(recipient['emailAddress'], recipient['displayName'], subject, message)
            print(f"Site '{self.name}' triggered success response! Emails have been sent!")
        self.test_met = True
    
    def normal_response(self):
        '''This function triggers when the test criteria is not met, but no errors occur, and the program can continue running.'''
        if self.test_met: # if product is no longer available, send emails
            subject = f'Stock Notification for "{self.name}"'
            message = f"{self.name} has returned to normal. View the link: {self.send_url}"
            for recipient in self.send_to:
                self.email_manager.send_email(recipient['emailAddress'], recipient['displayName'], subject, message)
            print(f"Site '{self.name}' has gone from meeting tests to failing tests. Normality messages have been sent. Testing will continue.")
        else: # if product is still not available, send emails
            print(f"Site '{self.name}' tested negative and will continue running.")
        self.test_met = False

    def stop(self):
        '''Sets state to disabled. Should also perform any necessary cleanup.'''
        self.disabled = True