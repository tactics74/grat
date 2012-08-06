"""
File: testall.py 
test file for quick development
"""
from grat import *
from urllib2 import *

def main():
    webpage = parser.Page("http://localhost/etc/parsetest.html")
    print webpage.html.content[1].content[1]

if __name__ == "__main__":
    main()
