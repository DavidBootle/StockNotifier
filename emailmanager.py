import sys
from envelopes import Envelope

class EmailManager:

    def __init__(self, smtpOptions, senderOptions):
        self.verify_options(smtpOptions, senderOptions)

    def send_email(self, to_address, to_name, subject, body):

        email = Envelope(
            from_addr=(self.email_address, self.display_name),
            to_addr=(to_address, to_name),
            subject=subject,
            text_body=body
        )

        email.send(self.url, port=self.port, login=self.login, password=self.password, tls=True)

    def verify_options(self, smtp_options, sender_options):
        if not smtp_options.get('url'):
            print("ERROR: smtpServer config is misconfigured. Missing 'url' parameter. Please check config.json.")
            sys.exit()
        elif not smtp_options.get('login'):
            print("ERROR: smtpServer config is misconfigured. Missing 'login' parameter. Please check config.json.")
            sys.exit()
        elif not smtp_options.get('password'):
            print("ERROR: smtpServer config is misconfigured. Missing 'password' parameter. Please check config.json.")
            sys.exit()
        elif not smtp_options.get('port'):
            print("ERROR: smtpServer config is misconfigured. Missing 'port' parameter. Please check config.json.")
            sys.exit()
        else:
            self.url = smtp_options['url']
            self.port = smtp_options['port']
            self.login = smtp_options['login']
            self.password = smtp_options['password']
        
        if not sender_options.get('displayName'):
            print("ERROR: sendFrom config is misconfigured. Missing 'displayName' parameter. Please check config.json.")
            sys.exit()
        elif not sender_options.get('emailAddress'):
            print("ERROR: sendFrom config is misconfigured. Missing 'emailAddress' parameter. Please check config.json.")
            sys.exit()
        else:
            self.display_name = sender_options['displayName']
            self.email_address = sender_options['emailAddress']
        