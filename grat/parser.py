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
    def __init__(self, content):
        if content == None:
            self.content = None
        else:
            if type(content) == list:
                #assumes tags are in order
                self.start_tag = content[0]
                self.closing_tag = content[-1]
                self.content = content[1:-1]
                self.tag_type = self.closing_tag[2:-1].split()[0]

            if type(content) == str:
                if not content.startswith('<'):
                    raise ArgumentError
                if not content.endswith('>'):
                    raise ArgumentError

                self.start_tag = content[:content.find('>')]
                self.closing_tag = content[content.find("</"):]
                self.content = content[content.find('>'):
                                       content.find("</")]
                self.tag_type = self.closing_tag[2:-1].split()[0]

    def startswith(self, str):
        if self.content != None:
            return self.content.startswith(str)
        return -1

    def expand(self):
        """Returns a string that contains the expanded version of self.content.
By expanded version we mean that all element objects inside
self.content will be in there string form."""
        pass

    def print_stats(self):
        print "Start tag: ", str(self.start_tag)
        print "Closing tag: ", str(self.closing_tag)
        print "Content: ", str(self.content)

    def __str__(self):
        return str(self.start_tag) + str(self.content) + str(self.closing_tag)


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
        future_tags = self.find_all_tags(self.value)
        for each_tag in future_tags:
            if each_tag.startswith("</"):
                curr_element_tags = []
                while True:
                    popped_tag = prev_tags.pop()
                    curr_element_tags.append(popped_tag)
                    if self.find_tag_type(popped_tag) == \
                       self.find_tag_type(each_tag):
                        curr_element_tags.reverse()
                        curr_element_tags.append(each_tag)

                        curr_element = Element(curr_element_tags)
                        if curr_element != None:
                            prev_tags.append( curr_element )
                        break

            else:
                prev_tags.append(each_tag)

        self.html = prev_tags[0]

    def find_all_tags(self, stryng):
        """Returns all tags in a list"""
        tags = []
        while True:
            if stryng.strip() == '':
                break
            index = stryng.find('<')

            if index > stryng.find('>'):
                index = stryng.find('>') + 1

            if index == 0:
                index = stryng.find('>') + 1
            
            if stryng[:index].strip() != '':
                tags.append(stryng[:index].strip())

            stryng = stryng[index:]
        return tags
       

    def find_tag_type(self, tag):
        """Returns tag stripped of angle brackets and forward slash"""
        if type(tag) == Element:
            return None

        if tag.startswith('</'):
            return tag[2:-1].split()[0]
        
        if tag.startswith('<'):
            return tag[1:-1].split()[0]
        
        else: return tag
