"""
File: parser.py 
Parser for html code to text
"""
import urllib2

class ArgumentError(Exception):
    """Exception for when an given argument is incorrect
       for a function/class."""
    def __init__(self):
        pass

    def __str__(self):
        return "The given argument is incorrect."


class Element(object):
    """Object to hold an HTML element."""
    def __init__(self, value):
        if not value.startswith('<'):
            raise ArgumentError
        if not value.endswith('>'):
            raise ArgumentError

        self.value = value
        self.content = self.remove_tags()
        self.tag_type = self.get_tag_type()

    def get_tag_type(self):
        return self.value.split('<')[2][1:-1] #get end tag and remove <,/,and >

    def remove_tags(self):
        """Removes starting and ending tags of a element."""
        stryng = self.value.split('>', 1)[1]
        stryng = stryng.split('<', 1)[0]
        return stryng.strip()

    def __str__(self):
        return self.value


class Page(object):
    """Object to hold a HTML page."""
    def __init__(self, url):
        try:
            opener = urllib2.build_opener()
            opener.addheaders = [('User-agent', 'Mozilla/5.0')]
            response = opener.open(url)
            self.value = response.read()
        except urllbi2.URLError, e:
            print e.reason

    def parse_html(self):
        pass