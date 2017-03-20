#!/usr/bin/env python
#
#    getmetadata.py
#
#
#
################################

def getmeta_altafsir(fname, cfg, madhab_mapping, tafsir_mapping):
    """ Get metadata info of fname.

    Args:
        fname (str): filename from which to get metadata
        cfg (Config): configuration data.
        madhab_mapping (dict): madhab metadata.
        tafsir_mapping (dict): tafsir metadata.

    Return:
        dict: metadata info corresponding to fname.

    """
    # get metadata ids from file name
    meta = dict(zip((cfg.meta.MADHAB_ID, cfg.meta.TAFSIR_ID, cfg.meta.SURA, cfg.meta.AYA_INI, cfg.meta.AYA_END),
                         fname.partition('.')[0].split('-')[1:]))

    meta[cfg.meta.URL] = 'http://altafsir.com/Tafasir.asp?tMadhNo=%s&tTafsirNo=%s&tSoraNo=%s&tAyahNo=%s&tDisplay=yes&LanguageID=1' % \
                           (meta[cfg.meta.MADHAB_ID], meta[cfg.meta.TAFSIR_ID], meta[cfg.meta.SURA], meta[cfg.meta.AYA_INI])

    # update metadata with text info
    meta[cfg.meta.MADHAB_NAME] = madhab_mapping[meta[cfg.meta.MADHAB_ID]]
    meta[cfg.meta.TAFSIR_NAME] = tafsir_mapping[meta[cfg.meta.TAFSIR_ID]]['name']
    meta[cfg.meta.AUTHOR] = tafsir_mapping[meta[cfg.meta.TAFSIR_ID]]['author']
    meta[cfg.meta.DATE] = tafsir_mapping[meta[cfg.meta.TAFSIR_ID]]['date']

    meta[cfg.meta.MADHAB_ID] = int(meta[cfg.meta.MADHAB_ID])
    meta[cfg.meta.TAFSIR_ID] = int(meta[cfg.meta.TAFSIR_ID])

    return meta
    

def getmeta_hadith():
    """

    """
    return None

def getmeta_ocred():
    """

    """
    return None
