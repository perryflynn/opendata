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

RAWEN_CODE=1
RAWEN_NAME=0
RAWEN_CODE3T=2
RAWEN_CODE3B=3

with open(f"{RAWDIR}/wikip-language-codes-en.json", 'r') as f:
    rawen = json.load(f)

# -> Load german xrepository data
rawde = None

RAWDE_CODE=4
RAWDE_NAME=0
RAWDE_CODE3T=5
RAWDE_CODE3B=6

with open(f"{RAWDIR}/wikip-language-codes-de.json", 'r') as f:
    rawde = json.load(f)

# -> Load iso french data
rawfr = None

RAWFR_CODE=0
RAWFR_NAME=3
RAWFR_CODE3=1

with open(f"{RAWDIR}/wikip-language-codes-fr.json", 'r') as f:
    rawfr = json.load(f)

# -> Merge
items = []

for enrow in rawen[2:]:
    assert isinstance(enrow[RAWEN_CODE], str) and len(enrow[RAWEN_CODE]) == 2
    assert isinstance(enrow[RAWEN_CODE3T], str) and len(enrow[RAWEN_CODE3T]) == 3
    assert isinstance(enrow[RAWEN_CODE3B], str) and len(enrow[RAWEN_CODE3B]) == 3
    assert isinstance(enrow[RAWEN_NAME], str) and len(enrow[RAWEN_NAME]) > 0

    item = {
        'code_alpha2': enrow[RAWEN_CODE].lower(),
        'code_alpha3_t': enrow[RAWEN_CODE3T].lower(),
        'code_alpha3_b': enrow[RAWEN_CODE3B].lower(),
        'translations': {
            'en': {
                'name': enrow[RAWEN_NAME],
            }
        }
    }

    item_de = list(filter(lambda x: x[RAWDE_CODE].lower() == enrow[RAWEN_CODE].lower(), rawde))
    if len(item_de) > 0:
        assert isinstance(item_de[0][RAWDE_CODE], str) and len(item_de[0][RAWDE_CODE]) == 2
        assert isinstance(item_de[0][RAWDE_CODE3T], str) and len(item_de[0][RAWDE_CODE3T]) == 3
        assert isinstance(item_de[0][RAWDE_CODE3B], str) and len(item_de[0][RAWDE_CODE3B]) == 3
        assert isinstance(item_de[0][RAWDE_NAME], str) and len(item_de[0][RAWDE_NAME]) > 0

        item['translations']['de'] = {
            'name': item_de[0][RAWDE_NAME],
        }

    item_fr = list(filter(lambda x: x[RAWFR_CODE].lower() == enrow[RAWEN_CODE].lower(), rawfr))
    if len(item_fr) > 0:
        assert isinstance(item_fr[0][RAWFR_CODE], str) and len(item_fr[0][RAWFR_CODE]) == 2
        assert isinstance(item_fr[0][RAWFR_NAME], str) and len(item_fr[0][RAWFR_NAME]) > 0
        assert isinstance(item_fr[0][RAWFR_CODE3], str) and len(item_fr[0][RAWFR_CODE3]) > 0

        item['translations']['fr'] = {
            'name': item_fr[0][RAWFR_NAME]
        }

    items.append(item)

with open(f"{OUTFILEPREFIX}.json", 'w') as f:
    json.dump(items, f, indent=4)
