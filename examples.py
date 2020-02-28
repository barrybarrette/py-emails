import emails


if __name__ == '__main__':

    # Simple Form
    ##########################################
    smtp_config = {
        'sender': '<your email address>',
        'host': 'smtp.example.com'
    }
    email = emails.Email(smtp_config, subject='Hi', body='Lunch tomorrow?')
    email.send('<your recipients>')  # recipients can be a string or a string-yielding iterable


    # Long Form
    ##########################################
    sender = '<your email address>'
    smtp_config = {
        'sender': sender,
        'host': 'smtp.example.com',
        'port': 587, # defaults to 25 if not specified
        'password': input(f'Password for {sender}: ') # Omit password if not needed
    }
    with open('README.md', 'rb') as fp:
        attachment = {
            'filename': 'readme.md',
            'content': fp.read(),
            'mime_type': 'text/markdown' # If not specified, emails will try to guess based on the filename
        }
    email = emails.Email(
        smtp_config,
        subject='howdy',
        body='Lorem Ipsum Lorem Ipsum Lorem Ipsum Lorem Ipsum Lorem Ipsum',
        attachments=[attachment]
    )
    email.send('<your recipients>')
