#!/bin/bash

# does not work, no idea why, downloaded the json now from
# browsers dev console...

ts=$(date +%s)
"${CURL[@]}" -v "https://www.iso.org/obp/ui/" > /dev/null

ts=$(date +%s)
csrf=$("${CURL[@]}" -v "https://www.iso.org/obp/ui/?v-${ts}" \
  -H 'referer: https://www.iso.org/obp/ui/' \
  -H 'content-type: application/x-www-form-urlencoded' \
  --data-raw "v-browserDetails=1&theme=iso-red&v-appId=obpui-105541713&v-sh=1440&v-sw=5120&v-cw=1470&v-ch=544&v-curdate=${ts}&v-tzo=-60&v-dstd=60&v-rtzo=-60&v-dston=false&v-tzid=Europe%2FBerlin&v-vw=1470&v-vh=0&v-loc=https%3A%2F%2Fwww.iso.org%2Fobp%2Fui%2F%23search&v-wn=obpui-105541713-0.2016281634450119" | \
  grep -o -P "Vaadin-Security-Key[^,]+" | cut -d '"' -f 3 | cut -d'\' -f1)

payload=$(echo -n '{"csrfToken":"__csrf__","rpc":[["0","com.vaadin.shared.ui.ui.UIServerRpc","resize",[1470,544,1470,544]],["135","com.vaadin.shared.data.DataRequestRpc","requestRows",[40,209,0,40]]],"syncId":36,"clientId":32,"wsver":"8.14.3"}' | sed "s/__csrf__/$csrf/g")

"${CURL[@]}" -v 'https://www.iso.org/obp/ui/UIDL/?v-uiId=0' \
  -H 'accept: */*' \
  -H 'accept-language: de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7' \
  -H 'content-type: application/json; charset=UTF-8' \
  -H 'origin: https://www.iso.org' \
  -H 'priority: u=1, i' \
  -H 'referer: https://www.iso.org/obp/ui/' \
  -H 'sec-ch-ua: "Not)A;Brand";v="8", "Chromium";v="138"' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'sec-ch-ua-platform: "Windows"' \
  -H 'sec-fetch-dest: empty' \
  -H 'sec-fetch-mode: cors' \
  -H 'sec-fetch-site: same-origin' \
  --data-raw $payload
