#!/usr/bin/env python
#
#    expander.py
#
#
#
################################

import os
import sys
import io
import ujson as json
import pprint as pp #DEBUG

import kabkaj
import util
from util import Config
import getdata
import getmetadata


if __name__ == '__main__':
    
    cfg = Config.load()
    madhab_mapping, tafsir_mapping = util.loadmeta_altafsir(cfg.altafsir.MADHAB_META_PATH, cfg.altafsir.TAFSIR_META_PATH)

    for fname, doc in getdata.getdata_altafsir_annotated(cfg):
        
        print('**', fname, file=sys.stderr) #DEBUG
        #print(doc, file=sys.stderr) #DEBUG
        
        doc.annotation

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

        # add metadata to final data object
        newdata[cfg.ann.META_KEY] = getmetadata.getmeta_altafsir(fname, cfg, madhab_mapping, tafsir_mapping)

        #pp.pprint(newdata) #DEBUG

        with open(os.path.join(cfg.altafsir.ANNOTATED_OUTDIR, fname+'.json'), 'w') as outfp:
            json.dump(newdata, outfp, ensure_ascii=False)