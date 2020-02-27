# py-emails
Simple wrapper around `email` and `smtplib` for composing and sending email messages in an intuitive, simple interface.
Pure python, no dependencies outside of the standard library


## Installation and use
Install with pip or your favorite package manager: `pip install py-emails`


Emails can be created declaratively:
```
from emails import Email

first_attachment = {
    'filename': 'example.png', 
    'content': open('example.png', 'rb').read()
}
other_attachment = {
    'filename': 'example.csv', 
    'content': open('example.csv', 'rb').read()
}
my_email = Email(
    sender='me@example.com', 
    subject='How are you?'
    body='Long time no see, we should get together!',
    attachments=[first_attachment, other_attachment]
)
```

Or using a template dictionary:
```
from emails import from_template

first_attachment = {
    'filename': 'example.png', 
    'content': open('example.png', 'rb').read()
}
other_attachment = {
    'filename': 'example.csv', 
    'content': open('example.csv', 'rb').read()
}
template = {
    'sender': 'me@example.com',
    'subject': 'How are you?',
    'body': 'Long time no see, we should get together!',
    'attachments': [first_attachment, other_attachment]
}
my_email = from_template(template)
```

Once you have the email object, sending it is as simple as specifying recipient(s) and an SMTP host:

```
recipients = ['person1@example.com', 'person2@example.com']
my_email.send(recipients, 'smtp.example.com')
my_email.send('person3@example.com', 'smtp.example.com')
```

