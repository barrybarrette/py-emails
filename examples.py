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

    # HTML Body Type Example
    ##########################################
    html_body = """\
        <html>
          <head>
            <style>
                .button {
                  border: none;
                  color: white;
                  padding: 15px 32px;
                  text-align: center;
                  text-decoration: none;
                  display: inline-block;
                  font-size: 16px;
                  margin: 4px 2px;
                  cursor: pointer;
                  background-color: #4CAF50;
                }
            </style>
          </head>
          <body>
            <h1>Sample Heading</h1>
            <p>Sample Paragraph</p>
            <b>Bold Message</b><br>
            <a href="https://www.python.org/"><input class="button" type=button value='Go to Python Website'></a>
          </body>
        </html>
    """
    email = emails.Email(smtp_config,
                         subject='HTML in body example',
                         body=html_body,
                         body_type="html")
    email.send('<your recipients>')  # recipients can be a string or a string-yielding iterable

    # HTML Body Type Example with Template
    ##########################################
    template = {
        'smtp_config': smtp_config,
        'subject': "HTML in body example",
        'body': html_body,
        'body_type': "html"
    }
    email = emails.from_template(template)
    email.send('<your recipients>')  # recipients can be a string or a string-yielding iterable
