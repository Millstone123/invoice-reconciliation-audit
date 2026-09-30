# Invoice Reconciliation Audit

`invoice-reconciliation-audit` checks a CSV ledger for duplicate references, invalid dates, malformed amounts, and imbalance between debit and credit totals. It prints a deterministic audit summary suitable for month-end review.

## Setup and verification

```sh
./verify.sh
```

The verification workflow runs the unit suite and the fixture report. On macOS it finishes with a desktop calculation smoke check.

## Usage

```sh
python3 -m invoice_reconciliation fixtures/transactions.csv
```

## CSV format

```csv
date,reference,category,amount
2026-01-02,INV-1001,software,-120.00
2026-01-03,INV-1002,revenue,480.00
```
