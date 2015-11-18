#########################################################################
# \brief Phonetic Dictionary Builder parser.
# \author PaG
# \data 2015-11-11
#########################################################################

import urllib
from BeautifulSoup import BeautifulSoup

ERROR_MSG_MISSING_PHONETIC = "PHONETIC-INDISPONIBLE"

#########################################################################
# \brief Returns the link to the wiktionary page of the input \a word.
# \author PaG
# \data 2015-11-11
#########################################################################
def buildWiktionaryPageLink(word):
   base_url = 'https://fr.wiktionary.org/wiki/'
   return base_url+word

#################################################################
# \brief Returns the html of the page specified by the \a url.
# \version 2015-11-06 PaG: Created
#################################################################
def getHtmlFromUrl(url):
   response = urllib.urlopen(url)
   # finds the encoding of the response
   encoding = response.headers['content-type'].split('charset=')[-1]
   html = response.read()
   try:
      html = unicode(html, encoding)
   except:
      print 'Error: getHtmlFromUrl: failure on url=', url
   return html
   
#########################################################################
# \brief Loads a wiktionary page and returns the phonetic inside that page.
# \author PaG
# \data 2015-11-11
#########################################################################
def findPhoneticInHtml(wiktionary_page_html):
   parsed_html = BeautifulSoup(wiktionary_page_html)   
   span_prononciation = parsed_html.body.find('span', {'title': 'prononciation API'})
   
   if (span_prononciation == None):
      return ERROR_MSG_MISSING_PHONETIC
   
   phonetic_transcription = span_prononciation.text
   # remove the slashes surrounding the phonetic transcription
   cleaned_str = phonetic_transcription
   #cleaned_str = cleaned_str.replace('/', '').replace('\\', '')
   return cleaned_str.encode('utf-8')
   
#########################################################################
# \brief For example, fr.wiktionary contains pages no french words.
#        This function allows ignoring such words/pages.
# \author PaG
# \data 2015-11-11
#########################################################################
def isWordLangageIgnored(word, wiktionary_page_html):
   parsed_html = BeautifulSoup(wiktionary_page_html)
   span_sectionlangue = parsed_html.body.find('span', {'class': 'sectionlangue'})
   # If the langage section is absent it means its a native langage word
   # (ie. if the page is from fr.wiktionary.org, that it's a french word)
   if span_sectionlangue == None:
      return False
   
   print word, 'is ignored;', span_sectionlangue.find('a', href=True), 'word'
   return True
   