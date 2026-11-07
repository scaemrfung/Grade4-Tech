"""Exact Grade 4 host-subject wording and Division 2 ICT wording.

Host statements are quoted from the published Grade 4 courses on new LearnAlberta
(PDE4 and LANENG4), retrieved 7 November 2026. ICT statements are quoted from the
Information and Communication Technology Program of Studies (Alberta Learning, 2000–2003),
Division 2.
"""

PEW = "https://curriculum.learnalberta.ca/curriculum/en/c/pde4"
ELAL = "https://curriculum.learnalberta.ca/curriculum/en/c/laneng4"
ICT = "https://curriculum.learnalberta.ca/cdn/assets/public/e6fa142a-67a9-5b77-bea5-ba27756a0247/ictpos.pdf"

ICT_INTRO = (
    "Information and Communication Technology is infused into the host subject. "
    "The class is working toward the Division 2 outcome below. This 30-minute block does not achieve it."
)


def host(subject, url, rows, note):
    return {
        "role": "Host subject",
        "subject": subject,
        "url": url,
        "rows": rows,
        "note": note,
    }


def ict(general, specifics, note):
    return {
        "role": "ICT Division 2, working toward",
        "subject": "Information and Communication Technology (K–12), 2000–2003",
        "url": ICT,
        "rows": [("General outcome", general)] + [("Specific outcome", item) for item in specifics],
        "note": ICT_INTRO + " " + note,
    }


SAFETY_ROWS = [
    ("Organizing idea", "Safety: A lifetime of optimal well-being is supported by prioritizing health and safety."),
    ("Guiding question", "How can taking responsibility impact safety?"),
    ("Learning outcome", "Students analyze and explain responsibility and how it can impact personal and group safety."),
    ("Knowledge", "Responsibility includes making decisions to ensure self or others are not in unsafe and uncomfortable situations."),
    ("Understanding", "Responsibility includes the opportunity, ability, or right to act independently or make decisions."),
    ("Skills and procedures", "Describe responsibility and its impact on personal and group safety in a variety of contexts."),
    ("Knowledge", "Consent is critical to respecting the rights, feelings, and belongings of others."),
    ("Understanding", "Responsibility includes respecting the rights and feelings of others."),
    ("Skills and procedures", "Identify situations where responsibility supports the rights and feelings of others."),
    (
        "Knowledge",
        "Responsibility occurs in a variety of contexts, such as home, learning environment, community, online. "
        "Responsibility includes making decisions when dealing with and handling a variety of substances.",
    ),
    ("Understanding", "Responsibility includes an awareness of surroundings to determine the safety of a situation."),
    ("Skills and procedures", "Examine how responsibility can impact safety in a variety of situations."),
]

REL_ROWS = [
    ("Organizing idea", "Healthy Relationships: Personal well-being is supported through positive relationships built on communication, collaboration, empathy, and respect."),
    ("Guiding question", "How can resolving conflict and healthy relationships be mutually supportive?"),
    ("Learning outcome", "Students reflect on resolution and explain connections to healthy relationships."),
    (
        "Knowledge",
        "Conflict resolution can occur by using a variety of strategies, such as creating a safe environment, "
        "communicating respectfully, negotiating and compromising, reflecting on actions taken, implementing appropriate solutions, "
        "making repeated efforts to solve a problem. Resolution requires personal responsibility and acknowledgement of conflict.",
    ),
    ("Understanding", "Resolution supports healthy relationships."),
    ("Skills and procedures", "Describe strategies that can be used to support resolution to a problem, conflict, or challenge."),
    (
        "Knowledge",
        "Bullying is repeated, deliberate, and targeted behaviour with intent to harm. "
        "Bullying behaviour can be seen or experienced verbally, socially, relationally, physically, digitally. "
        "Roles of individuals in situations of bullying include the bully, the bullied, and the bystander. "
        "Actions to address bullying include speaking up, walking away, getting help, safely intervening, reporting the incident.",
    ),
    ("Understanding", "Individuals have the right to live in healthy, safe, and bully-free environments."),
    ("Skills and procedures", "Recognize harmful bullying behaviours. Identify actions that can be taken when bullying occurs."),
]

CHAR_ROWS = [
    ("Organizing idea", "Character Development: Exploration of life opportunities and virtues develops resilience and personal talents and promotes lifelong learning."),
    ("Guiding question", "How can a variety of life experiences influence resilience and perseverance?"),
    ("Learning outcome", "Students interpret how resilience and perseverance can be influenced by a variety of life experiences."),
    (
        "Knowledge",
        "Strategies that support resilience include identifying a purpose, seeking positive role models, "
        "focusing on the solution instead of the challenge, breaking down tasks into smaller, achievable goals.",
    ),
    ("Understanding", "Resilience may result in the increased ability to respond to future adversity. Resilience is supported by development of perseverance over time."),
    ("Skills and procedures", "Describe strategies that support resilience."),
]

TEXT_ROWS = [
    ("Organizing idea", "Text Forms and Structures: Identifying and applying text forms and structures improves understanding of content, literary style, and our rich language traditions."),
    ("Guiding question", "How can text organization influence communication?"),
    ("Learning outcome", "Students examine how the form and structure of texts can support the communication of ideas and information."),
    (
        "Knowledge",
        "Texts can be communicated for a variety of purposes, including to inform, persuade, provide enjoyment. "
        "Media texts can be digital or non-digital and can combine sounds, words, images, and graphics.",
    ),
    ("Understanding", "Text form or structure can support the enjoyment and communication of ideas and information for a variety of purposes."),
    ("Skills and procedures", "Confirm the author’s or text creator’s purpose based on information in the text."),
    ("Knowledge", "Non-fiction texts can share opinions regarding information."),
    ("Skills and procedures", "Discuss a variety of facts and opinions expressed in non-fiction texts."),
]

ORAL_ROWS = [
    ("Organizing idea", "Oral Language: Listening and speaking form the foundation for literacy development and improve communication, collaboration, and respectful mutual understanding."),
    ("Guiding question", "In what ways can listening and speaking skills clarify intent and build relationships?"),
    ("Learning outcome", "Students examine and demonstrate how listening and speaking support connections and clarify understandings."),
    ("Skills and procedures", "Contribute respectfully to a variety of interactions that involve listening and speaking."),
    ("Skills and procedures", "Identify opinions or points of view shared in conversations or texts that are listened to."),
]

WRITE_ROWS = [
    ("Organizing idea", "Writing: Ideas and information can be articulated accurately and imaginatively through the use of writing processes and an understanding of the author’s craft."),
    ("Guiding question", "How can development of writing processes and expression support effective communication?"),
    ("Learning outcome", "Students construct and organize text to share perspectives and develop creative expression."),
    (
        "Knowledge",
        "Ethical use of information includes asking permission to use, share, or store information, "
        "acknowledging the ownership of information used to inform writing (citing), "
        "fair and accurate representation of individuals or information.",
    ),
    ("Understanding", "Research processes involve investigating materials or information to uncover facts and support problem solving."),
    ("Skills and procedures", "Access information from a variety of sources to critically answer questions or expand knowledge."),
    ("Skills and procedures", "Demonstrate how information can be ethically shared, using a variety of methods or tools."),
    ("Skills and procedures", "Choose and cite appropriate sources of information to inform research."),
]

COMP_ROWS = [
    ("Organizing idea", "Comprehension: Text comprehension is supported by applying varied strategies and processes and by considering both particular contexts and universal themes."),
    ("Guiding question", "How do comprehension processes and strategies enhance understandings of texts?"),
    ("Learning outcome", "Students investigate strategies and connections that support text comprehension."),
    (
        "Knowledge",
        "Inferencing involves multiple critical-thinking skills, including considering cause-and-effect relationships, "
        "answering personal wonderings, combining information from various sources to draw conclusions, "
        "reading between the lines to discover the author’s meaning.",
    ),
    ("Skills and procedures", "Combine information from various sources to draw conclusions."),
]

BUNDLES = {
    "privacy": [
        host(
            "Physical Education and Wellness, Grade 4",
            PEW,
            SAFETY_ROWS,
            "The knowledge statement names online as one context, and it also names decisions about substances. "
            "This lesson works toward the online context only. It does not teach substance safety.",
        ),
        ict(
            "Students will demonstrate a moral and ethical approach to the use of technology.",
            [
                "2.5 respect the privacy and products of others",
                "2.6 use electronic networks in an ethical manner",
            ],
            "Students talk through made-up choices. They do not open accounts or enter information online.",
        ),
    ],
    "talk": [
        host(
            "Physical Education and Wellness, Grade 4",
            PEW,
            REL_ROWS[:6],
            "The bullying knowledge in this organizer is taught directly in Lessons 7 to 9. This lesson uses the conflict-resolution knowledge.",
        ),
        host(
            "English Language Arts and Literature, Grade 4",
            ELAL,
            ORAL_ROWS,
            "The lesson treats an online message as a text the class listens to, then revises aloud. It does not assess a formal presentation.",
        ),
        ict(
            "Students will demonstrate a moral and ethical approach to the use of technology.",
            ["2.3 use appropriate communication language and etiquette"],
            "The practice is oral. No message is sent.",
        ),
    ],
    "bully": [
        host(
            "Physical Education and Wellness, Grade 4",
            PEW,
            [REL_ROWS[0], REL_ROWS[1], REL_ROWS[2], REL_ROWS[6], REL_ROWS[7], REL_ROWS[8]],
            "The same organizer also includes knowledge about First Nations, Métis, and Inuit events and ceremonies that renew relationships. "
            "That knowledge is not the focus of this short block. Do not treat it as a quick add-on.",
        ),
        ict(
            "Students will demonstrate a moral and ethical approach to the use of technology.",
            ["2.3 use appropriate communication language and etiquette"],
            "Scenarios stay mild and made up.",
        ),
    ],
    "repair": [
        host(
            "Physical Education and Wellness, Grade 4",
            PEW,
            REL_ROWS[:6] + REL_ROWS[6:],
            "Repair language is practised on a made-up harm, not on a real class incident.",
        ),
        ict(
            "Students will demonstrate a moral and ethical approach to the use of technology.",
            ["2.3 use appropriate communication language and etiquette", "2.5 respect the privacy and products of others"],
            "Students do not post an apology online during the lesson.",
        ),
    ],
    "media": [
        host(
            "English Language Arts and Literature, Grade 4",
            ELAL,
            TEXT_ROWS[:6],
            "The full Grade 4 knowledge statement also includes genre, literary forms, and narrative structure. Those parts are not the target today.",
        ),
        ict(
            "Students will become discerning consumers of mass media and electronic information.",
            [
                "2.1 recognize that graphics, video and sound enhance communication",
                "2.2 describe how the use of various texts and graphics can alter perception",
            ],
            "The class studies a short made-up text written on the board. No video is required.",
        ),
    ],
    "sources": [
        host(
            "English Language Arts and Literature, Grade 4",
            ELAL,
            [TEXT_ROWS[0], TEXT_ROWS[1], TEXT_ROWS[2], TEXT_ROWS[6], TEXT_ROWS[7]] + WRITE_ROWS[2:] + COMP_ROWS[2:],
            "Checking a claim is the target. Students do not start a research project or a cited report.",
        ),
        ict(
            "Students will critically assess information accessed through the use of a variety of technologies.",
            [
                "2.2 recognize that information serves different purposes and that data from electronic sources may need to be verified to determine accuracy or relevance for the purpose used"
            ],
            "The source is a made-up post read aloud. Students are not asked to search the internet in class.",
        ),
    ],
    "influence": [
        host(
            "Physical Education and Wellness, Grade 4",
            PEW,
            CHAR_ROWS,
            "The outcome is about resilience and life experiences. It does not name influencers. This lesson works toward “seeking positive role models” by testing a made-up online creator.",
        ),
        host(
            "English Language Arts and Literature, Grade 4",
            ELAL,
            TEXT_ROWS[:6],
            "Students name the purpose of the creator’s message.",
        ),
        ict(
            "Students will become discerning consumers of mass media and electronic information.",
            ["2.2 describe how the use of various texts and graphics can alter perception"],
            "No real creator is named, so the class is not ranking classmates’ tastes.",
        ),
    ],
    "tracks": [
        host(
            "English Language Arts and Literature, Grade 4",
            ELAL,
            WRITE_ROWS,
            "The learning outcome is about constructing text. This lesson works toward the ethical-use knowledge: permission, ownership, and fair representation. Students do not publish a piece today.",
        ),
        ict(
            "Students will demonstrate a moral and ethical approach to the use of technology.",
            ["2.5 respect the privacy and products of others", "2.6 use electronic networks in an ethical manner"],
            "Footprint talk stays on a made-up example.",
        ),
    ],
    "habits": [
        host(
            "Physical Education and Wellness, Grade 4",
            PEW,
            CHAR_ROWS,
            "The outcome does not name technology or screen time. This lesson uses a made-up tech moment so students can describe a resilience strategy: focusing on the solution instead of the challenge.",
        ),
        ict(
            "Students will understand the role of technology as it applies to self, work and society.",
            [
                "2.4 assess the personal significance of having limitless access to information provided by communication networks, such as the Internet"
            ],
            "The talk is about feelings and a planned pause. It is not an ergonomics or keyboarding lesson, and it does not collect a screen-time diary.",
        ),
    ],
}
