#########################################################################
# \brief Phonetic Dictionary Builder Utils.
# \author PaG
# \data 2015-11-11
#########################################################################

from BeautifulSoup import BeautifulSoup, SoupStrainer
from decimal import Decimal
import os
import requests
import urllib
import urllib2
from urlparse import urljoin

# Langages of the wiktionary
class WikiLang:
   fr = 'fr'

# The url of the page that stores the location of the wiki dumps
dumps_url = "https://dumps.wikimedia.org/backup-index.html"

#########################################################################
# \brief Download a file from its url
# \author http://stackoverflow.com/a/22776/2270052
#########################################################################
def download_file(url, output_dir):
   file_name = url.split('/')[-1]
   file_path = os.path.abspath(os.path.join(output_dir,file_name))
   u = urllib2.urlopen(url)
   f = open(file_path, 'wb')
   meta = u.info()
   file_size = int(meta.getheaders("Content-Length")[0])
   print "Downloading '%s' Size: %s MB" % (file_name, Decimal(10*file_size/1024/1024)/10)

   file_size_dl = 0
   block_sz = 8192
   while True:
       buffer = u.read(block_sz)
       if not buffer:
           break

       file_size_dl += len(buffer)
       f.write(buffer)
       status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
       status = status + chr(8)*(len(status)+1)
       print status,

   f.close()
   return file_path

#########################################################################
# \brief The page https://dumps.wikimedia.org/backup-index.html contains 
#        the urls of the latests dumps of the wikis.
#        This functions extracts the url of the french wiktionary dump.
# \author PaG
#########################################################################
def GetLatestWiktionaryDump(wiki_lang, output_dir):
   if not os.path.exists(output_dir):
      print "Error: output_dir argument: path does not exist"
      return

   # Load the page containing th location of the wikis dump
   print 'Loading \''+dumps_url+'\''
   page = urllib.urlopen(dumps_url).read()
   
   # Find the link to the dump for the wiki titled 'frdictionary' for example
   wikiname = wiki_lang+'wiktionary'
   dump_link_found = ''
   for link in BeautifulSoup(page, parseOnlyThese=SoupStrainer('a')):
      if link.text == wikiname:
         dump_link_found = link['href']

   # Converts the relative link to absolute link
   abs_link_dump = urljoin(dumps_url, dump_link_found)
   timestamp = abs_link_dump.split('/')[-1]
   print '  found one dump for \''+wikiname+'\' (from '+timestamp[:4]+'/'+timestamp[4:6]+'/'+timestamp[6:8]+')'
   
   # Build the link of the wiki dump
   dump_url = 'https://dumps.wikimedia.org/frwiktionary/'+timestamp+'/frwiktionary-'+timestamp+'-all-titles.gz'   
   print 'Loading \''+abs_link_dump+'\''
   print '  found the wiktionary entries file at:'
   print '  '+dump_url
   print 'Preparing the download of the wiktionary entries'
   
   return download_file(dump_url, output_dir)