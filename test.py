"""
File: testall.py 
test file for quick development
"""
from grat import *
from urllib2 import *

def main():
    webpage = parser.Page("www.python.org")
    out = open("test.txt", 'w')
    out.write( str(webpage) )
    out.close()

if __name__ == "__main__":
    main()
