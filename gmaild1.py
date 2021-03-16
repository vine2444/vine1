
import imaplib
import base64
import os
import email
import getpass
import logging

email_user = input('Email: ')
email_pass = getpass.getpass('Enter your password: ')
#email_pass = input('Password: ')

mail = imaplib.IMAP4_SSL('imap.gmail.com')
mail.login(email_user, email_pass)
mail.select()

''' need to do these two to access email
1) https://myaccount.google.com/lesssecureapps?pli=1

2) Gmail Settings -> Forwarding and POP / IMAP -> IMAP Acess to Enable IMAP
'''


type, data = mail.search(None, 'ALL')
mail_ids = data[0]
id_list = mail_ids.split()
logging.basicConfig(filename ='app.log',format='%(asctime)s %(levelname)-8s %(message)s', level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S')
maindir = '.'
if 'attachments' not in os.listdir(maindir):
    os.mkdir('attachments')

for num in data[0].split():
    typ, data = mail.fetch(num, '(RFC822)')
    raw_email = data[0][1]
# converts byte literal to string removing b''
    raw_email_string = raw_email.decode('utf-8')
    email_message = email.message_from_string(raw_email_string)
# downloading attachments
    for part in email_message.walk():
        # this part comes from the snipped I don't understand yet...
        if part.get_content_maintype() == 'multipart':
            continue
        if part.get('Content-Disposition') is None:
            continue
        fileName = part.get_filename()
        if bool(fileName) and fileName.endswith(('.xls','.zip', '.rar','.csv','xlsx','xlsm')):
            
            filePath = os.path.join(maindir, 'attachments', fileName)
            if not os.path.isfile(filePath):
                fp = open(filePath, 'wb')
                fp.write(part.get_payload(decode=True))
                logging.info('downloaded file' + fileName + ' ' + email_message['Date'] )

                fp.close()
            subject = str(email_message).split(
                "Subject: ", 1)[1].split("\nTo:", 1)[0]
            print("Downloaded file " + fileName + ' ' + email_message['Date'])
