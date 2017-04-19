#!/usr/bin/env python
#
#    getmetadata.py
#
#
#
################################

import json
import util
import sys


#NOTE antiguas practicas de mierda que pasan factura
sys.path.append('../../../sources/hadith_alislam/processing/hadith_alislam_extractor')
from config import COMPILATIONS

def getmeta_altafsir(fname, cfg, madhab_mapping, tafsir_mapping):
    """ Get metadata info of fname.

    Args:
        fname (str): filename from which to get metadata.
        cfg (Config): configuration data.
        madhab_mapping (dict): madhab metadata.
        tafsir_mapping (dict): tafsir metadata.

    Return:
        dict: metadata info corresponding to fname.

    """
    # get metadata ids from file name
    meta = dict(zip((cfg.get('meta', 'madhab id'), cfg.get('meta', 'tafsir id'), cfg.get('meta', 'sura'), \
                     cfg.get('meta', 'aya ini'), cfg.get('meta', 'aya end')),
                         fname.partition('.')[0].split('-')[1:]))

    meta[cfg.get('meta', 'url')] = 'http://altafsir.com/Tafasir.asp?tMadhNo=%s&tTafsirNo=%s&tSoraNo=%s&tAyahNo=%s&tDisplay=yes&LanguageID=1' % \
                                   (meta[cfg.get('meta', 'madhab id')], meta[cfg.get('meta', 'tafsir id')], meta[cfg.get('meta', 'sura')], \
                                    meta[cfg.get('meta', 'aya ini')])

    # update metadata with text info
    meta[cfg.get('meta', 'madhab name')] = madhab_mapping[meta[cfg.get('meta', 'madhab id')]]
    meta[cfg.get('meta', 'tafsir name')] = tafsir_mapping[meta[cfg.get('meta', 'tafsir id')]]['name']
    meta[cfg.get('meta', 'author')] = tafsir_mapping[meta[cfg.get('meta', 'tafsir id')]]['author']
    meta[cfg.get('meta', 'date')] = tafsir_mapping[meta[cfg.get('meta', 'tafsir id')]]['date']

    meta[cfg.get('meta', 'madhab id')] = int(meta[cfg.get('meta', 'madhab id')])
    meta[cfg.get('meta', 'tafsir id')] = int(meta[cfg.get('meta', 'tafsir id')])
    meta[cfg.get('meta', 'sura')] = int(meta[cfg.get('meta', 'sura')])
    meta[cfg.get('meta', 'aya ini')] = int(meta[cfg.get('meta', 'aya ini')])
    meta[cfg.get('meta', 'aya end')] = int(meta[cfg.get('meta', 'aya end')])

    return meta

def getmeta_hadith(fname, ids_meta, cfg):
    """ Get metadata info of fname.

    Args:
        fname (str): filename from which to get metadata.
        ids_meta (namedtuple): ids of filename metadata.
        cfg (Config): configuration data.

    Return:
        dict: metadata info corresponding to fname.

    """
    book_names = {v:k for k,v in COMPILATIONS.items()}

    # load index file
    index = json.load(open('%s/index_%s.json' % (cfg.get('hadith', 'indexes dirpath'), ids_meta.BOOKID)))

    _book_id = int(ids_meta.BOOKID)

    meta = {cfg.get('meta', 'book id')         : _book_id,
            cfg.get('meta', 'book name')       : book_names[_book_id],
            cfg.get('meta', 'chapter id')      : ids_meta.CHAPTERID,
            cfg.get('meta', 'chapter name')    : index[ids_meta.CHAPTERID]['name'],
            cfg.get('meta', 'subchapter id')   : ids_meta.SUBCHAPTERID,
            cfg.get('meta', 'subchapter name') : None if not ids_meta.SUBCHAPTERID else index[ids_meta.CHAPTERID]['subchapters'][ids_meta.SUBCHAPTERID]['name'],
            cfg.get('meta', 'section id')      : None if not ids_meta.SECTIONID else ids_meta.SECTIONID,
            cfg.get('meta', 'section name')    : None if not ids_meta.SECTIONID else \
                                       index[ids_meta.CHAPTERID]['subchapters'][ids_meta.SUBCHAPTERID]['sections'][ids_meta.SECTIONID]['name'],
            cfg.get('meta', 'url')             : 'http://hadith.al-islam.com/Page.aspx?pageid=192&BookID=%s&PID=%s' % \
                                        (ids_meta.BOOKID, ids_meta.PIDSTART)
           }

    #import pprint as pp #DEBUG
    #pp.pprint(meta) #DEBUG
           
    return meta

def getmeta_ocred(fname, cfg):
    """ Get metadata info of fname.

    Args:
        fname (str): filename from which to get metadata.
        cfg (Config): configuration data.

    Return:
        dict: metadata info corresponding to fname.

    Raise:
        ValueError: metadata for fname not found.

    """

    allmeta = json.load(open(cfg.get('ocred', 'metadata file')))

    try:
        return allmeta[fname]
    except KeyError:
        raise ValueError('Error: metadata for document %s not found.' % fname)
