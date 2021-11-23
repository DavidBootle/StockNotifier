import json
import sys
from emailmanager import EmailManager

# Load json config

class App:

    def __init__(self):
        self.load_config_file()

        self.email_manager = EmailManager(self.config['smtpServer'], self.config['sendFrom'])

    def load_config_file(self):
        # load config from config.json
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

    def run(self):
        pass

app = App()