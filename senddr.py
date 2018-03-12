#!/usr/bin/python3.5

import smtpd
import asyncore
import email
from email.parser import Parser
import sendgrid
import os
from sendgrid.helpers.mail import *

class CustomSMTPServer(smtpd.SMTPServer):

    def process_message(self, peer, mailfrom, rcpttos, data):
        print( 'Receiving message from:', peer)
        print( 'Message addressed from:', mailfrom)
        print( 'Message addressed to  :', rcpttos)
        body = email.message_from_string(data).get_payload()
        subject = Parser().parsestr(data)['subject']
        contenttype = Parser().parsestr(data)['Content-Type']
        print( 'Message contenttype   :', contenttype)
        print( 'Message subject       :', subject)
#        print( 'Message body          :', body)
        sg = sendgrid.SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))
        from_email = Email( mailfrom )
        to_email = Email( rcpttos )
        content = Content(contenttype.split(';')[0], body)
        mail = Mail(from_email, subject, to_email, content)
        response = sg.client.mail.send.post(request_body=mail.get())
        print(response.status_code)
        print(response.body)
        print(response.headers)
        return

server = CustomSMTPServer(('127.0.0.1', 25), None)
asyncore.loop()

