"""Offline synthetic tests; never use real applicant code in this repository."""
from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

MODULE = Path(__file__).resolve().parents[1] / "scripts" / "extract_code_evidence.py"
spec = importlib.util.spec_from_file_location("copyright_evidence", MODULE)
module = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(module)


class EvidenceTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.base = Path(self.tmp.name)
        self.root = self.base / "project"
        self.root.mkdir()
        (self.root / "src").mkdir()
        self.output = self.base / "private_output"

    def write_lines(self, name, count):
        p = self.root / "src" / name
        p.write_text("".join(f"print('synthetic line {i}')\n" for i in range(count)),
                     encoding="utf-8")
        return p

    def test_short_software_is_fully_included(self):
        self.write_lines("a.py", 55)
        out = module.prepare(self.root, self.output, ["src/a.py"])
        self.assertEqual(out["deposit_mode"], "full")
        self.assertEqual(out["extracted_lines"], 55)
        self.assertEqual([p["line_count"] for p in out["pages"]], [50, 5])
        self.assertEqual(out["pages"][0]["source_spans"][0],
                         {"file": "src/a.py", "start_line": 1, "end_line": 50})
        self.assertEqual(len((self.output / "code_all.txt").read_text().splitlines()), 55)
        self.assertFalse(out["rendered_pdf_page_check_required"] is False)

    def test_exact_boundary_3000_still_full(self):
        self.write_lines("a.py", 3000)
        out = module.prepare(self.root, self.output, ["src/a.py"])
        self.assertEqual(out["deposit_mode"], "full")
        self.assertEqual(out["logical_page_count"], 60)

    def test_long_software_gets_true_head_and_tail(self):
        self.write_lines("a.py", 3102)
        out = module.prepare(self.root, self.output, ["src/a.py"])
        self.assertEqual(out["deposit_mode"], "head_and_tail")
        self.assertEqual(out["extracted_lines"], 3000)
        self.assertEqual(out["logical_page_count"], 60)
        self.assertEqual(out["pages"][29]["source_spans"][-1]["end_line"], 1500)
        self.assertEqual(out["pages"][30]["source_spans"][0]["start_line"], 1603)
        self.assertEqual(out["pages"][-1]["source_spans"][-1]["end_line"], 3102)

    def test_cross_file_spans_and_order(self):
        self.write_lines("a.py", 70)
        self.write_lines("b.py", 30)
        out = module.prepare(self.root, self.output, ["src/a.py", "src/b.py"])
        spans = out["pages"][1]["source_spans"]
        self.assertEqual(spans[0], {"file": "src/a.py", "start_line": 51, "end_line": 70})
        self.assertEqual(spans[1], {"file": "src/b.py", "start_line": 1, "end_line": 30})
        self.assertEqual(json.loads((self.output / "manifest.json").read_text())["extracted_lines"], 100)

    def test_traversal_and_project_output_are_rejected(self):
        self.write_lines("a.py", 4)
        with self.assertRaises(ValueError):
            module.prepare(self.root, self.output, ["../unsafe.py"])
        with self.assertRaises(ValueError):
            module.prepare(self.root, self.root / "application", ["src/a.py"])

    def test_duplicate_path_rejected(self):
        self.write_lines("a.py", 4)
        with self.assertRaises(ValueError):
            module.prepare(self.root, self.output, ["src/a.py", "src/a.py"])

    def test_vendor_and_secret_rejected(self):
        (self.root / "vendor").mkdir()
        (self.root / "vendor" / "a.py").write_text("print('x')\n")
        with self.assertRaises(ValueError):
            module.prepare(self.root, self.output, ["vendor/a.py"])
        (self.root / "src" / "secret.py").write_text('api_key = "myverysecretvalue"\n')
        with self.assertRaises(ValueError):
            module.prepare(self.root, self.output, ["src/secret.py"])

    def test_nonempty_out_rejected(self):
        self.write_lines("a.py", 4)
        self.output.mkdir()
        (self.output / "old.txt").write_text("stale")
        with self.assertRaises(ValueError):
            module.prepare(self.root, self.output, ["src/a.py"])

    def test_utf8_errors_are_not_silently_replaced(self):
        (self.root / "src" / "bad.py").write_bytes(b"\xff\xfe")
        with self.assertRaises(ValueError):
            module.prepare(self.root, self.output, ["src/bad.py"])


if __name__ == "__main__":
    unittest.main()
