from selenium import webdriver
import selenium
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import selenium.common.exceptions as selenium_exceptions

class SeleniumManager:
    '''A class that is in charge of a single site. It manages its own webdriver and testing.'''

    def __init__(self, name: str, url: str, element_xpath: str, test_type: str, compare_value: str, send_to: list[object]):
        '''Initialize a new SeleniumManager'''
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(10) #will wait up to 10 seconds for the element to be found before an error occurs
        self.name = name
        self.url = url
        self.element_xpath = element_xpath
        self.test_type = test_type
        self.compare_value = compare_value
        self.send_to = send_to
    
    def run(self):
        '''Run one test.'''
        match self.test_type:
            case 'element_does_not_contain_text':
                # checks the element to see if the element's text contains the compare value. If not, it triggers the success response.
                self.element_does_not_contain_text_test()
            case _:
                self.failure_response(f'[ERROR] Site {self.name} is configured with a test type that is not valid. Please check the documentation for a list of valid test types.')
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
        message_start = f'[ERROR] Test failed for ${self.name}. '
        message_end = ''

        match type(exception):
            case type(selenium_exceptions.NoSuchElementException):
                message_end = "The element could not be found on the page. This could be because the time the page takes to load exceeds the page wait time, or that your XPath is invalid. Check your configuration."
            case _ as error:
                message_end = f"A {type(error)} occurred. Error output message: {str(error)}"
        
        self.failure_response(message_start + message_end)
    
    def failure_response(self, message: str):
        '''This function defines how the program should respond to an error.''' 
        print(message)
    
    def success_response(self):
        '''This function triggers when the test criteria are met. It should stop the webdriver and send an email.'''
        print(f'Site {self.name} triggered success response!')
        self.stop()
    
    def normal_response(self, message):
        '''This function triggers when the test criteria is not met, but no errors occur, and the program can continue running.'''
        print(f'Site {self.name} tested negative and will continue running.')

    def stop(self):
        '''Stops the webdriver. Should also perform any necessary cleanup.'''
        self.driver.quit()