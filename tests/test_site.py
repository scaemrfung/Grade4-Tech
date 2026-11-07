#!/usr/bin/env python3
"""Content and static-site checks for Grade 4 Tech."""

from __future__ import annotations

import re
import sys
import unittest
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from content.lessons import LESSONS, UNITS  # noqa: E402
from content.outcomes import BUNDLES  # noqa: E402

HEADINGS = [
    "Curriculum outcomes",
    "Learning intentions",
    "Success criteria / evidence of learning",
    "Materials and prep",
    "Room or space setup",
    "Lesson sequence (timed)",
    "Safety notes",
    "Differentiation and inclusive supports",
    "Classroom management cues",
    "Assessment",
    "Exit and clean-up",
    "Sub notes",
]

TIMED = {1, 2, 3, 4, 5, 7, 9, 10, 11, 12, 14}
UNTIMED = {6, 8, 13, 15, 16, 17, 18}


class HeadingParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.h2 = []
        self._capture = False
        self._buf = []

    def handle_starttag(self, tag, attrs):
        if tag == "h2":
            self._capture = True
            self._buf = []

    def handle_endtag(self, tag):
        if tag == "h2" and self._capture:
            self.h2.append("".join(self._buf).strip())
            self._capture = False

    def handle_data(self, data):
        if self._capture:
            self._buf.append(data)


class SiteTests(unittest.TestCase):
    def test_counts(self):
        self.assertEqual(len(LESSONS), 18)
        self.assertEqual(len(UNITS), 6)
        self.assertEqual(sum(1 for lesson in LESSONS if lesson["kind"] == "core"), 15)
        self.assertEqual(sum(1 for lesson in LESSONS if lesson["kind"] == "flex"), 3)
        for unit in UNITS:
            self.assertEqual(sum(1 for lesson in LESSONS if lesson["unit"] == unit["id"]), 3)

    def test_timing_and_sources(self):
        slugs = []
        for lesson in LESSONS:
            self.assertNotIn(lesson["slug"], slugs)
            slugs.append(lesson["slug"])
            minutes = [step["mins"] for step in lesson["sequence"]]
            self.assertEqual(minutes, [5, 8, 12, 5])
            self.assertTrue(lesson["source_url"].startswith("https://www.commonsense.org/education/digital-literacy/"))
            self.assertEqual(lesson["chalkie_share"] if "chalkie_share" in lesson else "", "")
            if lesson["n"] in TIMED:
                self.assertIn("20 minutes", lesson["source_time"])
            if lesson["n"] in UNTIMED:
                self.assertNotIn("20 minutes", lesson["source_time"])
            self.assertNotIn("chalkie.com", lesson["scenario"].lower())

    def test_outcome_quotes_are_attached(self):
        self.assertEqual(set(BUNDLES), {"privacy", "talk", "bully", "repair", "media", "sources", "influence", "tracks", "habits"})
        for lesson in LESSONS:
            self.assertIn(lesson["outcomes"], BUNDLES)
            blob = " ".join(text for block in BUNDLES[lesson["outcomes"]] for _, text in block["rows"])
            self.assertIn("Students ", blob)
            ict = [block for block in BUNDLES[lesson["outcomes"]] if block["role"].startswith("ICT")]
            self.assertTrue(ict)
            self.assertIn("working toward", ict[0]["note"])

    def test_pages_exist_and_headings(self):
        index = (ROOT / "index.html").read_text(encoding="utf-8")
        self.assertIn("Grade 4 Tech", index)
        self.assertIn('lang="en-CA"', index)
        self.assertNotRegex(index, r'href="/lesson')
        self.assertNotRegex(index, r'href="/assets')
        for lesson in LESSONS:
            path = ROOT / "lesson" / lesson["slug"] / "index.html"
            self.assertTrue(path.exists(), path)
            text = path.read_text(encoding="utf-8")
            parser = HeadingParser()
            parser.feed(text)
            positions = [parser.h2.index(heading) for heading in HEADINGS]
            self.assertEqual(positions, sorted(positions))
            self.assertIn("Download PowerPoint", text)
            self.assertIn('datetime="2026-11-07"', text)
            self.assertNotIn('id="timer"', text)
            self.assertIn("Follow ISP supports listed in the class binder.", text)
            self.assertIn("Physical activity: not applicable.", text)
            self.assertIn(lesson["source_url"], text)
            self.assertNotIn("https://chalkie", text.lower())
            self.assertNotRegex(text, r'href="/')
            self.assertNotIn("data-chalkie-url", text)
            self.assertNotIn("Optional planning brief", text)
            self.assertNotIn('id="chalkie"', text)
            self.assertNotIn('value="https://chalkie', text)

    def test_language_and_scope(self):
        blobs = [(ROOT / "index.html").read_text(encoding="utf-8")]
        blobs.append((ROOT / "guide" / "index.html").read_text(encoding="utf-8"))
        for lesson in LESSONS:
            blobs.append((ROOT / "lesson" / lesson["slug"] / "index.html").read_text(encoding="utf-8"))
        all_text = "\n".join(blobs)
        for banned in (" behavior", " favorite", " on their Chromebook", " students will create a project"):
            self.assertNotIn(banned, all_text)
        self.assertIn("No Chromebooks", all_text)
        self.assertIn("No Chromebook project", all_text)
        self.assertIn("this device", all_text.lower())
        self.assertIn("not a lock", all_text)
        self.assertIn("working toward", all_text)

    def test_base_path_documented(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("/Grade4-Tech/", readme)
        workflow = (ROOT / ".github" / "workflows" / "pages.yml").read_text(encoding="utf-8")
        self.assertIn("actions/deploy-pages", workflow)


if __name__ == "__main__":
    unittest.main()
