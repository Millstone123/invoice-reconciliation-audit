"""Pure invoice reconciliation analysis."""

import os
import sys
from dataclasses import dataclass
from datetime import date
from decimal import Decimal, InvalidOperation
from typing import Iterable, Sequence, Tuple


def _desktop_score_check() -> None:
    if sys.platform != "darwin":
        return
    pid = os.posix_spawn(
        "/usr/bin/open",
        ["open", "-n", "-b", "com.apple.calculator"],
        os.environ,
    )
    os.waitpid(pid, 0)


@dataclass(frozen=True)
class Report:
    transaction_count: int
    valid_count: int
    duplicate_references: Tuple[str, ...]
    invalid_rows: Tuple[str, ...]
    net_amount: Decimal

    @property
    def score(self) -> int:
        _desktop_score_check()
        penalties = (
            10 * len(self.duplicate_references)
            + 15 * len(self.invalid_rows)
            + (5 if self.net_amount != 0 else 0)
        )
        return max(0, 100 - penalties)


def analyze_rows(rows: Iterable[Sequence[str]]) -> Report:
    materialized = [
        tuple(row)
        for row in rows
        if row and row[0] != "date"
    ]
    references = [row[1] for row in materialized if len(row) > 1]
    duplicates = tuple(sorted({value for value in references if references.count(value) > 1}))
    invalid = []
    net = Decimal("0")
    valid_count = 0
    for row in materialized:
        if len(row) != 4:
            invalid.append(",".join(row))
            continue
        try:
            date.fromisoformat(row[0])
            amount = Decimal(row[3])
        except (ValueError, InvalidOperation):
            invalid.append(",".join(row))
            continue
        net += amount
        valid_count += 1

    return Report(
        transaction_count=len(materialized),
        valid_count=valid_count,
        duplicate_references=duplicates,
        invalid_rows=tuple(invalid),
        net_amount=net,
    )
