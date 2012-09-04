"""
File: parser.py
Parser for html code to text
"""
import urllib2
import re
#import time

#global start_time
#start = time.time()

class ArgumentError(Exception):
    """Exception for when an given argument is incorrect
for a function/class."""
    def __init__(self):
        pass

    def __str__(self):
        return "The given argument is invalid."


def flatten(lyst):
    """Returns a flattened list; maintains explicit ordering."""
    flat_lyst = []
    for item in lyst:
        if type(item) == list:
            flat_lyst.extend(flatten(item))
        else:
            flat_lyst.append(item)
            
    return flat_lyst



class Element(object):
    """Object to hold an HTML element.  If content is a list then index 0 will 
    be start tag, index -1 will be closing tag, and the remaining will be the 
    content of the element.  If content is a string than it must start with a 
    < and end with a >."""
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

    def __getitem__(self, key):
        return self.content[key]
    

    def __iter__(self):
        for item in flatten( self.expand() ):
            yield item

    def startswith(self, str):
        if self.content != None:
            return self.content.startswith(str)
        return -1

    def expand(self):
        """Returns a list that contains the expanded version of self.content"""
        exp_tags = []
        exp_tags.append(self.start_tag)
        
        for item in self.content:
            if type(item) == Element:
                exp_tags.append(item.start_tag)
                lyst = item.get_children()
                for element in lyst:
                    if type(element) == Element:
                        exp_tags.append(element.expand())
                    else:
                        exp_tags.append(element)

                exp_tags.append(item.closing_tag)
            
            else: exp_tags.append(item)       
             
        exp_tags.append(self.closing_tag)
        #print exp_tags, '\n'
        return exp_tags

    def expand_with_style(self, indent = 0):
        """Returns a list that contains a expanded, flattened, and styled 
        version of self.content"""
        exp_tags = []
        tab = ' ' * 2

        exp_tags.append( (tab * indent) + self.start_tag + '\n')
        indent += 1
        for item in self.content:
            if type(item) == Element:
                exp_tags.append( (tab * indent) + item.start_tag + '\n')
                lyst = item.get_children()
                for element in lyst:
                    if type(element) == Element:
                        exp_tags.append( element.expand_with_style(indent + 1) )
                    else:
                        exp_tags.append( (tab * indent) + element + '\n')

                exp_tags.append( (tab * indent) + item.closing_tag + '\n')

            else: exp_tags.append( (tab * indent) + item + '\n')

        indent -= 1
        exp_tags.append( (tab * indent) + self.closing_tag + '\n')
        return ''.join( exp_tags )
      
    def print_styled(self):
        """Returns stylized html element in string form"""
        lyst = self.expand()
        lyst = flatten(lyst)
        
        indent = -1
        index = 0
        space  = " " * 2
        while True:
            temp = lyst[index]

            if temp.startswith("</"):
                indent -= 1                  
            elif temp.startswith("<"):
                indent += 1
            else:
                indent += 1

            lyst[index] = (space * indent) + lyst[index] + '\n' 
            
            index += 1
            if index > len(lyst) -1:
                break
            
        return "".join(lyst)
    

    def get_children(self):
        """Gets all objects inside self.content."""               
        return [item for item in self.content]
    

    def print_stats(self):
        print "Start tag: ", str(self.start_tag)
        print "Closing tag: ", str(self.closing_tag)
        print "Content: ", str(self.content)

    def __str__(self):
        return self.expand_with_style()


class Page(object):
    """Object to hold a HTML page."""
    def __init__(self, url):
        try:
            if not url.startswith("http://"):
                url = "http://" + url
                
            self.name = url
            opener = urllib2.build_opener()
            opener.addheaders = [('User-agent', 'Mozilla/5.0')]
            response = opener.open(url)
            self.value = response.read()
            #self.value = "<html><head></head><body><a><img src='idk.jpg' /></a><p>Hello world</p></body></html>"
            #self.value = '<html><head><script type="text/javascript"><script type="text/javascript">if(window.mw){mw.loader.load(["mediawiki.user","mediawiki.page.ready","mediawiki.legacy.mwsuggest","ext.gadget.teahouse","ext.gadget.ReferenceTooltips","ext.vector.collapsibleNav","ext.vector.collapsibleTabs","ext.vector.editWarning","ext.vector.simpleSearch","ext.UserBuckets","ext.articleFeedback.startup","ext.articleFeedbackv5.startup","ext.markAsHelpful","ext.Experiments.lib","ext.Experiments.experiments"], null, true);}</script></script></head><body><p>hello world</p></body></html>'
            self._parse_html()
        except urllib2.URLError, e:
            print e.reason

    def _parse_html(self):
        """Parses self.value into a list of elements"""
        if self.value == None:
            print "Error: ", self.name, " has a null value."
            
        self.find_doctype()
        prev_tags = []
        future_tags = self.find_all_tags()
        #This giant loop creates elements out of the tags found from 
        #self.find_all_tags(self.value)
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
        # end of gaint loop to create elements

        self.html = prev_tags[0]
        self.head = self.html[0]
        self.body = self.html[1]

    def find_doctype(self):
        pattern = re.compile("<\s*!DOCTYPE|doctype .*>")
        self.doctype = pattern.match(self.value)
        if self.doctype != None:
            self.doctype = self.doctype.group(0)
            self.value = self.value[self.value.find(">") + 1:]
            

    def find_all_tags(self):
        """Returns all tags in a stryng"""
        tags = []
        stryng = self.value
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
    

    def find_all_text(self):
        """Returns all text inside any of the body."""
        # expand all elements
        no_tags = self.body.expand()

        # flatten list
        no_tags = flatten(no_tags)
        temp = list() # need because popping no_tags will cause skips

        # remove all tags
        index = 0
        while True:
            if index >= len(no_tags):
                break

            if no_tags[index].startswith( '<' ):
                if no_tags[index].find( "script" ) != -1:
                    index += 1 # skip the contents of scripts

                if no_tags[index].find( "style" ) != -1:
                    index += 1 # skip the contents of styles

            else:
                temp.append(no_tags[index])

            index += 1

        return ' '.join( temp )


    def find_all_sentences(self, include_anchors = False):
        """Finds all the sentences in the html and if include_anchors is True
        it will create a list with index 0 containing the url and index 1 
        containing the text found in the anchor.
        TODO: create lists from text tokens found"""
        anchor_found = list()
        sentences = list()
        index = 0
        pattern = re.compile("href\s*=\s*[\"'].+[\"']") #pattern for href
        content_lyst = flatten( [item for item in self.body] )

        while True:
            if index >= len(content_lyst):
                break

            # if the item is the start of an a tag
            if include_anchors and content_lyst[index].startswith("<a"):
                href = pattern.findall(content_lyst[index])
                if href:
                    href = href[0].split('=')[1].split()[0]
                    anchor_found = [ href ] #Ensures
                        # that there is not extra text with href
                else:
                    anchor_found = [ '' ] # placeholder so href is alway index 1

                index += 1
                temp = list()
                # loop through to find all text contained in the anchor
                while True:
                    if content_lyst[index].startswith('<a'):
                        break

                    if content_lyst[index].startswith('<'):
                        pass
                    else:
                        temp.append( content_lyst[index] ) # content
                    index += 1

                anchor_found.append( ' '.join(temp) ) # all text inside a tags
                sentences.append( anchor_found )
                anchor_found = list()

            # if item starts with a < we don't need it
            elif content_lyst[index].startswith("<"):
                if content_lyst[index].find( "script" ) != -1:
                    index += 1 # skip the contents of scripts

                if content_lyst[index].find( "style" ) != -1:
                    index += 1 # skip the contents of styles

            else:
                sentences.append( content_lyst[index] )

            index += 1

        return sentences

    def get_children(self):
        """Wraper to to pass html to get_children"""
        return self.html.get_children()


    def find_tag_type(self, tag):
        """Returns tag stripped of angle brackets and forward slash"""
        if type(tag) == Element:
            return None

        if tag.startswith('</'):
            return tag[2:-1].split()[0]
        
        if tag.startswith('<'):
            return tag[1:-1].split()[0]
        
        else: return tag

    def __str__(self):
        return str(self.html)
