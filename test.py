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
<<<<<<< HEAD
    webpage.find_all_sentences(True)
    #save( '\n'.join( webpage.find_all_sentences(False) ) )

=======
    #save( webpage.find_all_text() )
    #print webpage.find_all_links()
    #print webpage.find_all_images()
    print webpage.find_all_sentences()
>>>>>>> d5f8b890c93fd84def0305bcdf66810ac8b85578
if __name__ == "__main__":
    main()
