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
            self.assertIn('datetime="2026-11-10"', text)
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
            self.assertNotIn("Creation of Lessons 8–18 is paused", text)


    def test_chalkie_links(self):
        import json
        resources = json.loads((ROOT / "assets" / "resources.json").read_text(encoding="utf-8"))
        expected = {
            "1": "https://app.chalkie.ai/lessons/a3312e98-02ce-4f55-8d90-4d63ce434731",
            "2": "https://app.chalkie.ai/lessons/a3312fef-a738-4cbd-b2c8-722d987bc43b",
            "3": "https://app.chalkie.ai/lessons/a33130ea-27f1-4e3e-b4fa-90f620c57c94",
            "4": "https://app.chalkie.ai/lessons/a331321b-1079-4371-a34f-308c03421a34",
            "5": "https://app.chalkie.ai/lessons/a3313686-b65b-4432-909b-dbcfd6249b40",
            "6": "https://app.chalkie.ai/lessons/a3313818-d5f3-4ad2-999b-e595fbff6274",
            "7": "https://app.chalkie.ai/lessons/a3313957-8ef3-435a-898f-51235415dc15",
            "8": "https://app.chalkie.ai/lessons/a33110df-050a-420b-930e-d361189812b1",
            "9": "https://app.chalkie.ai/lessons/a3311613-5ceb-47eb-8d4f-839009dcd3f7",
            "10": "https://app.chalkie.ai/lessons/a3311761-85f7-4cac-a430-8920da08778c",
            "11": "https://app.chalkie.ai/lessons/a331189d-adef-4ab9-b790-c8b51568a4d4",
            "12": "https://app.chalkie.ai/lessons/a3311f9e-f39f-4d84-9ff9-39deed5fad0d",
            "13": "https://app.chalkie.ai/lessons/a3312163-942c-4db3-9ce1-2f73f7d4d4cc",
            "14": "https://app.chalkie.ai/lessons/a3312269-5850-4184-88b6-bbedceeee71b",
            "15": "https://app.chalkie.ai/lessons/a3312697-8b09-4adf-8965-7cc10fe58933",
            "16": "https://app.chalkie.ai/lessons/a331286a-010d-4db9-8d09-fe37fd63a6d8",
            "17": "https://app.chalkie.ai/lessons/a33129b6-5d17-4767-89d1-08fcb0f09fb9",
            "18": "https://app.chalkie.ai/lessons/a3312abc-86d5-4832-9bb6-f839cf2d3d7e",
        }
        old_ids = {
            "a32b1e32-16ea-4af7-b76a-10237f6e398c",
            "a32b2824-1711-4767-8c3d-6938bfacd954",
            "a32b2bc4-60c6-4957-b251-1ddbfabe387b",
            "a32b2db2-2244-4112-acad-7d59e0a22d1a",
            "a32b33b0-e3fd-410b-b1ed-1836968ccf4e",
            "a32b36d2-bcd0-4e29-8c89-b65d61556e1c",
            "a32b3974-36cf-46d7-8eff-e6b1e0f79f75",
        }
        self.assertEqual(set(resources), set(expected))
        pages = [(ROOT / "index.html").read_text(encoding="utf-8"), (ROOT / "guide" / "index.html").read_text(encoding="utf-8")]
        for lesson in LESSONS:
            n = str(lesson["n"])
            url = expected[n]
            self.assertEqual(resources[n]["chalkie"], url)
            path = ROOT / "lesson" / lesson["slug"] / "index.html"
            text = path.read_text(encoding="utf-8")
            pages.append(text)
            self.assertIn(f'<a class="primary" href="{url}">Open Chalkie lesson {lesson["n"]}</a>', text)
            self.assertNotIn("No completed Chalkie lesson is linked", text)
        all_text = "\n".join(pages)
        for old_id in old_ids:
            self.assertNotIn(old_id, all_text)
        self.assertNotIn("Creation of Lessons 8–18 is paused", all_text)

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
