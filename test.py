#!/usr/bin/python -tt
# -*- coding: utf-8 -*-
import argparse
import PDBUtils
import pdbparser
import re

reload(pdbparser)

from BeautifulSoup import BeautifulSoup, SoupStrainer

# Returns the seciton in the html, corresponding to the fr section
def findSectionByLanguage(html, language):
    parsed_html = BeautifulSoup(html)
    current_lng_section = parsed_html.find('span', {'class': 'sectionlangue', 'id': language})
    if not current_lng_section:
        print 'No \''+language+'\' section'
        #print 'No \''+language+'\' section for \''+word+'\''
        return None
    current_lng_section = current_lng_section.parent
    return current_lng_section

def isH3Section(section):
    return (section.name == 'h3' or section.name == 'H3')

# Section must be at the same depth as the H3 sections we are looking for
def findNextH3Section(h3_section):
    is_H3_section = False
    while not is_H3_section:
        h3_section = h3_section.findNextSibling()
        if h3_section == None:
            break
        is_H3_section = isH3Section(h3_section)
    return h3_section

# Returns true if this h3 section contains no phonetic information
def mustSkipSection(h3_section):
    useless_h3_sections = ['titreetym', 'titrepron', 'titreref', 'titrevoir']
    for useless in useless_h3_sections:
        if h3_section.find('span', {'class': useless}):
            print 'Skipped: \''+useless+'\''
            return True
    return False

def getSectionLangage(h2_section):
    return h2_section.find('span', {'class': 'sectionlangue'}).get('id')

# Returns True if the end of the current langage section has been reached
def endOfCurentLangageSectionReached(h3_section):
    lng_section = h3_section.findPreviousSibling('h2')
    return getSectionLangage(lng_section) != PDBUtils.WikiLang.fr

def getH3SectionId(h3_section):
    h3_section_id = h3_section.findAll('span')[0].get('id')
    return h3_section_id

def getH3SectionTitle(h3_section):
    h3_section_title = h3_section.findAll('span')[0].text.encode('utf-8')
    return h3_section_title

def getH3SectionClass(h3_section):
    h3_section_class = h3_section.findAll('span')[0].get('class')
    return h3_section_class

def isInterestingSectionId(h3_section):
    interesting_section_classes = ['titredef']
    h3_section_class = getH3SectionClass(h3_section)
    return h3_section_class in interesting_section_classes
    #interesting_section_ids = ['fr-nom', 'fr-adj', 'fr-flex-verb', 'fr-interj',
    #'fr-verb', 'fr-flex-adj', 'fr-flex-nom']
    #h3_section_id = getH3SectionId(h3_section)
    #assert h3_section_id in interesting_section_ids, h3_section_id
    #return h3_section_id in interesting_section_ids

def extractPhoneticFromTable(html_phonetic_table):
    html = str(html_phonetic_table)
    search_res = re.findall('\\\\(.+?)\\\\', html)
    return search_res

def extractPhoneticFromParagraph(html_phonetic_paragraph):
    html = str(html_phonetic_paragraph)
    search_res = re.findall('\\\\(.+?)\\\\', html)
    # There may be transcriptions for Quebec
    """
    if len(search_res) > 1:
        lng = html_phonetic_paragraph.find('span').findNextSibling().text
        assert lng == '(France)'
        search_res = [search_res[0]]
    """
    return search_res

# Removes all the special chars from the string
def cleanStr(str):
    cleaned_str = re.sub('[^a-zA-Z0-9\n\.]', ' ', str.decode('utf-8'))
    #cleaned_str = re.sub('[^A-Za-z0-9 ]+', '', str)
    return cleaned_str

def extractPhoneticsInH3Section(h3_section):
    print '-------------------------------------------------------------'
    print getH3SectionTitle(h3_section).upper()
    phonetics = []
    sibling = h3_section.findNextSibling()
    # there is sometimes an empty span after the H3 tag..
    if sibling.name == 'span':
        sibling = sibling.findNextSibling()
    # otherwise, it could be a table containing phonetic
    if sibling.name == 'table':
        phonetic = extractPhoneticFromTable(sibling)
        phonetics = phonetics + phonetic
        sibling = sibling.findNextSibling()
        print len(phonetic), 'transcriptions extracted in table'
    else: print 'No phonetic table found in this section.'
    # anyways, the <p> tag contains a phonetic transcription
    if sibling.name == 'p':
        phonetic = extractPhoneticFromParagraph(sibling)
        phonetics = phonetics + phonetic
        #assert len(phonetic) <= 1 #why would there be several transcriptions here? for Quebec? (cf. word 'OK')
        print len(phonetic), 'transcriptions extracted in paragraph'
    return phonetics

def wikiParser(html):
    phonetics = []
    h3_section = findSectionByLanguage(html, PDBUtils.WikiLang.fr)
    while h3_section:
        h3_section = findNextH3Section(h3_section)
        if h3_section == None:
            break
        if endOfCurentLangageSectionReached(h3_section):
            break
        if not isInterestingSectionId(h3_section):
            print "   '"+cleanStr(getH3SectionTitle(h3_section)).upper()+"' skipped"
            continue

        new_phonetics = extractPhoneticsInH3Section(h3_section)
        phonetics = phonetics + new_phonetics
        #print h3_section

    # remove duplicates
    phonetics = list(set(phonetics))
    return phonetics


#===============================================================
"""
# Parse the arguments to get the output directory where the dictionary must be created
parser = argparse.ArgumentParser(description='This Python script is a crawler/parser that ' \
                        'extracts phonetic transcriptions of french words from fr.wiktionary.org.')
group = parser.add_argument_group('mandatory arguments')
group.add_argument('-w', '--word', help='The word for which transcriptions will be extracted.')
args = parser.parse_args()



#word = 'affluent'
word = 'crisser'
base_url = 'http://127.0.0.1:8000/wiktionary_fr_all_2015-11/'

if args.word:
    word = args.word

page_url = pdbparser.buildWiktionaryPageLinkForKiwix(word, base_url)
page_html = pdbparser.getHtmlFromUrl(page_url)

# Eg. fr.wiktionary contains pages for spanish words
# we can choose to ignore foreign words
#if pdbparser.isWordLangageIgnored(word, page_html):
#   continue

#phonetic = pdbparser.newFindPhoneticInHtml(page_html)
phonetic = wikiParser(page_html)
print '\n', phonetic
"""
