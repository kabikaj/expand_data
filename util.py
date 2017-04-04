#!/usr/bin/env python
#
#     util.py
#
# Utility classes
#
#############################

import os
import pprint as pp
from collections import namedtuple
from configparser import ConfigParser, MissingSectionHeaderError, \
                         ExtendedInterpolation, NoSectionError, NoOptionError

##########################################
# CLASSES
##########################################

class CorpusDoc():
    """ Class representig the data model
        of a documnent of the corpus.

    """
    def __init__(self, text=None, annotation=None):
        """ Constructor.

        Args:
            text (str): text of the document
            annotations (dict): set of instance annotations.
                Each value is a list containing dicts of the form:
                    { "val" : str,
                      "ini" : int,
                      "end" : int }

        """
        self.text = text
        self.annotation = annotation

    def __repr__(self):
        return "<CorpusDoc text:%s annotations:%s>" % (self.text, self.annotation)

    def __str__(self):
        return "Instance of class CorpusDoc:\n\ntext = %s\n\nannotations =\n%s" % (self.text, pp.pformat(self.annotation))

_HadithMeta = namedtuple('_HadithMeta', ['PIDSTART', 'PIDEND', 'BOOKID', 'CHAPTERID', 'SUBCHAPTERID', 'SECTIONID'])

class HadithMeta(_HadithMeta):
    """ Class to store metadata from hadith filenames.

    Attributes:
        PIDSTART (int): pid variable for reconstucting url in start position.
        PIDEND (int): pid variable for reconstucting url in end position.
        BOOKID (int): book that constains document.
        CHAPTERID (int): chapter that constains document.
        SUBCHAPTERID (int): subchapter that constains document.
        SECTIONID (int): section that constains document.

    """
    def __str__(self):
        return """Instance of class HadithMeta:\n \
               PIDSTART = %s\n \
               PIDEND = %s\n \
               BOOKID = %s\n \
               CHAPTERID = %s\n \
               SUBCHAPTERID = %s\n \
               SECTIONID = %s\n \
               """ % (self.PIDSTART,
                      self.PIDEND,
                      self.BOOKID,     
                      self.CHAPTERID,
                      self.SUBCHAPTERID,
                      self.SECTIONID)

class Config():
    """ Configuration constants. """

    def load(cfgpath = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'config.ini'),
             globals = globals()):
        """ Load configuration file.

        Args:
            cfgpath (String): path of configuration file.
            globals (dict): global variables, to keep track of the module path.

        Returns:
            ConfigParser: Object read from configuration file.

        Raise:
            ValueError: if any error is find in config file.

        """
        cfg = ConfigParser(inline_comment_prefixes=('#'), interpolation=ExtendedInterpolation())
        cfg.optionxform = str # make parser case sensitive

        try:
            cfg.read(cfgpath)
            
        except MissingSectionHeaderError:
            raise ValueError('Error in module {__file__}: no sections in config file'.format(**globals))

        if not cfg.sections():
            raise ValueError('Error in module {__file__}: config file missing or empty'.format(**globals))
    
        return cfg
        

##########################################
# SUBROUTINES
##########################################

def getfiles(path):
    """ Generate list of file paths and names from directory path.

    Args:
       path (str): input directory

    Yields:
        str, str: full path of file and name

    """
    fobjs = (f for f in os.scandir(path) if f.is_file())

    for f in fobjs:
        yield (f.path, os.path.splitext(f.name)[0])


def loadmeta_altafsir(madhab_path, tafsir_path):
    """ Load metadata text files for altafsir.

    Args:
        madhab_path (str): path for madhab file.
        tafsir_path (str): path for tafsir file.

    returns:
        dict, dict: madhab metadata and tafsir metadata.

    """
    with open(madhab_path) as fp:
        lines = (li.split('|') for li in filter(None, (l.strip() for l in fp)) if not li.startswith('#'))
        madhab_mapping = {_id.strip() : name.strip() for _id, name in lines}

    with open(tafsir_path) as fp:
        lines = (list(map(str.strip, li.split('|'))) for li in filter(None, (l.strip() for l in fp)) if not li.startswith('#'))
        tafsir_mapping = {_id : {'name':name, 'author':author, 'date':date} for _id, name, author, date in lines}
    
    return madhab_mapping, tafsir_mapping

def parse_hadith_fname(fname):
    """ Extract metadata from fname.

    Example of fname: hadith.al-islam-10904-10907_33-76.json, where
        PIDSTART = 10904
        PIDEND = 10907
        BOOKID = 33
        CHAPTER = 76
        SUBCHAPTERID = None
        SECTION = None

    Args:
        fname (str): file name to parser.

    Return:
        namedtuple: metadata.

    """
    pidrange, _, rest = fname.partition('_')
    bookid, docmeta = (lambda x: (x[0], list(map(int, x[1:]))))(rest.split('-'))
    return HadithMeta(*list(map(int, pidrange.rsplit('-',2)[1:])), bookid, *docmeta, *([None]*(3-len(docmeta))))

#FIXME puta madre! antes habia quedado mejor!!
# metadata = dict(itertools.zip_longest(('pidstart', 'pidend', 'book', 'chapter', 'subchapter', 'section'),
#                                     itertools.chain(*(i.split('-') for i in fname.split('-',2)[-1].split('_')))))
