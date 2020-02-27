import email.message
import mimetypes
import smtplib


class Email:

    def __init__(self, sender, subject=None, body=None, attachments=None):
        self.sender = sender
        self.subject = subject
        self.body = body
        self.attachments = attachments or []


    def send(self, recipients, smtp_host):
        message = self._create_message(recipients)
        with smtplib.SMTP(smtp_host) as smtp:
            smtp.starttls()
            smtp.send_message(message)


    def _create_message(self, recipients):
        message = email.message.EmailMessage()
        if isinstance(recipients, str): message['To'] = recipients
        else: message['To'] = ', '.join(recipients)
        message['From'] = self.sender
        message['Subject'] = self.subject
        message.set_content(self.body)
        self._add_attachments(message)
        return message


    def _add_attachments(self, message):
        for attachment in self.attachments:
            mime_type, _ = mimetypes.guess_type(attachment['filename'])
            maintype, subtype = mime_type.split('/')
            message.add_attachment(
                attachment['content'],
                maintype=maintype,
                subtype=subtype,
                filename=attachment['filename']
            )


def from_template(template: dict) -> Email:
    sender = template['sender']
    subject = template.get('subject')
    body = template.get('body')
    attachments = template.get('attachments')
    return Email(sender, subject, body, attachments)
