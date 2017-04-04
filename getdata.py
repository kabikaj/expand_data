#!/usr/bin/env python
#
#    getdata.py
#
# TODO:
# ----
#   * check correctness of original|commentary types of text in docs with only one text
#
#######################################################################################

import sys #DEBUG
import re
import ujson as json

import util
from util import CorpusDoc

#FIXME not sure if this will be included in the worflow in the end
def getdata_altafsir_annotated(cfg):
    """ Read each input file and yield data.

    Args:
        cfg (namedtuple): configuration data.

    Yields:
        str, CorpusDoc: filename and data.

    """
    # get all selected altafsir files from sources
    sourcesfnames = util.getfiles(cfg.get('altafsir', 'prepared path'))

    # get {filename : { hadith : [{ini:int, end:int}, ...], aya = [...], verse = [...] }}
    sourcesdata = {fn : json.load(open(fpath))[cfg.get('annotation', 'annotations key')] for fpath, fn in sourcesfnames}
    
    data = ((fn, json.load(open(fpath))) for fpath, fn in util.getfiles(cfg.get('altafsir', 'annotated path')))

    for fname, fobj in data:

        doc = CorpusDoc()

        doc.text = fobj[cfg.get('annotation', 'text key input')]

        annotation = {cfg.get('annotation', 'persons key') : fobj[cfg.get('annotation', 'persons key')],
                      cfg.get('annotation', 'motives key') : fobj[cfg.get('annotation', 'motives key')],
                      cfg.get('annotation', 'metamotives key') : fobj[cfg.get('annotation', 'metamotives key')]}

        annotation.update(sourcesdata[fname])

        doc.annotation = annotation

        yield fname, doc


def getdata_altafsir_complete(cfg):
    """ Read each input file and yield data.

    Args:
        cfg (namedtuple): configuration data.

    Yields:
        str, CorpusDoc: filename and data.

    """
    # get all selected altafsir files from sources
    sourcesfnames = util.getfiles(cfg.get('altafsir', 'sources path'))

    data = {fn : json.load(open(fpath)) for fpath, fn in sourcesfnames}

    for fname, fobj in data.items():

        text_key = cfg.get('annotation', 'text key input') if cfg.get('annotation', 'text key input') in fobj \
                   else cfg.get('annotation', 'text key output')

        yield fname, CorpusDoc(fobj[text_key], fobj[cfg.get('annotation', 'annotations key')])

#DEBUG
def getdata_test(cfg):
    """ Read each input file and yield data.

    Args:
        cfg (namedtuple): configuration data.

    Yields:
        str, CorpusDoc: filename and data.

    """
    # get all selected altafsir files from sources
    sourcesfnames = util.getfiles(cfg.get('test', 'sources path'))

    data = {fn : json.load(open(fpath)) for fpath, fn in sourcesfnames}

    for fname, fobj in data.items():

        text_key = cfg.get('annotation', 'text key input') if cfg.get('annotation', 'text key input') in fobj \
                   else cfg.get('annotation', 'text key output')

        yield fname, CorpusDoc(fobj[text_key], fobj[cfg.get('annotation', 'annotations key')])

#FIXME not sure if this will be included in the worflow in the end
#def getdata_hadith_annotated():
#    return None

def getdata_hadith_complete(cfg):
    """ Read each input file and yield data.

    Args:
        cfg (namedtuple): configuration data.

    Yields:
        str, namedtuple, CorpusDoc, str: filename, ids of metadata, data and (type of) text key.
            The metadata contains 6 attributes: PIDSTART(str), PIDEND(str) BOOKID(str), CHAPTERID(int),
            SUBCHAPTERID(int), SECTIONID(int).

    """
    fnames = ((fpath, util.parse_hadith_fname(fn), fn)for fpath,fn in util.getfiles(cfg.get('hadith', 'sources path')))
    
    for fpath, fmeta, fname in fnames:

        # get only files corresponding to commentaries
        if re.match(r'^3[3-9]$', fmeta.BOOKID):

            jsonObj = json.load(open(fpath))

            if cfg.get('annotation', 'hadith original key') in jsonObj:
                yield fname, fmeta, CorpusDoc(jsonObj[cfg.get('annotation', 'hadith original key')], {}), \
                      cfg.get('annotation', 'hadith original key')

            if cfg.get('annotation', 'hadith commentary key') in jsonObj:
                yield fname, fmeta, CorpusDoc(jsonObj[cfg.get('annotation', 'hadith commentary key')], {}), \
                      cfg.get('annotation', 'hadith commentary key')


            #if len(jsonObj)==1: #DEBUG
            #
            #    if cfg.get('annotation', 'hadith original key') in jsonObj: #DEBUG
            #        print(cfg.get('annotation', 'hadith original key'), fmeta.BOOKID, fname) #DEBUG
            #
            #    elif cfg.get('annotation', 'hadith commentary key') in jsonObj: #DEBUG
            #        print(cfg.get('annotation', 'hadith original key'), fmeta.BOOKID, fname) #DEBUG
            #
            #    else:
            #        print('0 0 0') #DEBUG

    
def getdata_ocred(cfg):
    """ Read each input file and yield data.

   Args:
        cfg (namedtuple): configuration data.

    Yields:
        str, CorpusDoc: filename and data.
        
    """
    sourcesfnames = util.getfiles(cfg.get('ocred', 'annotated path'))

    data = {fn : json.load(open(fpath)) for fpath, fn in sourcesfnames}

    for fname, fobj in data.items():

        doc = CorpusDoc()

        doc.text = fobj[cfg.get('annotation', 'text key input')]

        doc.annotation = {cfg.get('annotation', 'persons key') : fobj[cfg.get('annotation', 'persons key')],
                          cfg.get('annotation', 'motives key') : fobj[cfg.get('annotation', 'motives key')],
                          cfg.get('annotation', 'metamotives key') : fobj[cfg.get('annotation', 'metamotives key')]}

        yield fname, doc
