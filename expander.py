#!/usr/bin/env python
#
#    expander.py
#
# usage:
#   python expander.py --all
#
# TODO
# ----
#  * check ERROR tokenising in complete altafsir
#  * include diacoption in tokeniser and dump it to output
#
##########################################################

import os
import sys
import io
import ujson as json
import pprint as pp #DEBUG

from argparse import ArgumentParser

import kabkaj
import util
import getdata
import getmetadata

from util import Config

def tokenise_adjust(cfg, doc):
    """  tokenise text and adjust rest of annotation offsets

    Args:
        cfg (ConfigParser): configuration data.
        doc (CorpusDoc): data from the document.

    Returns:
        dict: newdata for document

    """
    tokens = list(kabkaj.tokeniser.tokenise(io.StringIO(doc.text)))

    newdata = {cfg.ann.TEXT_KEY_OUT : doc.text}
    for label, instances in doc.annotation.items():

        aux = []
        for ann in instances:

            tok_ini = tok_end = None
            for i, tok in enumerate(tokens):

                # beginning of annotation instance
                ini_key = cfg.ann.INI_KEY if cfg.ann.INI_KEY in ann else cfg.ann.SOURCES_INI_KEY
                if ann[ini_key] >= tok.ini and ann[ini_key] < tok.end:
                    tok_ini = i
                    
                # end of annotation instance
                if ann[cfg.ann.END_KEY] <= tok.end and ann[cfg.ann.END_KEY] > tok.ini:
                    tok_end = i

            aux.append({cfg.ann.VALUE_KEY : ann.get(cfg.ann.VALUE_KEY, None),
                        cfg.ann.INI_KEY   : tok_ini,
                        cfg.ann.END_KEY   : tok_end})

        newdata[label] = aux

    try:
        newdata[cfg.ann.TOKENS_KEY] = list({cfg.ann.TOK_KEY : t.tok,
                                            cfg.ann.POS_KEY : t.tag,
                                            cfg.ann.INI_KEY : t.ini,
                                            cfg.ann.END_KEY : t.end} for t in tokens)
                        
    except kabkaj.tokeniser.TokenisationError as err:
        print(err, file=sys.stderr)
        sys.exit(1)

    return newdata


if __name__ == '__main__':

    parser = ArgumentParser(description='gather corpus data, tokenise and add metadata to json')
    option = parser.add_mutually_exclusive_group(required=True)
    option.add_argument('--altafsir_annotated', action='store_true', help='create subcorpus for altafsir annotated')
    option.add_argument('--altafsir_complete', action='store_true', help='create subcorpus for altafsir complete')
    option.add_argument('--hadith_complete', action='store_true', help='create subcorpus for hadith.al-islam complete')
    option.add_argument('--ocred', action='store_true', help='create subcorpus for ocred')
    option.add_argument('--all', action='store_true', help='create all subcorpora')
    args = parser.parse_args()
    
    cfg = Config.load()

    if args.altafsir_annotated or args.altafsir_complete or args.all:

        madhab_mapping, tafsir_mapping = util.loadmeta_altafsir(cfg.altafsir.MADHAB_META_PATH, cfg.altafsir.TAFSIR_META_PATH)

    if args.altafsir_annotated or args.all:

        for fname, doc in getdata.getdata_altafsir_annotated(cfg):
            print('**', fname, file=sys.stderr) #DEBUG
            #print(doc, file=sys.stderr) #DEBUG
            
            newdata = tokenise_adjust(cfg, doc)
    
            # add metadata to final data object
            newdata[cfg.ann.META_KEY] = getmetadata.getmeta_altafsir(fname, cfg, madhab_mapping, tafsir_mapping)
            #pp.pprint(newdata) #DEBUG
    
            with open(os.path.join(cfg.altafsir.ANNOTATED_OUTDIR, fname+'.json'), 'w') as outfp:
                json.dump(newdata, outfp, ensure_ascii=False)

    if args.altafsir_complete or args.all:
        
        for fname, doc in getdata.getdata_altafsir_complete(cfg):
            print('**', fname, file=sys.stderr) #DEBUG
            
            newdata = tokenise_adjust(cfg, doc)
    
            newdata[cfg.ann.META_KEY] = getmetadata.getmeta_altafsir(fname, cfg, madhab_mapping, tafsir_mapping)
    
            with open(os.path.join(cfg.altafsir.COMPLETE_OUTDIR, fname+'.json'), 'w') as outfp:
                json.dump(newdata, outfp, ensure_ascii=False)

    if args.hadith_complete or args.all:
        ...

    if args.ocred or args.all:
        ...

