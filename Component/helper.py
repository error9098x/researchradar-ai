import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header
from email.mime.application import MIMEApplication
from email.utils import COMMASPACE

def send_email(sender, password, receiver, smtp_server, smtp_port, email_message, subject, attachment=None, is_html=False):
    message = MIMEMultipart()
    message['To'] = COMMASPACE.join([receiver])  
    message['From'] = sender
    message['Subject'] = subject

    # Attach the email body
    if is_html:
        message.attach(MIMEText(email_message, 'html', 'utf-8'))
    else:
        # For plain text messages
        message.attach(MIMEText(email_message, 'plain', 'utf-8'))

    if attachment:
        maintype, _, subtype = (attachment.type or 'application/octet-stream').partition('/')
        # Create a MIMEApplication object for the attachment
        att = MIMEApplication(attachment.read(), _subtype=subtype)
        att.add_header('Content-Disposition', 'attachment', filename=attachment.name)
        message.attach(att)  # Attach the attachment to the message

    # Establish a connection to the SMTP server
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()  
    server.login(sender, password)  # Log in to the server using the provided credentials
    text = message.as_string()  # Convert the message to a string
    server.sendmail(sender, receiver, text)  # Send the email
    server.quit() 

