#!/bin/bash

set -euo pipefail
cd "$(dirname "$0")"

./country-codes/build.py
./language-codes/build.py
