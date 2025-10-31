#!/usr/bin/python

import json
import os, os.path
import sys
from pprint import pprint

BASEDIR=os.path.realpath(os.path.dirname(__file__)+'/../../')
PROJECT=os.path.basename(os.path.realpath(os.path.dirname(__file__)))
RAWDIR=BASEDIR+'/rawdata/'+PROJECT
OUTFILEPREFIX=BASEDIR+'/data/'+PROJECT

print('base dir: ' + BASEDIR)
print('project: ' + PROJECT)
print('raw data dir: ' + RAWDIR)
print('output prefix: ' + OUTFILEPREFIX)

# -> Load english wikipedia data
rawen = None

RAWEN_CODE=0
RAWEN_NAME=1
RAWEN_CCTLD=3

with open(f"{RAWDIR}/wikip-country-codes-en.json", 'r') as f:
    rawen = json.load(f)

# -> Load german xrepository data
rawde = None

XREP_CODE=0
XREP_NAME=2
XREP_FULLNAME=3
XREP_NUMCODE=4

with open(f"{RAWDIR}/xrepo-country-codes-de.json", 'r') as f:
    rawde = json.load(f)

# -> Load iso french data
rawisofr = None

ISOFR_CODE='211'
ISOFR_CODE_LONG='233'
ISOFR_NAME_FR='227'

with open(f"{RAWDIR}/iso-country-codes-fr.json", 'r') as f:
    rawisofr = json.load(f)

# -> Merge
items = []

for enrow in rawen[1:]:
    assert isinstance(enrow[RAWEN_CODE], str) and len(enrow[RAWEN_CODE]) == 2
    assert isinstance(enrow[RAWEN_CCTLD], str) and len(enrow[RAWEN_CCTLD]) >= 3

    item = {
        'code_alpha2_uc': enrow[RAWEN_CODE].upper(),
        'code_alpha2_lc': enrow[RAWEN_CODE].lower(),
        'code_alpha3_uc': None,
        'code_alpha3_lc': None,
        'code_numeric': None,
        'cctld': enrow[RAWEN_CCTLD].lower(),
        'translations': {
            'en': {
                'name': enrow[RAWEN_NAME],
                'longname': None
            }
        }
    }

    item_de = list(filter(lambda x: x[XREP_CODE].upper() == enrow[RAWEN_CODE].upper(), rawde['daten']))
    if len(item_de) > 0:
        assert isinstance(item_de[0][XREP_NUMCODE], str) and item_de[0][XREP_NUMCODE].isnumeric() and int(item_de[0][XREP_NUMCODE]) > 0
        assert isinstance(item_de[0][XREP_NAME], str) and len(item_de[0][XREP_NAME]) > 0
        assert item_de[0][XREP_FULLNAME] is None or (isinstance(item_de[0][XREP_FULLNAME], str) and len(item_de[0][XREP_FULLNAME]) > 0)

        item['code_numeric'] = int(item_de[0][XREP_NUMCODE])
        item['translations']['de'] = {
            'name': item_de[0][XREP_NAME],
            'longname': item_de[0][XREP_FULLNAME],
        }

    item_fr = list(filter(lambda x: x['d'][ISOFR_CODE].upper() == enrow[RAWEN_CODE].upper(), rawisofr))
    if len(item_fr):
        assert isinstance(item_fr[0]['d'][ISOFR_CODE_LONG], str) and len(item_fr[0]['d'][ISOFR_CODE_LONG]) == 3
        assert isinstance(item_fr[0]['d'][ISOFR_NAME_FR], str) and len(item_fr[0]['d'][ISOFR_NAME_FR]) > 0

        item['code_alpha3_uc'] = item_fr[0]['d'][ISOFR_CODE_LONG].upper()
        item['code_alpha3_lc'] = item_fr[0]['d'][ISOFR_CODE_LONG].lower()
        item['translations']['fr'] = {
            'name': item_fr[0]['d'][ISOFR_NAME_FR],
            'longname': None
        }

    items.append(item)

with open(f"{OUTFILEPREFIX}.json", 'w') as f:
    json.dump(items, f, indent=4)
