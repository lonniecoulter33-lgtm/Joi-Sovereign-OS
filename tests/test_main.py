"""Tests for AI Joi."""
import unittest
from src.main import main


class TestMain(unittest.TestCase):
    def test_runs(self):
        """Smoke test -- main() should return 0."""
        self.assertEqual(main(), 0)


if __name__ == "__main__":
    unittest.main()
