"""
File: testall.py 
test file for quick development
"""
from grat import *
from urllib2 import *

def main():
    webpage = parser.Page("http://www.python.org")
    for tag in webpage.tags:
        print tag, "\n\n"

if __name__ == "__main__":
    main()
