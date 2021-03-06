from wtforms import ValidationError
import tldextract
import requests
from bs4 import BeautifulSoup
import re


class MessagingURl(object):
    """
    Validates that a URL points at a level 3 UCSC content page
    """

    def __call__(self, form, field):
        messaging_regex = re.compile(r"^http(|s):\/\/emailbuilder.ucsc.edu\/.+")
        ext = tldextract.extract(field.data)
        if ext.domain != 'ucsc':
            raise ValidationError('URL must belong to a UCSC domain')
        r = requests.get(field.data)
        if r.status_code != requests.codes.ok:            
            raise ValidationError('That URL was not found. Perhaps it isn\'t published yet?')
        if r.headers['content-type'] != 'text/html; charset=UTF-8':
            raise ValidationError('That URL does not contain HTML')
        soup = BeautifulSoup(r.content, 'lxml')

        valid = False

        if messaging_regex.match(field.data):
            tables = soup.findAll('table', {'align': 'center', 'summary': 'Email content'})
            if tables is not None:
                valid = True

        if not valid:
            raise ValidationError('URL must be from emailbuilder.ucsc.edu')
