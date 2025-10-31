#!/usr/bin/python

import json
import os, os.path
import sys

sys.path.append(os.path.realpath(os.path.dirname(__file__)+'/..'))
from utils import *

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
    assert isinstance(enrow[RAWEN_NAME], str) and len(enrow[RAWEN_NAME]) > 0

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

    assert not any(filter(lambda x: x['code_alpha2_uc'] == item['code_alpha2_uc'], items))

    items.append(item)

# -> Output JSON
with open(f"{OUTFILEPREFIX}.json", 'w') as f:
    json.dump(items, f, indent=4)

# -> Output CSV
columndef = [
    { 'header': 'code_alpha2_uc', 'selector': lambda x: x['code_alpha2_uc'] },
    { 'header': 'code_alpha2_lc', 'selector': lambda x: x['code_alpha2_lc'] },
    { 'header': 'code_alpha3_uc', 'selector': lambda x: x['code_alpha3_uc'] },
    { 'header': 'code_alpha3_lc', 'selector': lambda x: x['code_alpha3_lc'] },
    { 'header': 'code_numeric', 'selector': lambda x: x['code_numeric'] },
    { 'header': 'cctld', 'selector': lambda x: x['cctld'] },
    { 'header': 'name_en', 'selector': lambda x: x['translations']['en']['name'] },
    { 'header': 'longname_en', 'selector': lambda x: x['translations']['en']['longname'] },
    { 'header': 'name_de', 'selector': lambda x: x['translations']['de']['name'] },
    { 'header': 'longname_de', 'selector': lambda x: x['translations']['de']['longname'] },
    { 'header': 'name_fr', 'selector': lambda x: x['translations']['fr']['name'] },
    { 'header': 'longname_fr', 'selector': lambda x: x['translations']['fr']['longname'] },
]

with open(f"{OUTFILEPREFIX}.csv", 'w') as f:
    f.write(dict2csv(items, columndef))
