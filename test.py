"""
File: testall.py 
test file for quick development
"""
from grat import *
from urllib2 import *

def main():
    p1 = parser.Element("<p>Hello world!</p>")
    print p1
    print p1.content
    print p1.tag_type

if __name__ == "__main__":
    main()
