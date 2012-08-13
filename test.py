"""
File: testall.py 
test file for quick development
"""
from grat import *
from urllib2 import *

def main():
    webpage = Parser.Page("http://localhost/etc/parsetest.html")
    print webpage.html

if __name__ == "__main__":
    main()
