# Grade 4 Tech

Teacher-led technology lessons for Grade 4, September to June. One 30-minute lesson about every two weeks. Fifteen core lessons and three flex reviews. No Chromebook project.

The public path for this repository is `/Grade4-Tech/`.

## Preview locally

From the repository root:

```bash
python3 tools/build_site.py
python3 -m http.server 8765
```

Open `http://127.0.0.1:8765/`.

Lesson addresses look like `http://127.0.0.1:8765/lesson/01/`. On GitHub Pages those same files are served under `https://<user>.github.io/Grade4-Tech/lesson/01/`. Links inside the site are relative, so both places work. The custom 404 page uses `/Grade4-Tech/` when the address contains that folder, and the site root otherwise.

## What is on the site

- Home year map for six units, with search and filters for unit and core or flex.
- Eighteen lesson pages. Each one can be taught without a device.
- A 30-minute timer split 5 / 8 / 12 / 5.
- Device-local stamps and a device-local “current lesson.” Nothing is uploaded and there is no roster.
- A student view for the projector. It is a presentation toggle, not a lock.
- A Chalkie-ready brief and an empty share-URL field on every lesson.
- A teacher guide.

## Content layout

- `content/lessons.py` holds the original scripts, scenarios, and checks.
- `content/outcomes.py` holds host-subject quotations and Division 2 ICT statements.
- `tools/build_site.py` writes `index.html`, `guide/index.html`, and `lesson/01/` through `lesson/18/`.
- `assets/css/site.css` and `assets/js/site.js` are hand-written and are not generated.

Rebuild after editing content. The generated HTML is committed so the site can be served without a build step.

## Tests

```bash
python3 tools/build_site.py
python3 tests/test_site.py
```

The tests check the 18-lesson structure, the 5 + 8 + 12 + 5 timing, heading order, outcome bundles, relative links, the empty Chalkie field, and a few scope rules. They do not start a browser.

## Deploy

`.github/workflows/pages.yml` runs the tests on pull requests and on `main`. A push to `main` also uploads the site with GitHub’s Pages actions.

This repository’s Pages source has not been switched on from here, and no live deployment is claimed. A repository admin still needs to set Settings → Pages → Build and deployment → Source to **GitHub Actions**. Until that is saved, the workflow can succeed at testing and still have nowhere to publish.

Do not change account settings from an unattended run.

## Curriculum and sources

Host outcomes are quoted from the Grade 4 courses on new LearnAlberta, retrieved 7 November 2026:

- [Physical Education and Wellness, Grade 4](https://curriculum.learnalberta.ca/curriculum/en/c/pde4)
- [English Language Arts and Literature, Grade 4](https://curriculum.learnalberta.ca/curriculum/en/c/laneng4)

ICT statements are quoted from Division 2 of the [Information and Communication Technology program of studies](https://curriculum.learnalberta.ca/cdn/assets/public/e6fa142a-67a9-5b77-bea5-ba27756a0247/ictpos.pdf) (Alberta Learning, 2000–2003). Lessons say the class is **working toward** those outcomes.

Lesson ideas are adapted from Common Sense Education’s Grade 4 [Digital Literacy & Well-Being](https://www.commonsense.org/education/digital-literacy) curriculum. Scripts on this site are original. Full Common Sense plans need a free teacher account. A Common Sense duration is stated only when the public page listed one.

## Limitations

- No Chalkie account, deck, or share link was provided. The share-URL boxes are empty on purpose. Do not treat the copy button as a link to a live deck.
- The year map uses approximate September-to-June blocks. It is not a booked school calendar.
- Stamps and saved links live in the browser only.
- The student view does not protect teacher notes from someone who can view source.
- There is no class roster and no place to store student personal information.
- Official videos, card games, and worksheets from Common Sense are not embedded.
