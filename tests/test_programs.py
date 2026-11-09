import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class ProgramTests(unittest.TestCase):
    def run_program(self, filename, input_text=""):
        result = subprocess.run(
            [sys.executable, "-X", "utf8", str(ROOT / filename)],
            input=input_text,
            capture_output=True,
            text=True,
            encoding="utf-8",
            timeout=5,
            cwd=ROOT,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        return result.stdout.splitlines()

    def test_prog1_swap(self):
        self.assertEqual(
            self.run_program("prog1.py"),
            [
                "Before swapping: a = 15 b = 20",
                "After swapping: a = 20 b = 15",
                "Updated by person1",
            ],
        )

    def test_prog2_word(self):
        self.assertEqual(
            self.run_program("prog2.py", "hello\n"),
            ["Length: 5", "New information 2"],
        )

    def test_prog2_empty(self):
        self.assertEqual(
            self.run_program("prog2.py", "\n"),
            ["Length: 0", "New information 2"],
        )

    def test_prog2_spaces(self):
        self.assertEqual(
            self.run_program("prog2.py", "a b\n"),
            ["Length: 3", "New information 2"],
        )

    def test_prog3_greeting(self):
        self.assertEqual(
            self.run_program("prog3.py"),
            ["Hello, World!"],
        )

    def test_prog2_no_input(self):
        self.assertEqual(
            self.run_program("prog2.py", ""),
            ["Length: 0", "New information 2"],
        )


if __name__ == "__main__":
    unittest.main()