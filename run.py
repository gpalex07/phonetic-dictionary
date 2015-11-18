import argparse
import gzip
import os
import PDBUtils
import pdbparser
import sys


# Parse the arguments to get the output directory where the dictionary must be created
parser = argparse.ArgumentParser(description='This Python script is a crawler/parser that ' \
                        'extracts phonetic transcriptions of french words from fr.wiktionary.org.')
group = parser.add_argument_group('mandatory arguments')
group.add_argument('-o', '--output_dir', help='output directory where the dictionary will be created', required=True)
args = parser.parse_args()

# Run the Phonetic Dictionary Builder
#entries_file_name = PDBUtils.GetLatestWiktionaryDump(PDBUtils.WikiLang.fr, args.output_dir)
entries_file_name = './tmp/frwiktionary-20151102-all-titles.gz'

# Pick the next word in the wiktionary entries
print
print 'Wiktionary entries saved in', entries_file_name
print 'Extracting the archive'
print 'Loading each word\'s phonetic'


dict_filename = 'phonetic_dictionary_'+PDBUtils.WikiLang.fr+'.txt'
dict_file = open(dict_filename, 'a')

# Extract the entries list, since they are stored in a .gz
with gzip.open(entries_file_name, 'r', 'utf-8') as entries_file:
   for word in entries_file:
      word = word.replace('\n', '')
      #sys.stdout.write('\rProcessing word' + word)
      #sys.stdout.flush() # important
      print '\r                                              ',
      print '\r' + word,
      #print 'current word', word,
      
      page_url = pdbparser.buildWiktionaryPageLink(word)
      page_html = pdbparser.getHtmlFromUrl(page_url)
      
      # Eg. fr.wiktionary contains pages for spanish words
      # we can choose to ignore foreign words
      #if pdbparser.isWordLangageIgnored(word, page_html):
      #   continue
         
      phonetic = pdbparser.findPhoneticInHtml(page_html)
      formatted_res = word+'_'+phonetic+'\n'
      dict_file.write(formatted_res)
      dict_file.flush()
      os.fsync(dict_file.fileno())
 
#PDBUtils.Pick()



dict_file.close()