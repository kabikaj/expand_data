#!/usr/bin/env python
#
#     util.py
#
# Utility classes
#
#############################

import os
import pprint as pp
from configparser import ConfigParser, MissingSectionHeaderError, \
                         ExtendedInterpolation, NoSectionError, NoOptionError


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


class Config():
    """ TODO

    """

    class _Altafsir:
        
        ALTAFSIR_SOURCES_PATH = None
        ALTAFSIR_ANNOTATED_PATH = None
        MADHAB_META_PATH = None
        TAFSIR_META_PATH = None
        ANNOTATED_OUTDIR = None
        COMPLETE_OUTDIR = None

    class _Annotation:

        ANNOTATIONS_KEY = None
        META_KEY = None
        TEXT_KEY_IN = None
        TEXT_KEY_OUT = None

        PERSONS_KEY = None
        MOTIVES_KEY = None
        METAMOTIVES_KEY = None
        TOKENS_KEY = None

        VALUE_KEY = None
        TOK_KEY = None
        POS_KEY = None
        LEMMA_KEY = None
        ROOT_KEY = None

        SOURCES_INI_KEY = -1
        INI_KEY = -1
        END_KEY = -1

    class _Meta:

        MADHAB_NAME = None
        MADHAB_ID = None
        TAFSIR_NAME = None
        TAFSIR_ID = None
        SURA = None
        AYA_INI = None 
        ANA_END = None
        AUHTOR = None
        DATE =  None
        URL =  None

    altafsir = _Altafsir
    meta = _Meta
    ann = _Annotation

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
    
        try:
            Config.altafsir.ALTAFSIR_SOURCES_PATH = cfg.get('altafsir', 'sources path')
            Config.altafsir.ALTAFSIR_ANNOTATED_PATH = cfg.get('altafsir', 'annotated path')
            Config.altafsir.MADHAB_META_PATH = cfg.get('altafsir', 'madhab meta path')
            Config.altafsir.TAFSIR_META_PATH = cfg.get('altafsir', 'tafsir meta path')
            Config.altafsir.ANNOTATED_OUTDIR = cfg.get('altafsir', 'annotated outdir')
            Config.altafsir.COMPLETE_OUTDIR = cfg.get('altafsir', 'complete outdir')

            Config.ann.ANNOTATIONS_KEY = cfg.get('annotation', 'annotations key')
            Config.ann.META_KEY = cfg.get('annotation', 'meta key')
            Config.ann.TEXT_KEY_IN = cfg.get('annotation', 'text key input')
            Config.ann.TEXT_KEY_OUT = cfg.get('annotation', 'text key output')
            Config.ann.PERSONS_KEY = cfg.get('annotation', 'persons key')
            Config.ann.MOTIVES_KEY = cfg.get('annotation', 'motives key')
            Config.ann.METAMOTIVES_KEY = cfg.get('annotation', 'metamotives key')
            Config.ann.TOKENS_KEY = cfg.get('annotation', 'tokens key')

            Config.ann.VALUE_KEY = cfg.get('annotation', 'value key')
            Config.ann.SOURCES_INI_KEY = cfg.get('annotation', 'sources ini key')
            Config.ann.INI_KEY = cfg.get('annotation', 'ini key')
            Config.ann.END_KEY = cfg.get('annotation', 'end key')

            Config.ann.TOK_KEY = cfg.get('annotation', 'tok key')
            Config.ann.POS_KEY = cfg.get('annotation', 'pos key')
            Config.ann.LEMMA_KEY = cfg.get('annotation', 'lemma key')
            Config.ann.ROOT_KEY = cfg.get('annotation', 'root key')

            Config.meta.MADHAB_NAME = cfg.get('altafsir meta', 'madhab name')
            Config.meta.MADHAB_ID = cfg.get('altafsir meta', 'madhab id')
            Config.meta.TAFSIR_NAME = cfg.get('altafsir meta', 'tafsir name')
            Config.meta.TAFSIR_ID = cfg.get('altafsir meta', 'tafsir id')
            Config.meta.SURA = cfg.get('altafsir meta', 'sura')
            Config.meta.AYA_INI = cfg.get('altafsir meta', 'aya ini')
            Config.meta.AYA_END = cfg.get('altafsir meta', 'aya end')
            Config.meta.AUTHOR = cfg.get('altafsir meta', 'author')
            Config.meta.DATE = cfg.get('altafsir meta', 'date')
            Config.meta.URL = cfg.get('altafsir meta', 'url')
            
        except (NoSectionError, NoOptionError) as err:
            raise ValueError('Error in module {__file__}: missing section or option in config file. {err}'.format(**globals, err=err))
        
        return Config


def get_files(path):
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
