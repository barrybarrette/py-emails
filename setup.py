from setuptools import setup, find_packages

with open('README.md', 'r') as readme_file:
    long_description = readme_file.read()

setup(
    name='py-emails',
    version='1.2.1',
    author='Barry Barrette',
    author_email='barrybarrette@gmail.com',
    description='Simple wrapper around email and smtplib standard libraries for composing and sending email messages in an intuitive, simple interface.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/barrybarrette/py-emails',
    packages=find_packages()
)
