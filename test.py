"""
File: testall.py 
test file for quick development
"""
from grat import *
from urllib2 import *

def save(content):
    out = open("test.txt", 'w')
    out.write( content )
    out.close()

def main():
    webpage = parser.Page("http://en.wikipedia.org/wiki/Ovid")
    save( webpage.find_all_text() )

if __name__ == "__main__":
    main()
