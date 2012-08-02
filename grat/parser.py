"""
File: parser.py 
Parser for html code to text
"""
import urllib2
import re

class ArgumentError(Exception):
    """Exception for when an given argument is incorrect
       for a function/class."""
    def __init__(self):
        pass

    def __str__(self):
        return "The given argument is invalid."


class Element(object):
    """Object to hold an HTML element."""
    def __init__(self, value):
        if type(content) == list:
            #assumes tags are in order
            self.start_tag = content[0]
            self.closing_tag = content[-1]
            self.content = content[1:-1]

        if type(content) == str:
            if not value.startswith('<'):
                raise ArgumentError
            if not value.endswith('>'):
                raise ArgumentError

            self.start_tag = content[:content.find('>')]
            self.closing_tag = content[content.find("</"):]
            self.content = content[content.find('>'):
                                   content.find("</")]


        if self.value.count('<') > 1:
            self.content = self.remove_tags()
            self.tag_type = self.get_tag_type()
        else:
            self.content = None
            self.tag_type = None

    def __str__(self):
        return self.content


class Page(object):
    """Object to hold a HTML page."""
    def __init__(self, url):
        try:
            self.name = url
            opener = urllib2.build_opener()
            opener.addheaders = [('User-agent', 'Mozilla/5.0')]
            response = opener.open(url)
            self.value = response.read()
            self.parse_html()
        except urllib2.URLError, e:
            print e.reason

    def parse_html(self):
        """Parses self.value into a list of elements"""
        if self.value == None:
            print "Error: ", self.name, " has a null value."

        prev_tags = []
        future_tags = find_all_tags(url)
        for each_tag in future_tags:
            if each_tag.startswith("</"):
                curr_element_tags = []
                while True:
                    popped_tag = prev_tags.pop()
                    curr_element_tags.append(popped_tag.reverse())
                    if find_tag_type(popped_tag) == find_tag_type(each_tag):
                        prev_tags.append( Element(curr_element_tags) )
                        break

            else:
                prev_tags.append(each_tag)






