import mimetypes

import unittest
from unittest.mock import patch, call

import emails



class TestEmails(unittest.TestCase):

    def setUp(self):
        self.sender = 'sender@example.com'
        self.recipients = ['recipient1@example.com', 'recipient2@example.com']
        self.subject = 'Test subject'
        self.body = 'Test body'
        self.attachments = [
            {
                'filename': 'example.csv',
                'content': b'1,2,3'
            },
            {
                'filename': 'example.json',
                'content': b'{"a": 1, "b": 2}'
            }
        ]


    def test_constructor(self):
        email = emails.Email(self.sender, self.subject, self.body, self.attachments)
        self.assertEqual(email.sender, self.sender)
        self.assertEqual(email.subject, self.subject)
        self.assertEqual(email.body, self.body)
        self.assertEqual(email.attachments, self.attachments)


    def test_from_template(self):
        template = {
            'sender': self.sender,
            'subject': self.subject,
            'body': self.body,
            'attachments': self.attachments
        }
        email = emails.from_template(template)
        self.assertEqual(email.sender, self.sender)
        self.assertEqual(email.subject, self.subject)
        self.assertEqual(email.body, self.body)
        self.assertEqual(email.attachments, self.attachments)


    def test_from_template_raises_if_sender_not_specified(self):
        template = {
            'subject': self.subject,
            'body': self.body,
            'attachments': self.attachments
        }
        with self.assertRaises(KeyError):
            email = emails.from_template(template)


    @patch('smtplib.SMTP')
    def test_smtp_is_called_correctly(self, smtp_mock):
        self._prepare_smtp_mock(smtp_mock)
        email = emails.Email(self.sender, self.subject, self.body, self.attachments)
        email.send(self.recipients, 'test_smtp_host')
        smtp_mock.assert_called_once_with('test_smtp_host')
        smtp_mock.__enter__.assert_called_once()
        smtp_mock.starttls.assert_called_once()
        smtp_mock.send_message.assert_called_once()
        smtp_mock.__exit__.assert_called_once()


    @patch('email.message.EmailMessage.add_attachment')
    @patch('smtplib.SMTP')
    def test_sent_message_is_constructed_correctly(self, smtp_mock, add_attachment_mock):
        self._prepare_smtp_mock(smtp_mock)
        email = emails.Email(self.sender, self.subject, self.body, self.attachments)
        email.send(self.recipients, 'test_smtp_host')
        sent_message = smtp_mock.send_message.call_args[0][0]
        self.assertEqual(sent_message['From'], self.sender)
        self.assertEqual(sent_message['To'], ', '.join(self.recipients))
        self.assertEqual(sent_message['Subject'], self.subject)
        self.assertEqual(sent_message.get_content().strip(), self.body)
        expected_calls = []
        for attachment in self.attachments:
            content = attachment['content']
            filename = attachment['filename']
            mime_type = mimetypes.guess_type(filename)
            maintype, subtype = mime_type[0].split('/')
            expected_calls.append(call(content, maintype=maintype, subtype=subtype, filename=filename))
        self.assertEqual(add_attachment_mock.mock_calls, expected_calls)


    @patch('smtplib.SMTP')
    def test_single_recipient(self, smtp_mock):
        self._prepare_smtp_mock(smtp_mock)
        email = emails.Email(self.sender, self.subject, self.body, self.attachments)
        email.send('person1@example.com', 'test_smtp_host')
        sent_message = smtp_mock.send_message.call_args[0][0]
        self.assertEqual(sent_message['To'], 'person1@example.com')


    def _prepare_smtp_mock(self, smtp_mock):
        smtp_mock.return_value = smtp_mock
        smtp_mock.__enter__.return_value = smtp_mock