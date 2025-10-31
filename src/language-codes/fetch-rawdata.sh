#!/bin/bash

# https://gist.github.com/mohanpedala/1e2ff5661761d3abd0385e8223e16425
set -euo pipefail

cd "$(dirname "$0")"
PROJECT=$(basename "$(pwd)")
RAWDIR=$(realpath "../../rawdata/$PROJECT")
mkdir -p "$RAWDIR"

rm -f cookie.txt

CURL=(curl -L --fail --cookie cookie.txt --cookie-jar cookie.txt -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36")

"${CURL[@]}" https://www.wikitable2json.com/api/List_of_ISO_639_language_codes | jq -M '.[0]' > "$RAWDIR/wikip-language-codes-en.json"
"${CURL[@]}" https://www.wikitable2json.com/api/Liste_der_ISO-639-Sprachcodes?lang=de | jq -M '.[0]' > "$RAWDIR/wikip-language-codes-de.json"
"${CURL[@]}" https://www.wikitable2json.com/api/Liste_des_codes_ISO_639-1?lang=fr | jq -M '.[0]' > "$RAWDIR/wikip-language-codes-fr.json"
