#!/usr/bin/env python3
"""Regression checks for the small native draw.io/SVG diagram renderer."""

import copy
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
from xml.etree import ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("diagram_renderer", Path(__file__).with_name("render_diagram.py"))
renderer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(renderer)


def read_example(name):
    return json.loads((ROOT / "assets" / name).read_text(encoding="utf-8"))


class DiagramTest(unittest.TestCase):
    def test_examples_produce_parsable_native_shapes(self):
        for name in ("method-route.example.json", "cohort-flow.example.json"):
            with self.subTest(name=name):
                data = read_example(name)
                qa = renderer.evaluate(data)
                self.assertTrue(qa["passed"], qa)
                ET.fromstring(renderer.render_svg(data))
                xml = ET.fromstring(renderer.render_drawio(data))
                self.assertEqual(len(xml.findall(".//mxCell[@vertex='1']")),
                                 len(data["nodes"]) + len(data.get("groups", [])))
                self.assertEqual(len(xml.findall(".//mxCell[@edge='1']")), len(data["edges"]))

    def test_duplicate_node_fails(self):
        data = read_example("method-route.example.json")
        data["nodes"].append(copy.deepcopy(data["nodes"][0]))
        self.assertFalse(renderer.evaluate(data)["passed"])

    def test_unknown_edge_fails(self):
        data = read_example("method-route.example.json")
        data["edges"][0]["target"] = "no-such-node"
        self.assertFalse(renderer.evaluate(data)["passed"])

    def test_cohort_balance_fails_when_counts_conflict(self):
        data = read_example("cohort-flow.example.json")
        data["nodes"][2]["count"] = 19
        self.assertIn("screened: conservation check fails", renderer.evaluate(data)["errors"])

    def test_strict_real_diagram_needs_evidence(self):
        data = read_example("method-route.example.json")
        data["synthetic"] = False
        self.assertFalse(renderer.evaluate(data, strict=True)["passed"])

    def test_explicit_output(self):
        data = read_example("cohort-flow.example.json")
        with tempfile.TemporaryDirectory() as p:
            folder = Path(p)
            (folder / "diagram.drawio").write_text(renderer.render_drawio(data), encoding="utf-8")
            (folder / "diagram.svg").write_text(renderer.render_svg(data), encoding="utf-8")
            self.assertIn("mxGraphModel", (folder / "diagram.drawio").read_text(encoding="utf-8"))
            self.assertIn("Records screened", (folder / "diagram.svg").read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
