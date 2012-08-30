Grat
===========

Python web scraper

===========

Usage:
    >>> from grat import *
    >>> webpage = parser.Page(<webpage url>)
    >>> print webpage.html

    Output:
        A string containing the html code of the webpage located at the given 
        webpage url.

===========

Install:
    Just copy the grat folder into your project project then add "from grat 
    import *" to the top of any file you wish to use this project in.

===========

Modules:
Grat:
    -Grat.parser:
        -Grat.flatten(list):
            Returns a flattened list; maintains explicit ordering.

        -Grat.Parser.Element(string/list):
            Object to hold an HTML element.  If content is a list then 
            index 0 will be start tag, index -1 will be closing tag, and 
            the remaining will be the content of the element.  If content
            is a string than it must start with a < and end with a >.

            Methods:
                -Element.startswith(string):
                    Runs the built-in function startswith with the arguments 
                    of the elements contents and the string given.

                -Element.expand():
                    Returns a list with all elements expanded to their string
                    form.  Example: a <p element> might expand to 
                    <p>Hello world!</p> (text inside tags will vary).

                -Element.expand_with_style():
                    Returns a list that contains a expanded, flattened, and styled 
                    version of self.content

                -Element.print_styled():
                    Returns stylized html element in string form.

                -Element.get_children():
                    Returns all Element objects found in the contents of this
                    Element.

                -Element.print_stats():
                    Prints element in a more readable way and does not expand 
                    the contents of the element.  Mainly used for debugging.

        -Grat.Parser.Page(string):
            Object to hold a HTML page.  Accepts the url of a webpage as an 
            argument.

            Methods:
                -Page.find_doctype():
                    Returns the doctype of the web page.

                -Page.find_all_tags(string):
                    Returns all tags in a stryng

                -Page.find_tag_type(string):
                    Returns the tag type of string.  If string object is a 
                    Element object None will be returned.  If the tag type of
                    the string can not be found the string will be returned.

                -Page.find_all_text():
                    Returns all text inside any of the body.

                -Page.get_children():
                    Wraper to to pass html to Element.get_children.


