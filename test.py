"""
File: testall.py 
test file for quick development
"""
from grat import *
from urllib2 import *

def main():
    webpage = parser.Page("http://www.python.org")
    webpage.parse_html()
    for el in webpage.tags:
        print el.content
        print '=' * 25

if __name__ == "__main__":
    main()
