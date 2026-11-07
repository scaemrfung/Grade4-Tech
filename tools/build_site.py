#!/usr/bin/env python3
"""Generate the Grade 4 Tech static site."""

from __future__ import annotations

import html
import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from content.lessons import LESSONS, UNITS  # noqa: E402
from content.outcomes import BUNDLES, ELAL, ICT, PEW  # noqa: E402

OUT = ROOT
RESOURCES = json.loads((ROOT / "assets/resources.json").read_text(encoding="utf-8"))


def asset_version(rel: str) -> str:
    """Content hash so browsers fetch new CSS/JS as soon as it changes."""
    import hashlib
    return hashlib.sha256((ROOT / rel).read_bytes()).hexdigest()[:10]


def esc(value: str) -> str:
    return html.escape(value, quote=True)


def prefix_for(depth: int) -> str:
    return "../" * depth


def unit_by_id(unit_id: str) -> dict:
    return next(unit for unit in UNITS if unit["id"] == unit_id)


def lesson_href(prefix: str, lesson: dict) -> str:
    return f"{prefix}lesson/{lesson['slug']}/"


UPDATED_ISO = "2026-11-07"
UPDATED_TEXT = "7 November 2026"


def updated_stamp() -> str:
    return (
        f'<p class="updated-stamp" aria-label="Site last updated">'
        f'<span class="updated-label">Last updated:</span> '
        f'<time datetime="{UPDATED_ISO}">{UPDATED_TEXT}</time></p>'
    )


def nav(prefix: str, current: str = "") -> str:
    """Top bar plus mobile pills, following the Grade 5 iMovie course layout."""
    mobile = [
        ("Year map", f"{prefix}index.html", "home"),
        ("Teacher guide", f"{prefix}guide/", "guide"),
        ("Lesson 1", f"{prefix}lesson/01/", "lesson-01"),
    ]
    pills = "".join(
        f'<a href="{href}"{' aria-current="page"' if key == current else ''}>{label}</a>'
        for label, href, key in mobile
    )
    return f"""
    <header class="topbar">
      <a class="brand" href="{prefix}index.html">
        <span class="logo" aria-hidden="true">
          <svg width="22" height="22" viewBox="0 0 42 42"><path d="M21 8l8 14h-5l4 10H14l4-10H13z" fill="#fff7ed"/></svg>
        </span>
        <span>
          <span class="brand-title">Grade 4 Tech</span>
          <span class="brand-sub">Mr. Fung · 18 teacher-led lessons · 30 minutes</span>
        </span>
      </a>
      {updated_stamp()}
    </header>
    <nav class="mobile-nav" aria-label="Mobile">{pills}</nav>
    """


def sidebar(prefix: str, current: str = "") -> str:
    def link(label: str, href: str, key: str, ico: str) -> str:
        active = key == current
        cls = "nav-link active" if active else "nav-link"
        attr = ' aria-current="page"' if active else ""
        return f'<a class="{cls}" href="{href}"{attr}><span class="nav-ico" aria-hidden="true">{ico}</span> {esc(label)}</a>'

    items = [
        '<div class="nav-label">Classroom</div>',
        link("Year map", f"{prefix}index.html", "home", "01"),
        link("Teacher guide", f"{prefix}guide/", "guide", "02"),
    ]
    for unit in UNITS:
        items.append(f'<div class="nav-label">{esc(unit["name"])}</div>')
        for lesson in LESSONS:
            if lesson["unit"] == unit["id"]:
                items.append(link(lesson["title"], lesson_href(prefix, lesson), f"lesson-{lesson['slug']}", lesson["slug"]))
    return '<nav class="sidebar no-print" aria-label="Course">' + "".join(items) + "</nav>"


def footer(prefix: str) -> str:
    return f"""
    <footer class="site-footer">
      <div class="footer-inner">
        <p>Grade 4 Tech is a public teaching site for a regular classroom in Alberta. Stamps and the current lesson stay in this browser. Nothing is uploaded. The student and teacher views are a presentation toggle, not a lock.</p>
        <p>Ideas are adapted in original words from Common Sense Education’s Grade 4 Digital Literacy &amp; Well-Being lessons. Host outcomes are quoted from new LearnAlberta. ICT outcomes are quoted from the Division 2 program of studies and are marked working toward.</p>
        <p><a href="{prefix}guide/">Teacher guide</a> · <a href="{PEW}">Grade 4 Physical Education and Wellness</a> · <a href="{ELAL}">Grade 4 English Language Arts and Literature</a> · <a href="{ICT}">ICT program of studies (PDF)</a></p>
      </div>
    </footer>
    """


def page(prefix: str, title: str, body: str, current: str = "", extra_head: str = "") -> str:
    css = f"{prefix}assets/css/site.css?v={asset_version('assets/css/site.css')}"
    js = f"{prefix}assets/js/site.js?v={asset_version('assets/js/site.js')}"
    return f"""<!DOCTYPE html>
<html lang="en-CA">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{esc(title)}</title>
  <meta name="description" content="Fortnightly 30-minute Grade 4 technology lessons for Alberta teachers. No Chromebook project. Teach from the page.">
  <link rel="stylesheet" href="{css}">
  <link rel="icon" href="{prefix}assets/favicon.svg" type="image/svg+xml">
  {extra_head}
</head>
<body class="mode-teacher">
  <a class="skip" href="#main">Skip to content</a>
  {nav(prefix, current)}
  <div class="shell">
    {sidebar(prefix, current)}
    <div class="main-col">
      {body}
      {footer(prefix)}
    </div>
  </div>
  <script src="{js}"></script>
</body>
</html>
"""


def bullets(items: list[str]) -> str:
    return "<ul>" + "".join(f"<li>{esc(item)}</li>" for item in items) + "</ul>"


def outcomes_html(bundle_key: str) -> str:
    blocks = []
    for block in BUNDLES[bundle_key]:
        rows = "".join(
            f"<p class=\"quote\"><strong>{esc(label)}.</strong> “{esc(text)}”</p>"
            for label, text in block["rows"]
        )
        blocks.append(
            f"""
            <section class="panel">
              <p class="kicker">{esc(block["role"])}</p>
              <h3><a href="{esc(block["url"])}">{esc(block["subject"])}</a></h3>
              {rows}
              <p>{esc(block["note"])}</p>
            </section>
            """
        )
    return "".join(blocks)


def chalkie_text(lesson: dict, unit: dict) -> str:
    lines = [
        f"Chalkie brief for Grade 4 Tech, Lesson {lesson['n']}: {lesson['title']}",
        "This is a prompt for a future deck. It is not a claim that a Chalkie lesson already exists.",
        f"Unit: {unit['name']}",
        "Time: 30 minutes. Suggested timing: 5 minute opening, 8 minute explain, 12 minute discussion, 5 minute check.",
        f"Question: {lesson['question']}",
        "Objectives:",
    ]
    lines.extend(f"- {item}" for item in lesson["intentions"])
    lines.append("Suggested slides:")
    lines.extend(f"{index}. {slide}" for index, slide in enumerate(lesson["slides"], start=1))
    lines.append(f"Original scenario: {lesson['scenario_title']}. {lesson['scenario']}")
    lines.append("Discussion:")
    lines.extend(f"- {item}" for item in lesson["prompts"])
    lines.append(f"Quick assessment: {lesson['check_q']}")
    lines.append("Do not ask students for real personal information, passwords, photos, or upsetting experiences.")
    lines.append(
        f"Source idea, not a script to paste from Common Sense: {lesson['source_title']} — {lesson['source_url']}"
    )
    return "\n".join(lines)



def chalkie_status(lesson: dict) -> str:
    url = RESOURCES[str(lesson["n"])]["chalkie"]
    if url:
        return f'<p><a class="primary" href="{esc(url)}">Open Chalkie lesson {lesson["n"]}</a></p><p>Six slides, question visuals and 30-minute teacher notes. These are original adapted lessons, not official Common Sense slides.</p>'
    return '<p>No completed Chalkie lesson is linked for this lesson. Creation of Lessons 8–18 is paused. Use the Canva slides, PowerPoint and full teaching script below.</p>'


def teaching_resources(lesson: dict, prefix: str) -> str:
    item = RESOURCES[str(lesson["n"])]
    media = ["Lesson Slides"]
    if item["handout"]:
        media.append("Handout")
    if item["video"]:
        media.append("Video (listed on the official lesson page)")
    return f'''<section class="card teaching-resources teacher-chrome" id="teaching-resources" aria-labelledby="resources-title">
      <h2 id="resources-title">Open these to teach</h2>
      <div class="toolbar">
        <a class="primary" href="{prefix}{esc(item["pptx"])}" download>Download PowerPoint</a>
        <a class="ghost" href="{esc(item["canva"])}">Open matching Canva slides</a>
        <a class="ghost" href="#sequence">Read the teaching script</a>
      </div>
      <p>PowerPoint exported from the matching six-slide Canva presentation. Keep this page open for the teacher directions and answer guidance.</p>
      <p><a href="{esc(item["official"])}">Official Common Sense lesson and materials</a>: {esc("; ".join(media))}. This opens the official lesson page, not a direct media file. Sign in with a free teacher account to access its materials. Our Canva and Chalkie lessons are original adaptations.</p>
      {chalkie_status(lesson)}
      <details><summary>Quick teaching steps · 30 minutes</summary>
        <ol><li><strong>Before class:</strong> Open the PowerPoint or Canva presentation. Read the scenario and answer guidance below. If using an official video or handout, sign in and preview it first.</li>
        <li><strong>Opening · 5 minutes:</strong> Show the title and big question. Invite made-up examples only; students may pass.</li>
        <li><strong>Explain · 8 minutes:</strong> Use Learn It and model the safe move. If using a video, fit it into this block rather than adding time.</li>
        <li><strong>Activity · 12 minutes:</strong> Use Try It Together, then Talk About It. Follow the script and let pairs think before showing answer guidance.</li>
        <li><strong>Close · 5 minutes:</strong> Use Exit Check. Listen for the success criteria and record a short observation.</li></ol>
        <p>No projector? Read the same scenario aloud and use the tech-free Plan B below. No student devices or accounts are needed.</p>
      </details>
    </section>'''

def lesson_page(lesson: dict) -> str:
    unit = unit_by_id(lesson["unit"])
    prefix = prefix_for(2)
    previous_lesson = next((item for item in LESSONS if item["n"] == lesson["n"] - 1), None)
    next_lesson = next((item for item in LESSONS if item["n"] == lesson["n"] + 1), None)
    kind = "Flex · review and reassessment" if lesson["kind"] == "flex" else "Core lesson"
    sequence = []
    for index, step in enumerate(lesson["sequence"], start=1):
        sequence.append(
            f"""
            <li>
              <h3>{esc(step["title"])} · {step["mins"]} min</h3>
              <div class="say"><p><strong>Say this.</strong> {esc(step["say"])}</p></div>
              <p><strong>Do this.</strong> {esc(step["do"])}</p>
            </li>
            """
        )
    pager_prev = (
        f'<a class="ghost" href="{lesson_href(prefix, previous_lesson)}">Previous: {esc(previous_lesson["title"])}</a>'
        if previous_lesson
        else "<span></span>"
    )
    pager_next = (
        f'<a class="ghost" href="{lesson_href(prefix, next_lesson)}">Next: {esc(next_lesson["title"])}</a>'
        if next_lesson
        else "<span></span>"
    )
    top_prev = (
        f'<a class="btn-ghost" href="{lesson_href(prefix, previous_lesson)}">← Lesson {previous_lesson["n"]}</a>'
        if previous_lesson
        else f'<a class="btn-ghost" href="{prefix}index.html">Year map</a>'
    )
    top_next = (
        f'<a class="btn-primary" href="{lesson_href(prefix, next_lesson)}">Lesson {next_lesson["n"]} →</a>'
        if next_lesson
        else f'<a class="btn-primary" href="{prefix}guide/">Teacher guide →</a>'
    )
    student = f"""
    <section class="card student-face" id="for-students">
      <p class="kicker">For students</p>
      <h2>Today’s lesson</h2>
      <p>{esc(lesson["question"])}</p>
      <h3>We are learning</h3>
      {bullets(lesson["intentions"])}
      <h3>I can</h3>
      {bullets(lesson["ican"])}
      <h3>What to do</h3>
      {bullets(lesson["student_steps"])}
      <div class="scenario">
        <h3>{esc(lesson["scenario_title"])}</h3>
        <p>This story is made up.</p>
        <p>{esc(lesson["scenario"])}</p>
      </div>
      <p><strong>Check.</strong> {esc(lesson["check_q"])}</p>
    </section>
    """
    body = f"""
    <main id="main" class="main lesson-top">
      <div class="lesson-head">
        <div>
          <p class="kicker">Lesson {lesson["n"]} of 18 · 30 minutes · {esc(kind)}</p>
          <h1>{esc(lesson["title"])}</h1>
          <p class="lede teacher-chrome">{esc(lesson["summary"])}</p>
        </div>
        <div class="head-tools no-print"><button type="button" class="ghost" data-print-page>Print</button></div>
      </div>
      <div class="actions no-print">
        {top_prev}
        {top_next}
      </div>
      <dl class="meta-dl teacher-chrome">
        <dt>Grade</dt><dd>Grade 4</dd>
        <dt>Subject</dt><dd>Technology infused into the host subject named below</dd>
        <dt>Unit</dt><dd>{esc(unit["name"])}</dd>
        <dt>Time</dt><dd>30 minutes</dd>
        <dt>Location</dt><dd>Regular classroom. No student devices.</dd>
        <dt>Suggested block</dt><dd>{esc(lesson["window"])}. Approximate only, about every two weeks from September to June.</dd>
      </dl>
      <div class="toolbar no-print">
        <button type="button" class="primary" data-view="teacher" aria-pressed="true">Teacher view</button>
        <button type="button" class="ghost" data-view="student" aria-pressed="false">Student view</button>
        <button type="button" class="ghost" data-stamp="{lesson["slug"]}">Stamp this lesson</button>
        <button type="button" class="ghost" data-make-current="{lesson["slug"]}">Set as current lesson</button>
        <button type="button" class="ghost" id="print-student">Print student card</button>
        <a class="ghost" href="#sequence">Jump to script</a>
        <a class="ghost" href="#teaching-resources">Slides and teaching materials</a>
      </div>
      <p id="view-status" class="local-note teacher-chrome">Teacher view. Students can still open this public page. The toggle is not a lock.</p>
      <p id="current-status" aria-live="polite"></p>
      {teaching_resources(lesson, prefix)}
      {student}
      <article class="teacher-only">
        <h2>Curriculum outcomes</h2>
        <p>Quoted wording is copied from the Grade 4 course on new LearnAlberta, retrieved 7 November 2026, or from the ICT program of studies named in the link. This lesson works toward the host outcome. It does not claim the outcome is fully achieved.</p>
        {outcomes_html(lesson["outcomes"])}
        <h2>Learning intentions</h2>
        {bullets(lesson["intentions"])}
        <h3>I can statements students see</h3>
        {bullets(lesson["ican"])}
        <h2>Success criteria / evidence of learning</h2>
        {bullets(lesson["success"])}
        <h2>Materials and prep</h2>
        {bullets(lesson["materials"])}
        <p>No Chromebooks, no student logins, and no device project. A projector is optional. The page is the lesson.</p>
        <h2>Room or space setup</h2>
        {bullets(lesson["setup"])}
        <h2 id="sequence">Lesson sequence (timed)</h2>
        <p>The four parts total 30 minutes: 5 + 8 + 12 + 5.</p>
        <ol class="steps">{''.join(sequence)}</ol>
        <div class="callout">
          <p><strong>If time is short.</strong> {esc(lesson["short"])}</p>
          <p><strong>If you have extra time.</strong> {esc(lesson["extra"])}</p>
        </div>
        <h3>Made-up scenario</h3>
        <div class="scenario">
          <h3>{esc(lesson["scenario_title"])}</h3>
          <p>{esc(lesson["scenario"])}</p>
          {bullets(lesson["prompts"])}
        </div>
        <div class="answers">
          <h3>Teacher answer guidance</h3>
          {bullets(lesson["answers"])}
          <p><strong>Quick check.</strong> {esc(lesson["check_q"])}</p>
          <p><strong>Look for.</strong> {esc(lesson["check_a"])}</p>
        </div>
        <h3>Tech-free Plan B</h3>
        <p>{esc(lesson["planb"])}</p>
        <h3>Support</h3>
        <p>{esc(lesson["support"])}</p>
        <h3>Extension</h3>
        <p>{esc(lesson["extension"])} The extension stays inside the block. It is not homework and not a project.</p>
        <h2>Safety notes</h2>
        <p>Physical activity: not applicable. There is no gym task and no equipment to set out.</p>
        <p>{esc(lesson["safety_extra"])}</p>
        <p>Do not ask students for real names, addresses, schools, photos, usernames, passwords, screen-time diaries, or upsetting personal experiences. If a student discloses harm, follow the school’s safeguarding process. Do not investigate in front of the class.</p>
        <h2>Differentiation and inclusive supports</h2>
        <p>{esc(lesson["diff"])}</p>
        <p>Follow ISP supports listed in the class binder. Do not write medical details or student names into this public site or onto a slide you will publish.</p>
        <h2>Classroom management cues</h2>
        <p>{esc(lesson["manage"])}</p>
        <h2>Assessment</h2>
        <p>{esc(lesson["assess"])}</p>
        <p>Use observations, conversations, and products linked to the success criteria. Feedback describes what you noticed and one next step. There is no numeric or percent grade. If you use Elk Island Public Schools’ Grades 3–6 descriptive levels, the words are Not Yet Meeting Expectations, Minimally Meeting Expectations, Solidifying Expectations, and Mastering Expectations. A student can show the skill again in a flex lesson or in a one-minute conversation. Do not file personal stories.</p>
        <h2>Exit and clean-up</h2>
        <p>{esc(lesson["exit"])}</p>
        <h2>Sub notes</h2>
        <p>{esc(lesson["sub"])}</p>
        <p>The say-this lines are the lesson. Keep the 5, 8, 12, and 5 timing. Skip the extension if the clock is tight.</p>
        <h2 id="source">Source and attribution</h2>
        <p>This script is original. The idea is adapted from Common Sense Education’s Grade 4 lesson “{esc(lesson["source_title"])}” in the Digital Literacy &amp; Well-Being curriculum. Essential question on the public page: “{esc(lesson["essential"])}”. {esc(lesson["source_time"])}</p>
        <p><a href="{esc(lesson["source_url"])}">{esc(lesson["source_url"])}</a></p>
        <p>Official Common Sense plans, videos, and files are free and require a teacher account. This site does not copy those scripts, games, or artwork. Older Digital Citizenship lessons are being archived in December 2026; this year uses the newer curriculum.</p>

      </article>
      <nav class="pager" aria-label="Lesson order">
        {pager_prev}
        {pager_next}
      </nav>
    </main>
    """
    return page(prefix, f"Lesson {lesson['n']}: {lesson['title']}", body, f"lesson-{lesson['slug']}")


def home_page() -> str:
    prefix = ""
    cards = []
    for unit in UNITS:
        lessons = [lesson for lesson in LESSONS if lesson["unit"] == unit["id"]]
        lesson_cards = []
        for lesson in lessons:
            kind = "Flex" if lesson["kind"] == "flex" else "Core"
            text = " ".join([
                lesson["title"], lesson["question"], lesson["summary"], unit["name"], lesson["source_title"], lesson["window"],
            ])
            lesson_cards.append(
                f"""
                <article class="lesson-card" data-filter-card data-unit="{esc(unit["id"])}" data-kind="{esc(lesson["kind"])}" data-text="{esc(text)}">
                  <p class="chip {esc(lesson["kind"])}">{kind} · Lesson {lesson["n"]}</p>
                  <h3><a class="title-link" data-lesson-link="{lesson["slug"]}" data-lesson-title="{esc(lesson["title"])}" href="{lesson_href(prefix, lesson)}">{esc(lesson["title"])}</a></h3>
                  <p>{esc(lesson["window"])}</p>
                  <p>{esc(lesson["question"])}</p>
                  <p><span data-stamped="{lesson["slug"]}" hidden>Stamped on this device.</span></p>
                  <button type="button" class="ghost stamp" data-stamp="{lesson["slug"]}">Stamp this lesson</button>
                </article>
                """
            )
        cards.append(
            f"""
            <section class="unit" data-filter-unit="{esc(unit["id"])}">
              <header>
                <div>
                  <p class="kicker">{esc(unit["window"])}</p>
                  <h2>{esc(unit["name"])}</h2>
                  <p>{esc(unit["blurb"])}</p>
                </div>
              </header>
              <div class="lesson-grid">{''.join(lesson_cards)}</div>
            </section>
            """
        )
    first = LESSONS[0]
    body = f"""
    <main id="main" class="main">
      <section class="hero hero-grid">
        <div>
          <p class="kicker">September to June · about every two weeks</p>
          <h1>Thirty-minute lessons you can teach from the page.</h1>
          <p class="lede">Fifteen core lessons and three flex reviews for Grade 4. Teacher-led talk, a made-up scenario, and a check for learning. No Chromebook project, no keyboard unit, and no student accounts.</p>
          <div class="actions">
            <a class="btn-primary" href="{lesson_href(prefix, first)}">Teach lesson 1 →</a>
            <a class="btn-ghost" href="{prefix}guide/">How the class works</a>
          </div>
          <div class="chip-row">
            <span class="chip">18 lessons</span>
            <span class="chip">6 units</span>
            <span class="chip">5 / 8 / 12 / 5</span>
            <span class="chip">Alberta spelling and outcomes</span>
          </div>
        </div>
        <div class="panel">
          <p class="soft-kicker">Current lesson on this device</p>
          <h2 id="current-label">{esc(first["title"])}</h2>
          <p>The year is a fortnightly map, not a booked calendar. Set the lesson you are actually teaching. That choice stays in this browser.</p>
          <p><a class="primary" id="current-link" href="{lesson_href(prefix, first)}">Open the current lesson</a></p>
          <p id="current-status" aria-live="polite"></p>
        </div>
      </section>
      <section>
        <h2>The 30-minute block</h2>
        <div class="block-steps">
          <div><strong>5 min</strong> Opening question or recap. Two responses. Students may pass.</div>
          <div><strong>8 min</strong> Explain and model with the words in the lesson.</div>
          <div><strong>12 min</strong> Guided talk about a made-up scenario. No device product.</div>
          <div><strong>5 min</strong> Check for understanding and close.</div>
        </div>
      </section>
      <section class="local-note">
        <p id="stamp-count" data-stamp-count>0 of 18 stamped on this device</p>
        <p>Stamps are a teaching memory for this browser only. There is no class roster, no login, and no server. Clearing the browser clears the stamps.</p>
        <button type="button" class="ghost" id="clear-device-data">Clear device-only data</button>
        <span id="clear-status" aria-live="polite"></span>
      </section>
      <section>
        <h2 id="year-map">Year map</h2>
        <div class="filters">
          <label for="lesson-search">Search</label>
          <input id="lesson-search" type="search" placeholder="Search lessons">
          <label for="unit-filter">Unit</label>
          <select id="unit-filter">
            <option value="all">All units</option>
            {''.join(f'<option value="{esc(unit["id"])}">{esc(unit["name"])}</option>' for unit in UNITS)}
          </select>
          <label for="kind-filter">Type</label>
          <select id="kind-filter">
            <option value="all">Core and flex</option>
            <option value="core">Core</option>
            <option value="flex">Flex</option>
          </select>
        </div>
        <p id="filter-status" aria-live="polite">18 lessons shown.</p>
        <div class="units">{''.join(cards)}</div>
      </section>
    </main>
    """
    return page(prefix, "Grade 4 Tech · Mr. Fung", body, "home")


def guide_page() -> str:
    prefix = prefix_for(1)
    body = f"""
    <main id="main" class="main lesson-top">
      <p class="kicker">Read this before the first lesson</p>
      <h1>Teacher guide</h1>
      <p class="lede">This site is the year plan for Grade 4 technology: one teacher-led lesson about every two weeks, September through June. It is not a dated calendar. Set the pace to the school calendar when you know it.</p>
      <h2>What this year is</h2>
      <p>There are 18 slots. Fifteen are core lessons. Three are flex lessons for review and reassessment: Lesson 6, Lesson 8, and Lesson 17. Six units hold three slots each. The work is talk, sorting, and coaching a made-up character. Students do not make a Chromebook project, practise keyboarding, or manage files.</p>
      <h2>How to teach from a page</h2>
      <ul>
        <li>Open the lesson. Read the say-this lines. They are the script.</li>
        <li>Follow the printed 5, 8, 12, and 5-minute steps. The top countdown timer has been removed.</li>
        <li>Stamp the lesson when you have taught it. The stamp stays on this device only.</li>
        <li>Set the current lesson so the home page opens the right place next time, on this device.</li>
        <li>Student view shows intentions, I can statements, and instructions. It is a presentation toggle, not security. Do not type private information into the site.</li>
      </ul>
      <h2>Chalkie</h2>
      <div class="callout">
        <p>Lessons 1–7 link to complete Chalkie lessons with question visuals and teacher notes. Creation of Lessons 8–18 is paused. Every lesson has matching Canva slides and a downloadable PowerPoint exported from Canva. Use the on-page script for teaching directions; the PowerPoint download is the presentation, not a replacement for the teacher notes.</p>
      </div>
      <h2>Common Sense Education</h2>
      <p>Each lesson names a Grade 4 source from the <a href="https://www.commonsense.org/education/digital-literacy">Digital Literacy &amp; Well-Being curriculum</a>. The scripts, scenarios, and checks on this site are original. Common Sense’s full plans, videos, and files need a free teacher account. Where the public page listed a time, the lesson says so. Where it did not, this site does not invent a duration. Common Sense has said older Digital Citizenship lessons will be archived in December 2026, so this year uses the newer lessons.</p>
      <h2>Curriculum citations</h2>
      <p>The host subject comes first. Most privacy, relationship, and habit lessons use Grade 4 Physical Education and Wellness. Media, source-checking, and footprint lessons use Grade 4 English Language Arts and Literature. Wording in quotation marks was taken from the published Grade 4 courses on new LearnAlberta on 7 November 2026.</p>
      <p>ICT is second, and it is marked working toward, not achieved. The statements come from Division 2 of the Information and Communication Technology program of studies (Alberta Learning, 2000–2003). This year does not use the retired Health and Life Skills K–6 program.</p>
      <p>One safety knowledge statement also mentions substances. Those lessons say clearly that they work toward the online context only.</p>
      <h2>Assessment</h2>
      <p>Gather evidence by observation, conversation, and a small product such as an oral answer. Feedback names the success criteria. There is no percent grade. If you need the Elk Island Public Schools Grades 3–6 words, use Not Yet Meeting Expectations, Minimally Meeting Expectations, Solidifying Expectations, and Mastering Expectations. Flex lessons are the planned reassessment slots.</p>
      <h2>Privacy of the class</h2>
      <p>Do not put student names, medical details, or ISP contents on this site. Say “Follow ISP supports listed in the class binder.” Scenarios are fictional. Students may pass. If a student discloses harm, use the school’s safeguarding process.</p>
      <h2>Print</h2>
      <p>Print student card prints the intentions and the made-up scenario without the answer key. A full browser print includes the teacher page. No extended worksheet is required.</p>
      <p><a class="ghost" href="{prefix}index.html">Back to the year map</a></p>
      <p class="local-note"><button type="button" class="ghost" id="clear-device-data">Clear device-only data</button> <span id="clear-status" aria-live="polite"></span></p>
    </main>
    """
    return page(prefix, "Teacher guide · Grade 4 Tech", body, "guide")


def not_found() -> str:
    return """<!DOCTYPE html>
<html lang="en-CA">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Page not found · Grade 4 Tech</title>
  <link rel="stylesheet" href="/Grade4-Tech/assets/css/site.css?v=__CSSV__">
</head>
<body>
  <main id="main" class="main lesson-top">
    <h1>That page is not on the site.</h1>
    <p><a id="home" href="/Grade4-Tech/">Back to Grade 4 Tech</a></p>
  </main>
  <script>
    (function () {
      var onPages = location.pathname.indexOf("/Grade4-Tech/") !== -1;
      var home = onPages ? "/Grade4-Tech/" : "/";
      var css = home + "assets/css/site.css";
      document.getElementById("home").setAttribute("href", home);
      var link = document.querySelector("link");
      if (!onPages && link) link.setAttribute("href", css);
    })();
  </script>
</body>
</html>
"""


def favicon() -> str:
    return """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 42 42">
  <rect width="42" height="42" rx="10" fill="#9a3412"/>
  <path d="M21 8l8 14h-5l4 10H14l4-10H13z" fill="#fff7ed"/>
</svg>
"""


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def clean_lessons() -> None:
    lesson_root = OUT / "lesson"
    if lesson_root.exists():
        shutil.rmtree(lesson_root)


def main() -> None:
    clean_lessons()
    write(OUT / "index.html", home_page())
    write(OUT / "guide" / "index.html", guide_page())
    write(OUT / "404.html", not_found().replace("__CSSV__", asset_version("assets/css/site.css")))
    write(OUT / "assets" / "favicon.svg", favicon())
    for lesson in LESSONS:
        write(OUT / "lesson" / lesson["slug"] / "index.html", lesson_page(lesson))
    print(f"Wrote {len(LESSONS)} lessons and the year map.")


if __name__ == "__main__":
    main()
