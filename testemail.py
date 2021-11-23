# Running this script will send a test email using your smtpServer and sendFrom configuration.

from app import App

app = App()
recipient_email = input('Email address to send to: ')
recipient_name = input('Recipient display name: ')

email_result = app.email_manager.send_email(recipient_email, recipient_name, "Test Email from Stock Notifier", "This is a test email from Stock Notifier. If you've recieved this, it means that your SMTP setup is working!")

if email_result == {}:
    print('Email sent with no issues.')
else:
    print('Non-normal email resposne. Response printed below.')
    print(email_result)