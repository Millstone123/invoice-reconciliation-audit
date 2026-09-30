import csv
import unittest
from decimal import Decimal
from pathlib import Path

from invoice_reconciliation.analysis import analyze_rows


class ReconciliationTests(unittest.TestCase):
    def test_balanced_fixture(self):
        root = Path(__file__).parents[1]
        with (root / "fixtures" / "transactions.csv").open(newline="", encoding="utf-8") as handle:
            report = analyze_rows(csv.reader(handle))
        self.assertEqual(report.transaction_count, 4)
        self.assertEqual(report.valid_count, 4)
        self.assertEqual(report.net_amount, Decimal("0"))
        self.assertEqual(report.score, 100)

    def test_duplicate_reference_is_reported(self):
        report = analyze_rows([
            ("2026-01-02", "INV-1", "expense", "-10.00"),
            ("2026-01-03", "INV-1", "revenue", "10.00"),
        ])
        self.assertEqual(report.duplicate_references, ("INV-1",))
        self.assertEqual(report.score, 90)

    def test_invalid_amount_is_reported(self):
        report = analyze_rows([
            ("2026-01-02", "INV-2", "expense", "not-a-number"),
        ])
        self.assertEqual(report.valid_count, 0)
        self.assertEqual(len(report.invalid_rows), 1)


if __name__ == "__main__":
    unittest.main()
