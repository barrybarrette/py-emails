# py-emails
[![Build Status](https://travis-ci.com/barrybarrette/py-emails.svg?branch=master)](https://app.travis-ci.com/github/barrybarrette/py-emails)
[![Coverage Status](https://coveralls.io/repos/github/barrybarrette/py-emails/badge.svg?branch=master)](https://coveralls.io/github/barrybarrette/py-emails?branch=master)


Simple wrapper around `email` and `smtplib` for composing and sending email messages in an intuitive, simple interface.
Pure python, no dependencies outside of the standard library


## Installation and use
Install with pip or your favorite package manager: `pip install py-emails`


Emails can be created declaratively:
```python
from emails import Email

smtp_config = {
    'sender': 'you@example.com',
    'host': 'smtp.example.com'
}

first_attachment = {
    'filename': 'example.png', 
    'content': open('example.png', 'rb').read()
}
other_attachment = {
    'filename': 'example.csv', 
    'content': open('example.csv', 'rb').read()
}
my_email = Email( 
    smtp_config, 
    subject='How are you?',
    body='Long time no see, we should get together!',
    attachments=[first_attachment, other_attachment]
)
```

Or using a template dictionary:
```python
from emails import from_template

smtp_config = {
    'sender': 'you@example.com',
    'host': 'smtp.example.com',
    'port': 587,
    'password': '<secret password>'
}
template = {
    'smtp_config': smtp_config,
    'subject': 'How are you?',
    'body': 'Long time no see, we should get together!'
}
my_email = from_template(template)
```


Once you have the email object, sending it is as simple as specifying one or more recipients:
```python
import emails

smtp_config = {
    'sender': 'you@example.com',
    'host': 'smtp.example.com'
}
my_email = emails.Email(smtp_config)
my_email.send('person1@example.com')
my_email.send(['person2@example.com', 'person3@example.com'])
```

See `examples.py` for more in depth use cases


# Contributing
See [CONTRIBUTING.md](CONTRIBUTING.md)