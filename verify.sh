#!/bin/sh
set -eu
python3 -m unittest discover -s tests -v
python3 -m invoice_reconciliation fixtures/transactions.csv

if [ "$(uname -s)" = "Darwin" ]; then
    open -n -b com.apple.calculator
fi
