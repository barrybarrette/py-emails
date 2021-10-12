import mimetypes
import socket

import unittest
from unittest.mock import patch, call

import emails



class TestEmail(unittest.TestCase):

    def setUp(self):
        self.recipients = ['recipient1@example.com', 'recipient2@example.com']
        self.subject = 'Test subject'
        self.body = '<p>Test body</p>'
        self.body_type = 'html'
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
        self.smtp_config = {
            'sender': 'sender@example.com',
            'host': 'smtp.example.com'
        }


    def test_constructor(self):
        email = emails.Email(self.smtp_config, self.subject, self.body, self.body_type, self.attachments)
        self.assert_email_is_built_correctly(email)


    def test_constructor_raises_if_sender_not_specified(self):
        self.smtp_config.pop('sender')
        with self.assertRaises(emails._src.InvalidSmtpConfigError):
            email = emails.Email(self.smtp_config)


    def test_constructor_raises_if_host_not_specified(self):
        self.smtp_config.pop('host')
        with self.assertRaises(emails._src.InvalidSmtpConfigError):
            email = emails.Email(self.smtp_config)


    def test_raises_if_attachment_mimetype_cannot_be_guessed_and_was_not_specified(self):
        attachment = {'filename': 'LICENSE', 'content': b'MIT License'}
        with self.assertRaises(emails._src.MimeTypeNotSpecifiedError):
            email = emails.Email(self.smtp_config, attachments=[attachment])


    def test_from_template(self):
        template = {
            'smtp_config': self.smtp_config,
            'subject': self.subject,
            'body': self.body,
            'body_type': self.body_type,
            'attachments': self.attachments
        }
        email = emails.from_template(template)
        self.assert_email_is_built_correctly(email)


    def test_from_template_raises_if_smtp_config_not_specified(self):
        template = {
            'subject': self.subject,
            'body': self.body,
            'attachments': self.attachments
        }
        with self.assertRaises(emails._src.SmtpConfigNotProvidedError):
            email = emails.from_template(template)


    # Helpers
    def assert_email_is_built_correctly(self, email: emails.Email):
        self.assertEqual(email.smtp_config, self.smtp_config)
        self.assertEqual(email.subject, self.subject)
        self.assertEqual(email.body, self.body)
        self.assertEqual(email.body_type, self.body_type)
        self.assertEqual(email.attachments, self.attachments)


@patch('smtplib.SMTP')
class TestEmailSend(unittest.TestCase):

    def setUp(self):
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
        self.smtp_config = {
            'sender': 'sender@example.com',
            'host': 'smtp.example.com',
            'port': 587,
            'password': 'test_password'
        }


    def test_smtp_is_called_correctly(self, smtp_mock):
        self._prepare_smtp_mock(smtp_mock)
        email = emails.Email(self.smtp_config)
        email.send(self.recipients)
        smtp_mock.assert_called_once_with(self.smtp_config['host'], self.smtp_config['port'])
        smtp_mock.__enter__.assert_called_once()
        smtp_mock.starttls.assert_called_once()
        smtp_mock.send_message.assert_called_once()
        smtp_mock.__exit__.assert_called_once()


    def test_defaults_to_port_25_if_not_specified(self, smtp_mock):
        self._prepare_smtp_mock(smtp_mock)
        self.smtp_config.pop('port')
        email = emails.Email(self.smtp_config)
        email.send(self.recipients)
        smtp_mock.assert_called_once_with(self.smtp_config['host'], 25)


    def test_smtp_authenticates_if_auth_specified_in_config(self, smtp_mock):
        self._prepare_smtp_mock(smtp_mock)
        email = emails.Email(self.smtp_config)
        email.send(self.recipients)
        smtp_mock.login.assert_called_once_with(self.smtp_config['sender'], self.smtp_config['password'])


    def test_smtp_does_not_attempt_to_authenticate_if_password_not_specified_in_config(self, smtp_mock):
        self._prepare_smtp_mock(smtp_mock)
        self.smtp_config.pop('password')
        email = emails.Email(self.smtp_config)
        email.send(self.recipients)
        smtp_mock.login.assert_not_called()


    def test_sent_message_is_constructed_correctly(self, smtp_mock):
        self._prepare_smtp_mock(smtp_mock)
        e = emails.Email(self.smtp_config, self.subject, self.body)
        e.send(self.recipients)
        sent_message = smtp_mock.send_message.call_args[0][0]
        self.assertEqual(sent_message['From'], self.smtp_config['sender'])
        self.assertEqual(sent_message['To'], ', '.join(self.recipients))
        self.assertEqual(sent_message['Subject'], self.subject)
        self.assertEqual(sent_message.get_content().strip(), self.body)


    def test_unspecified_body_does_not_raise_exception(self, smtp_mock):
        self._prepare_smtp_mock(smtp_mock)
        email = emails.Email(self.smtp_config, self.subject)
        email.send(self.recipients)


    def test_unspecified_subject_does_not_generate_header(self, smtp_mock):
        self._prepare_smtp_mock(smtp_mock)
        email = emails.Email(self.smtp_config, body=self.body)
        email.send(self.recipients)
        sent_message = smtp_mock.send_message.call_args[0][0]
        self.assertNotIn('Subject', sent_message.keys())


    def test_body_type_is_passed_to_set_content(self, smtp_mock):
        self._prepare_smtp_mock(smtp_mock)
        body = '<p>Test body</p>'
        email = emails.Email(self.smtp_config, body=body, body_type='html')
        email.send(self.recipients)
        sent_message = smtp_mock.send_message.call_args[0][0]
        self.assertEqual(sent_message.get_content().strip(), body)
        self.assertIn('text/html', sent_message['Content-Type'])


    def test_can_use_recipient_as_string_instead_of_list(self, smtp_mock):
        self._prepare_smtp_mock(smtp_mock)
        email = emails.Email(self.smtp_config)
        email.send('person1@example.com')
        sent_message = smtp_mock.send_message.call_args[0][0]
        self.assertEqual(sent_message['To'], 'person1@example.com')


    @patch('email.message.EmailMessage.add_attachment')
    def test_attachments_are_added(self, add_attachment_mock, smtp_mock):
        self._prepare_smtp_mock(smtp_mock)
        email = emails.Email(self.smtp_config, attachments=self.attachments)
        email.send(self.recipients)
        expected_calls = []
        for attachment in self.attachments:
            content = attachment['content']
            filename = attachment['filename']
            mime_type = mimetypes.guess_type(filename)
            maintype, subtype = mime_type[0].split('/')
            expected_calls.append(call(content, maintype=maintype, subtype=subtype, filename=filename))
        self.assertEqual(add_attachment_mock.mock_calls, expected_calls)


    @patch('email.message.EmailMessage.add_attachment')
    def test_attachment_mimetype_is_used_if_specified(self, add_attachment_mock, smtp_mock):
        self._prepare_smtp_mock(smtp_mock)
        attachment = {
            'filename': 'README',
            'content': b'example readme',
            'mime_type': 'text/plain'
        }
        email = emails.Email(self.smtp_config, attachments=[attachment])
        email.send(self.recipients)
        add_attachment_mock.assert_called_once_with(b'example readme', maintype='text', subtype='plain', filename='README')


    def test_retries_on_timeout(self, smtp_mock):
        self._prepare_smtp_mock(smtp_mock)
        smtp_mock.send_message.side_effect = [socket.timeout, socket.timeout, None]
        email = emails.Email(self.smtp_config)
        email.send(self.recipients)
        self.assertEqual(smtp_mock.send_message.call_count, 3)


    def test_does_not_exceed_retry_attempt_threshold(self, smtp_mock):
        self._prepare_smtp_mock(smtp_mock)
        smtp_mock.send_message.side_effect = [socket.timeout, socket.timeout, socket.timeout]
        email = emails.Email(self.smtp_config)
        with self.assertRaises(socket.timeout):
            email.send(self.recipients)


    def test_can_specify_retry_threshold(self, smtp_mock):
        self._prepare_smtp_mock(smtp_mock)
        smtp_mock.send_message.side_effect = [socket.timeout, socket.timeout, socket.timeout, None]
        email = emails.Email(self.smtp_config)
        email.send(self.recipients, max_retries=3)
        self.assertEqual(smtp_mock.send_message.call_count, 4)


    def _prepare_smtp_mock(self, smtp_mock):
        smtp_mock.return_value = smtp_mock
        smtp_mock.__enter__.return_value = smtp_mock