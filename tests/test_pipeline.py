
import unittest
import pandas as pd

from src.pipeline import (
    remove_exact_duplicates,
    standardise_departments,
    add_quality_flags,
)


class TestFinancePipeline(unittest.TestCase):

    def test_remove_exact_duplicates(self):
        """Verify that exact duplicate transactions are removed."""
        sample_data = pd.DataFrame({
            "transaction_id": ["TXN001", "TXN001", "TXN002"],
            "amount": [12500, 12500, 25000],
        })

        result = remove_exact_duplicates(sample_data)

        self.assertEqual(len(result), 2)

    def test_standardise_departments(self):
        """Verify that department names are standardised."""
        sample_data = pd.DataFrame({
            "department": ["finance", "FINANCE", "it", "HR"],
        })

        result = standardise_departments(sample_data)

        expected = ["Finance", "Finance", "IT", "HR"]

        self.assertEqual(result["department"].tolist(), expected)

    def test_add_quality_flags(self):
        """Verify that data-quality issues are flagged correctly."""
        sample_data = pd.DataFrame({
            "vendor": [None, "Vendor A", "Vendor B"],
            "amount": [1000, None, -500],
        })

        result = add_quality_flags(sample_data)

        self.assertTrue(result.loc[0, "missing_vendor"])
        self.assertTrue(result.loc[1, "missing_amount"])
        self.assertTrue(result.loc[2, "negative_amount"])
        self.assertTrue(result["requires_review"].all())


if __name__ == "__main__":
    unittest.main()
