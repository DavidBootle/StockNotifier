import json
import sys
from emailmanager import EmailManager
from pathlib import Path
from selenium import webdriver
import time
from sitemanager import SiteManager

# Load json config

class App:

    def __init__(self):
        self.site_managers: list[SiteManager] = []
        self.load_config_file()
        self.load_diagnostic_folder()

        self.wait_time: (int | float) = self.config.get('waitTime') if self.config.get('waitTime') else 0


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
        self.driver = None

        # start loading sites
        sites_dir = Path('.') / 'sites'
        if not sites_dir.exists(): # if the sites directory doesn't exist, exit with an error message
            print("ERROR: 'sites' directory is required. See documentation for more details.")
            sys.exit()
        sites = sites_dir.glob('*.json')
        for site in sites:
            if site.name[0] != '.': # skip files with a .name
                self.site_managers.append(SiteManager(self.driver, site, self.email_manager))

    def run(self):
        '''Starts running the app. This includes starting up webdrivers and actively performing testing.'''
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(10)
        # update driver for site_managers
        for site_manager in self.site_managers:
            site_manager.driver = self.driver
        while len(self.site_managers) > 0:
            tmp_site_managers = self.site_managers.copy()
            for site_manager in tmp_site_managers:
                site_enabled = site_manager.run()
                if not site_enabled:
                    self.site_managers.remove(site_manager)
            if self.wait_time > 0:
                print(f'Waiting {self.wait_time} seconds according to config...')
                time.sleep(self.wait_time)
        print('No sites are still running! The program will now exit.')
        self.stop()
    
    def load_diagnostic_folder(self):
        diagnostics_folder = Path('.') / 'diagnostics'
        if not diagnostics_folder.exists():
            diagnostics_folder.mkdir()
    
    def stop(self):
        self.driver.quit()

if __name__ == "__main__":
    print('Starting app!')
    app = App()
    app.run()