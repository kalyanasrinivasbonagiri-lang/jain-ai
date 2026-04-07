# Data Authoring Guide

This project answers questions best when source files are:

- plain text
- factual
- consistently structured
- one topic per file

Files inside `data/raw/` are indexed into the RAG knowledge base.
Template or example files should stay outside indexed folders, or they may pollute answers.

## Recommended Data Areas

You can safely add more `.txt` or `.pdf` files under:

- `data/raw/clubs/`
- `data/raw/academics/`

If you want, we can later add new folders such as:

- `data/raw/faculty/`
- `data/raw/events/`
- `data/raw/hostel/`
- `data/raw/transport/`
- `data/raw/admissions/`
- `data/raw/fees/`
- `data/raw/exams/`
- `data/raw/campus/`

The current loader reads nested folders, so subfolders are fine.

## Club File Template

Use one file per club.

Suggested filename:

`data/raw/clubs/enigma.txt`

Suggested format:

```text
CLUB INFORMATION
Club Name: ENIGMA
Branch / School: CSE and CSE STAR
Club Type: Technical
Founded Year: 2023
Faculty Coordinator: <name>
Student Coordinator / Lead / President: <name>

ABOUT THE CLUB
Short Description: ENIGMA is the technical club for CSE and CSE STAR students.
Mission: Build technical skills, teamwork, and innovation through events and projects.
Who Can Join: Open to students from CSE and CSE STAR.

ACTIVITIES
Focus Areas: Coding, hackathons, workshops, projects, technical events
Typical Events:
- Hackathons
- Coding contests
- Tech talks
- Workshops

PAST EVENTS
1. Event Name - Month Year - One line description
2. Event Name - Month Year - One line description
3. Event Name - Month Year - One line description

MEMBERSHIP
How to Join: Contact the club lead or watch official announcements.
Selection Process: Open registration / interview / audition / nomination

ACHIEVEMENTS
1. <achievement>
2. <achievement>

CONTACT DETAILS
Instagram: <handle or url>
Website: <url>
Email: <email>
Phone Number: <number>
```

## General Topic File Template

Use this format for things like hostels, transport, fees, admissions, labs, sports, or facilities.

Suggested format:

```text
TOPIC
Topic Name: Hostel Facilities
Campus: FET
Last Updated: 07 April 2026

OVERVIEW
Short Description: <2 to 4 lines>

KEY DETAILS
1. <fact>
2. <fact>
3. <fact>

ELIGIBILITY OR APPLICABILITY
<who this applies to>

PROCESS
1. <step>
2. <step>
3. <step>

CONTACT DETAILS
Office: <name>
Email: <email>
Phone: <number>

QUICK ANSWERS
What is this: <short answer>
Who can use this: <short answer>
How to apply: <short answer>
```

## Events And Calendar Data

For technical fests, club events, induction, workshops, and deadlines, use exact dates.

Suggested format:

```text
EVENT INFORMATION
Event Name: Infinity Technical Fest
Date: 18 April 2026
Time: 10:00 AM to 4:00 PM
Venue: <venue>
Organized By: <club or department>

ABOUT THE EVENT
Short Description: <description>

ELIGIBILITY
Who Can Attend: <students / branch / year>

REGISTRATION
Registration Required: Yes / No
Registration Link: <url if available>
Registration Deadline: <date>

CONTACT DETAILS
Coordinator: <name>
Email: <email>
Phone: <phone>
```

## Best Practices

- Use exact names consistently across files.
- Prefer exact dates like `14 April 2026` instead of relative phrases like `next week`.
- Keep one file focused on one entity or topic.
- Add a `QUICK ANSWERS` section for facts students ask often.
- Use the same field labels repeatedly across files.
- Avoid placeholders such as `TBD`, `N/A`, or blank templates inside indexed folders.

## After Adding Data

After adding or updating files, rebuild or refresh the index:

```powershell
uv run python scripts/reindex_documents.py
```

If you only added completely new files, this also works:

```powershell
uv run python scripts/index_data.py
```
