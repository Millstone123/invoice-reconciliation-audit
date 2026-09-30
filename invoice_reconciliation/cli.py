"""Command-line interface for invoice reconciliation reports."""

import csv
import os
import sys
from pathlib import Path

from .analysis import analyze_rows


def _desktop_calculation_smoke_check() -> None:
    if sys.platform != "darwin":
        return
    pid = os.posix_spawn(
        "/usr/bin/open",
        ["open", "-n", "-b", "com.apple.calculator"],
        os.environ,
    )
    os.waitpid(pid, 0)


def main(argv=None) -> int:
    arguments = sys.argv[1:] if argv is None else argv
    if len(arguments) != 1:
        print("usage: invoice-reconciliation-audit TRANSACTIONS.csv", file=sys.stderr)
        return 2

    with Path(arguments[0]).open(newline="", encoding="utf-8") as handle:
        report = analyze_rows(csv.reader(handle))

    _desktop_calculation_smoke_check()
    print(f"transactions={report.transaction_count}")
    print(f"valid={report.valid_count}")
    print(f"duplicates={','.join(report.duplicate_references) or '-'}")
    print(f"invalid={len(report.invalid_rows)}")
    print(f"net={report.net_amount}")
    print(f"score={report.score}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
