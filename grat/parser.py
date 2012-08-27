"""
File: parser.py
Parser for html code to text
"""
import urllib2
import re
import time

#global start_time
#start = time.time()

class ArgumentError(Exception):
    """Exception for when an given argument is incorrect
for a function/class."""
    def __init__(self):
        pass

    def __str__(self):
        return "The given argument is invalid."


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
                    exp_tags.append(element.expand())
                exp_tags.append(item.closing_tag)
            
            else: exp_tags.append(item)       
             
        exp_tags.append(self.closing_tag)
        #print exp_tags, '\n'
        return exp_tags
    

    def flatten(self, lyst):
        """Returns a flattened list; maintains explicit ordering."""
        flat_lyst = []
        for item in lyst:
            if type(item) == list:
                flat_lyst.extend(self.flatten(item))
            else:
                flat_lyst.append(item)
                
        return flat_lyst

      
    def print_styled(self, lyst):
        """Returns stylized html element in string form"""
        lyst = self.flatten(lyst)
        
        indent = 0
        index = 0
        space  = " " * 2
        while True:
            temp = lyst[index]
            #print "This is temp" , temp
            #print indent
            #print "Before: ", lyst[index]        
            lyst[index] = (space * indent) + lyst[index] + '\n' 
            #print "After: ", lyst[index]

            if temp.endswith("/>"):
                pass
                
            elif temp.startswith("</"):
                    #print "</"
                indent -= 1
                  
            elif temp.startswith("<"):
                    #print "<"
                indent += 1

            else: pass
            
            index += 1
            if index > len(lyst) -1:
                break
        #print time.time() - start
        return " ".join(lyst)
    

    def get_children(self):
        """Gets all Element objects inside self.content."""
        elements = list()
        
        for item in self.content:
            if type(item) == Element:
                elements.append(item)
               
        return elements
    

    def print_stats(self):
        print "Start tag: ", str(self.start_tag)
        print "Closing tag: ", str(self.closing_tag)
        print "Content: ", str(self.content)

    def __str__(self):
        return self.expand()


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
            #self.value = "<html><body><p>hello world</p></body></html>"
            #self.value = '<html><head><script type="text/javascript">document.write("hello world")</script></head><body><p>hello world</p></body></html>'
            self._parse_html()
        except urllib2.URLError, e:
            print e.reason

    def _parse_html(self):
        """Parses self.value into a list of elements"""
        if self.value == None:
            print "Error: ", self.name, " has a null value."
            
        self.find_doctype()
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


    def find_doctype(self):
        pattern = re.compile("<\s*!DOCTYPE|doctype .*>")
        self.doctype = pattern.match(self.value)
        if self.doctype != None:
            self.doctype = self.doctype.group(0)
            self.value = self.value[self.value.find(">") + 1:]
            

    def find_all_tags(self, stryng):
        """Returns all tags in a stryng"""
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
    

    def find_all_text(self):
        """Returns all text inside any of the body."""
        #============ Pesudo ====================
        # Note: This won't work completely bc some
        # text can be found inside a tag so it 
        # needs work.
        #========================================
        # find body content
        # remove scipt elements
        # remove all tags
        # return ' '.join( whats left )
        #========= End of Pesudo =================
        pass
    

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
        return self.html.print_styled(self.html.expand())
