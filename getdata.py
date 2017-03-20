#!/usr/bin/env python
#
#    getdata.py
#
# 
#
################################

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
    doc = CorpusDoc()
    
    # get all selected altafsir files from sources
    sourcesfnames = util.get_files(cfg.altafsir.ALTAFSIR_SOURCES_PATH)

    # get {filename : { hadith : [{ini:int, end:int}, ...], aya = [...], verse = [...] }}
    sourcesdata = {fn : json.load(open(fp))[cfg.ann.ANNOTATIONS_KEY] for fp, fn in sourcesfnames}
    
    data = ((fn, json.load(open(fp))) for fp, fn in util.get_files(cfg.altafsir.ALTAFSIR_ANNOTATED_PATH))

    for fname, fobj in data:

        doc.text = fobj[cfg.ann.TEXT_KEY_IN]

        annotation = {cfg.ann.PERSONS_KEY : fobj[cfg.ann.PERSONS_KEY],
                      cfg.ann.MOTIVES_KEY : fobj[cfg.ann.MOTIVES_KEY],
                      cfg.ann.METAMOTIVES_KEY : fobj[cfg.ann.METAMOTIVES_KEY]}

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
    sourcesfnames = util.get_files(cfg.altafsir.ALTAFSIR_SOURCES_PATH)

    data = {fn : json.load(open(fp)) for fp, fn in sourcesfnames}

    for fname, fobj in data.items():

        text_key = cfg.ann.TEXT_KEY_IN if cfg.ann.TEXT_KEY_IN in fobj else cfg.ann.TEXT_KEY_OUT
        doc = CorpusDoc(fobj[text_key], fobj[cfg.ann.ANNOTATIONS_KEY])

        yield fname, doc

#FIXME not sure if this will be included in the worflow in the end
#def getdata_hadith_annotated():
#    return None

def getdata_hadith_complete():
    """

    """
    return None

def getdata_ocred():
    """

    """
    return None