import json
import sys
from emailmanager import EmailManager
from seleniummanager import SeleniumManager

# Load json config

class App:

    def __init__(self):
        self.load_config_file()

        self.email_manager = EmailManager(self.config['smtpServer'], self.config['sendFrom'])

    def load_config_file(self):
        '''Loads and validates config information from config.json.'''
        try:
            with open('config.json') as config_file:
                try:
                    self.config = json.load(config_file)
                    if not self.config.get('smtpServer'):
                        print('ERROR: config.json must contain smtpServer options. See documentation for details.')
                        sys.exit()
                    if not self.config.get('sendFrom'):
                        print('ERROR: config.json must contain sendFrom options. See documentation for details.')
                        sys.exit()
                except json.decoder.JSONDecodeError as error:
                    print("ERROR: config.json is not a valid json file. See message below for decoder response.")
                    print("Message:", error)
                    sys.exit()
        except FileNotFoundError:
            print("ERROR: Must have a config.json file in the application directory.")
            sys.exit()
        
        # start loading sites

    def run(self):
        '''Starts running the app. This includes starting up webdrivers and actively performing testing.'''
        pass

if __name__ == "__main__":
    app = App()
    print('doing things!')