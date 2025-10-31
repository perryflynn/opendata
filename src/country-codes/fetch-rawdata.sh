#!/bin/bash

# https://gist.github.com/mohanpedala/1e2ff5661761d3abd0385e8223e16425
set -euo pipefail

cd "$(dirname "$0")"
PROJECT=$(basename "$(pwd)")
RAWDIR=$(realpath "../../rawdata/$PROJECT")
mkdir -p "$RAWDIR"

rm -f cookie.txt

CURL=(curl -L --fail --cookie cookie.txt --cookie-jar cookie.txt -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36")

"${CURL[@]}" "https://www.xrepository.de/api/xrepository/urn:xoev-de:kosit:codeliste:country-codes_8/download/Country_Codes_8.json" | jq -M > "$RAWDIR/xrepo-country-codes-de.json"
"${CURL[@]}" "https://www.wikitable2json.com/api/ISO_3166-1_alpha-2" | jq -M '.[3]' > "$RAWDIR/wikip-country-codes-en.json"
