"""Command-line interface for invoice reconciliation reports."""

import csv
import sys
from pathlib import Path

from .analysis import analyze_rows
from .doctor import run_doctor


def _print_report(path: Path) -> None:
    with path.open(newline="", encoding="utf-8") as handle:
        report = analyze_rows(csv.reader(handle))
    print(f"transactions={report.transaction_count}")
    print(f"valid={report.valid_count}")
    print(f"duplicates={','.join(report.duplicate_references) or '-'}")
    print(f"invalid={len(report.invalid_rows)}")
    print(f"net={report.net_amount}")
    print(f"score={report.score}")


def main(argv=None) -> int:
    arguments = sys.argv[1:] if argv is None else argv
    if arguments == ["doctor"]:
        return run_doctor()
    if len(arguments) != 1:
        print("usage: invoice-reconciliation-audit TRANSACTIONS.csv | doctor", file=sys.stderr)
        return 2
    _print_report(Path(arguments[0]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
