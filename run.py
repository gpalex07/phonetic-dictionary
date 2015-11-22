import argparse
from decimal import Decimal
import gzip
import os
import PDBUtils
import pdbparser
import sys
from time import time


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
processed_entries = 0
num_entries = 0
remaining_time_refresh_rate = 10 # refresh remaining time message every 10 words.

# Extract the entries list, since they are stored in a .gz
with gzip.open(entries_file_name, 'r', 'utf-8') as entries_file:
   num_entries = sum(1 for line in entries_file)
   entries_file.seek(0)
   begin_time = time()
   prec_time = begin_time
   message = ''
   
   for word in entries_file:
      processed_entries = processed_entries + 1
      word = word.replace('\n', '')
	  # Clears the previous word.
      percentage_str = '[%3.3f%%]' % (Decimal(processed_entries*100)/num_entries)
      #print '\rProcessing word ('+str(processed_entries)+'/'+str(num_entries)+') '+percentage_str+' : '+word,
            
      # Print remaining time every n words
      congruance = processed_entries % remaining_time_refresh_rate
      if congruance == 0:
         current_time = time()
         diff = current_time-prec_time
         num_remaining_words = num_entries-processed_entries
         remaining_time_sec = num_remaining_words/remaining_time_refresh_rate*diff
         mr, sr = divmod(remaining_time_sec, 60)
         hr, mr = divmod(mr, 60)
         dr, hr = divmod(hr, 24)

         total_elapsed_sec = current_time - begin_time
         me, se = divmod(total_elapsed_sec, 60)
         he, me = divmod(me, 60)
         de, he = divmod(he, 24)
         
         message = '\rRemaining time: [%dd:%dh:%02dm:%02ds], elapsed time: [%dd:%dh:%02dm:%02ds]' % (dr, hr, mr, sr, de, he, me, se)
         #print '\nRemaining time: [%d:%02d:%02d], elapsed time: [%d:%02d:%02d]]' % (hr, mr, sr, he, me, se)
         prec_time = current_time
      elif congruance > 2:
         print '\r                                                                                                      ',
         message = '\r%d/%d %s: %s' % (processed_entries, num_entries, percentage_str, word)
      print message,
      
      
      
      
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