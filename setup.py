from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='py-emails',
    version='0.0.1',
    author='Barry Barrette',
    author_email='barrybarrette@gmail.com',
    description='Simple wrapper around email and smtplib for composing and sending email messages in an intuitive, simple interface.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/whitebarry/py-emails',
    packages=find_packages(),

)