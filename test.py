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
    #save( webpage.find_all_text() )
    #print webpage.find_all_links()
    #print webpage.find_all_images()
    print webpage.find_all_sentences()
if __name__ == "__main__":
    main()
