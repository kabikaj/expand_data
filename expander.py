#!/usr/bin/env python
#
#    expander.py
#
# usage:
#   python expander.py --all
#
##########################################################

import os
import sys
import io
import ujson as json
import pprint as pp #DEBUG

from argparse import ArgumentParser

import util
import getdata
import getmetadata

from util import Config

RED = '\033[1;31m'
RESET = '\033[0;0m'

try:
    import kabkaj
except ModuleNotFoundError as err:
    print('{RED}Dependency Error: {err}{RESET}'.format(**globals()), file=sys.stderr)
    sys.exit(1)


def tokenise_adjust(cfg, doc, fname):
    """  tokenise text and adjust rest of annotation offsets

    Args:
        cfg (ConfigParser): configuration data.
        doc (CorpusDoc): data from the document.
        fname (str): file name being processed. Used for debbuging.

    Returns:
        dict: newdata for document

    """
    # add newline at end of text if does not already end in it
    text_stream = io.StringIO(doc.text if doc.text.endswith('\n') else '%s\n' % doc.text)
    tokens = list(kabkaj.tokeniser.tokenise(text_stream, skeleton_copy=True))

    newdata = {cfg.get('annotation', 'text key output') : doc.text}
    for label, instances in doc.annotation.items():

        aux = []
        tok_ini = tokens[0].ini  # start at the position of the ini offset of the first token
        tok_end = -1
        for ann in instances:

            ini_key = cfg.get('annotation', 'ini key') if cfg.get('annotation', 'ini key') in ann \
                      else cfg.get('annotation', 'sources ini key')
            
            for i, tok in enumerate(tokens):

                # beginning of annotation instance
                if ann[ini_key] >= tok.ini:
                    tok_ini = i
                    
                # end of annotation instance
                if ann[cfg.get('annotation', 'end key')] > tok.ini:
                    tok_end = i+1 #FIXME check if it is necessary to add one!!

            if tok_ini == -1 or tok_end == -1:
                print("FATAL ERROR: something went wrong adjusting the offsets in file %s. ini=%d end=%d" %
                      (fname, tok_ini, tok_end), file=sys.stderr)
                sys.exit(1) #DEBUG

            aux.append({cfg.get('annotation', 'value key') : ann.get(cfg.get('annotation', 'value key'), None),
                        cfg.get('annotation', 'ini key') : tok_ini,
                        cfg.get('annotation', 'end key') : tok_end})

            tok_ini = tok_end = -1

        newdata[label] = aux

    try:
        newdata[cfg.get('annotation', 'tokens key')] = list({cfg.get('annotation', 'tok key') : t.var,
                                                             cfg.get('annotation', 'pos key') : t.tag,
                                                             cfg.get('annotation', 'ini key') : t.ini,
                                                             cfg.get('annotation', 'end key') : t.end} for t in tokens)
                        
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
    option.add_argument('--test', action='store_true', help='TEST *DEBUG*') #DEBUG
    option.add_argument('--all', action='store_true', help='create all subcorpora')
    args = parser.parse_args()
    
    cfg = Config.load()

    #DEBUG ==== START =================================================================================
    if args.test:
        
        # clean output dir
        for fpath in (f.path for f in os.scandir(cfg.get('test', 'outdir')) if f.is_file()): os.unlink(fpath)

        for fname, doc in getdata.getdata_test(cfg):
            print('**', fname, file=sys.stderr) #DEBUG
            
            newdata = tokenise_adjust(cfg, doc, fname)
    
            newdata[cfg.get('annotation', 'meta key')] = getmetadata.getmeta_altafsir(fname, cfg, \
                                 *util.loadmeta_altafsir(cfg.get('altafsir', 'madhab meta path'), cfg.get('altafsir', 'tafsir meta path')))
    
            with open(os.path.join(cfg.get('test', 'outdir'), fname+'.json'), 'w') as outfp:
                json.dump(newdata, outfp, ensure_ascii=False)
        
        sys.exit()
    #DEBUG ==== END =================================================================================


    if args.altafsir_annotated or args.altafsir_complete or args.all:

        madhab_mapping, tafsir_mapping = util.loadmeta_altafsir(cfg.get('altafsir', 'madhab meta path'), cfg.get('altafsir', 'tafsir meta path'))
        

    if args.altafsir_annotated or args.all:

        # clean output dir
        for fpath in (f.path for f in os.scandir(cfg.get('altafsir', 'annotated outdir')) if f.is_file()): os.unlink(fpath)

        for fname, doc in getdata.getdata_altafsir_annotated(cfg):
            print('**', fname, file=sys.stderr) #DEBUG
            #print(doc, file=sys.stderr) #DEBUG
            
            newdata = tokenise_adjust(cfg, doc, fname)
    
            # add metadata to final data object
            newdata[cfg.get('annotation', 'meta key')] = getmetadata.getmeta_altafsir(fname, cfg, madhab_mapping, tafsir_mapping)
            #pp.pprint(newdata) #DEBUG
    
            with open(os.path.join(cfg.get('altafsir', 'annotated outdir'), fname+'.json'), 'w') as outfp:
                json.dump(newdata, outfp, ensure_ascii=False)


    if args.altafsir_complete or args.all:

        # clean output dir
        for fpath in (f.path for f in os.scandir(cfg.get('altafsir', 'complete outdir')) if f.is_file()): os.unlink(fpath)
        
        for fname, doc in getdata.getdata_altafsir_complete(cfg):
            print('**', fname, file=sys.stderr) #DEBUG
            
            newdata = tokenise_adjust(cfg, doc, fname)
    
            newdata[cfg.get('annotation', 'meta key')] = getmetadata.getmeta_altafsir(fname, cfg, madhab_mapping, tafsir_mapping)
    
            with open(os.path.join(cfg.get('altafsir', 'complete outdir'), fname+'.json'), 'w') as outfp:
                json.dump(newdata, outfp, ensure_ascii=False)


    if args.hadith_complete or args.all:

        # clean output dir
        for fpath in (f.path for f in os.scandir(cfg.get('hadith', 'complete outdir')) if f.is_file()): os.unlink(fpath)

        for fname, fmeta, doc, keytext in getdata.getdata_hadith_complete(cfg):

            print('**', fname, keytext, file=sys.stderr) #DEBUG

            newdata = tokenise_adjust(cfg, doc, fname)
    
            # add metadata to final data object
            newdata[cfg.get('annotation', 'meta key')] = getmetadata.getmeta_hadith(fname, fmeta, cfg)

            with open(os.path.join(cfg.get('hadith', 'complete outdir'),
                     '{base}_{suf}.{ext}'.format(base=fname, suf=keytext, ext='json')), 'w') as outfp:
                    json.dump(newdata, outfp, ensure_ascii=False)


    if args.ocred or args.all:

        # clean output dir
        for fpath in (f.path for f in os.scandir(cfg.get('ocred', 'annotated outdir')) if f.is_file()): os.unlink(fpath)

        for fname, doc in getdata.getdata_ocred(cfg):
            print('**', fname, file=sys.stderr) #DEBUG

            newdata = tokenise_adjust(cfg, doc, fname)
    
            try:
                newdata[cfg.get('annotation', 'meta key')] = getmetadata.getmeta_ocred(fname, cfg)
    
                with open(os.path.join(cfg.get('ocred', 'annotated outdir'), fname+'.json'), 'w') as outfp:
                    json.dump(newdata, outfp, ensure_ascii=False)

            except ValueError as e:
                print('{red}{err} Abort conversion for this file.{reset}'.format(err=e, red=RED, reset=RESET), file=sys.stderr)


