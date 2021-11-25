import asyncio
import json
import sys
from emailmanager import EmailManager
from seleniummanager import SeleniumManager
from pathlib import Path

# Load json config

class App:

    def __init__(self):
        self.selenium_managers: dict[str, SeleniumManager] = {}
        self.load_config_file()

        self.email_manager: EmailManager = EmailManager(self.config['smtpServer'], self.config['sendFrom'])
        self.load_sites()

    def load_config_file(self):
        '''Loads and validates config information from config.json.'''
        try:
            with open('config.json') as config_file:
                try:
                    self.config = json.load(config_file)
                    if not self.config.get('smtpServer'): # if the smtpServer doesn't exist, exit with an error message
                        print('ERROR: config.json must contain smtpServer options. See documentation for details.')
                        sys.exit()
                    if not self.config.get('sendFrom'): # if the sendFrom object doesn't exist, exit with an error message
                        print('ERROR: config.json must contain sendFrom options. See documentation for details.')
                        sys.exit()
                except json.decoder.JSONDecodeError as error: # if there is an error while decoding the json, exit with an error message
                    print("ERROR: config.json is not a valid json file. See message below for decoder response.")
                    print("Message:", error)
                    sys.exit()
        except FileNotFoundError: # if config.json doesn't exit, exit with an error message
            print("ERROR: Must have a config.json file in the application directory.")
            sys.exit()
    
    def load_sites(self):
        '''Loads selenium managers from the sites config files.'''
        # start loading sites
        sites_dir = Path('.') / 'sites'
        if not sites_dir.exists(): # if the sites directory doesn't exist, exit with an error message
            print("ERROR: 'sites' directory is required. See documentation for more details.")
            sys.exit()
        sites = sites_dir.glob('*.json')
        for site in sites:
            site_name = site.name[:-5] # removes the .json from the file name
            with site.open() as site_contents:
                try:
                    contents = json.load(site_contents)
                except json.decoder.JSONDecodeError as error:
                    print(f"ERROR: site configuration '{site.name}' is not valid JSON. See message below for decoder response.")
                    print("Message:", error)
                    sys.exit()
            self.validate_site_config(contents, site.name)
            send_to = []
            for block in contents['sendTo']:
                email_address = block['emailAddress']
                display_name = block.get('displayName')
                display_name = display_name if display_name else email_address
                send_to.append({
                    'email_address': email_address,
                    'display_name': display_name
                })
            send_url = contents.get('sendURL')
            send_url = send_url if send_url else contents['url']
            self.selenium_managers[site_name] = SeleniumManager(
                contents['name'],
                contents['url'], 
                contents['elementXPath'],
                contents['testType'],
                contents['compareValue'],
                send_to,
                contents['reloadTime'],
                contents['waitTime'],
                self.email_manager,
                send_url)
    
    def validate_site_config(self, config: dict[str, any], file_name):
        if not config.get("name"):
            print(f"ERROR: site configuarion '{file_name}' is missing required parameter 'name'. See documentation for more details.")
            sys.exit()
        if not config.get("url"):
            print(f"ERROR: site configuarion '{file_name}' is missing required parameter 'url'. See documentation for more details.")
            sys.exit()
        if not config.get("elementXPath"):
            print(f"ERROR: site configuarion '{file_name}' is missing required parameter 'elementXPath'. See documentation for more details.")
            sys.exit()
        if not config.get("testType"):
            print(f"ERROR: site configuarion '{file_name}' is missing required parameter 'testType'. See documentation for more details.")
            sys.exit()
        if not config.get("compareValue"):
            print(f"ERROR: site configuarion '{file_name}' is missing required parameter 'compareValue'. See documentation for more details.")
            sys.exit()
        if not config.get("sendTo"):
            print(f"ERROR: site configuarion '{file_name}' is missing required parameter 'sendTo'. See documentation for more details.")
            sys.exit()
        if type(config['sendTo']) != list:
            print(f"ERROR: site configuarion '{file_name}' is invalid. Parameter 'sendTo' must be a list. See documentation for more details.")
            sys.exit()
        if len(config['sendTo']) == 0:
            print(f"WARNING: site configuration '{file_name} has no sendTo values. No notification will be sent!")
        for index, obj in enumerate(config['sendTo']):
            if not obj.get("emailAddress"):
                print(f"ERROR: site configuarion '{file_name}' is invalid. 'sendTo' block {index + 1} is missing required parameter 'emailAddress'. See documentation for more details.")
                sys.exit()
        if not config.get("reloadTime"):
            print(f"ERROR: site configuarion '{file_name}' is missing required parameter 'reloadTime'. See documentation for more details.")
            sys.exit()
        if not config.get("waitTime"):
            print(f"ERROR: site configuarion '{file_name}' is missing required parameter 'waitTime'. See documentation for more details.")
            sys.exit()

    def run(self):
        '''Starts running the app. This includes starting up webdrivers and actively performing testing.'''
        # start selenium managers
        for key in self.selenium_managers:
            self.selenium_managers[key].start()
            try:
                asyncio.run(self.selenium_managers[key].run())
            except Exception as error:
                app.email_manager.send_email('davidtbootle@gmail.com', 'David Bootle', 'Stock Notfier CRITICAL ERROR', f'''
                Stock Notifier has encountered a critical error! Check server ASAP!
                
                Error Type: {type(error)}
                Error Message: {error}
                ''')
                raise error

if __name__ == "__main__":
    print('Starting app!')
    app = App()
    app.run()