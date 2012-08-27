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
    webpage = parser.Page("www.python.org")
    save( str(webpage) )

if __name__ == "__main__":
    main()
