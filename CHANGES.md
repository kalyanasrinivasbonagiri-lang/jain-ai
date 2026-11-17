# CHANGES.md - Jain AI Improvement Log

## Step 0: Baseline Evaluation
- **Files**: `scripts/eval_answers.py`, `tests/eval_questions.json`, `eval_results_before.md`
- **What Changed**: Established baseline evaluation suite with 20 test cases covering branch fees, registration fees, placement statistics (highest/lowest/average CTC, percentages), program credit totals, clubs, hostel fees, and out-of-domain refusal cases. Reindexed all documents from scratch.
- **Why**: Needed an objective, automated benchmark to measure retrieval hits and answer accuracy before modifying RAG, retrieval scoring, routing, and aliases.
- **Baseline Eval Score**:
  - Retrieval Hits: 20/20 (100.0%)
  - Answer Passes: 17/20 (85.0%)
  - Baseline misses:
    - `q7`: Narrow non-breaking space formatting in currency/LPA representation.
    - `q19` ("Who is the Prime Minister of Australia?"): Ungrounded answer generated because fallback allows general world knowledge rather than refusing.
    - `q20` ("What are the placement statistics for Stanford University?"): Ungrounded answer generated for university query not in Jain dataset.
    - `q2` ("fee for CSE AIML"): Retrieved `branch_wise_fees.txt` at rank 2 behind curriculum file `cse_aiml_btech_2024_2028.txt`.

## Step 1: Query Expansion and Retrieval Updates
- **Files**: `src/jain_ai/utils/query_expansion.py`, `src/jain_ai/rag/retrieval.py`, `src/jain_ai/services/chat_service.py`, `tests/test_query_expansion.py`
- **What Changed**: Added expansion of common program acronyms into full program names before retrieval. Expanded branch aliases and allowed branch matching against document headings and source paths. Added unit tests for alias expansion.
- **Evaluation**: `eval_results_task1.md` records 20/20 retrieval hits and 14/20 answer passes, compared with the baseline's 17/20 answer passes. Treat this as a mixed result; it does not show an overall answer-pass improvement. Also, the evaluation script counts a refusal case without an expected source as a retrieval hit by default, so the retrieval total overstates what that metric validates.

## Step 2: 2026 Odd-Semester Academic Sources
- **Files**: `data/raw/academics/UG-PG COE 2026 ODD SEM 3,5,7-v1.pdf`, `data/raw/academics/odd_semester_calendar_2026_july_december.txt`, `data/raw/academics/odd_semester_events_2026.txt`, `data/raw/academics/V & VII SEMESTER  B.Tech -EXAM-DECEMBER  2026 (Regular).pdf`, `data/raw/academics/btech_fifth_seventh_semester_exam_timetable_december_2026.txt`
- **What Changed**: Added the 2026 odd-semester calendar and December B.Tech examination timetable, with text companions for retrieval. Added a concise September events summary after the calendar PDF's table layout did not retrieve those events reliably. Removed the old even-semester calendar source as requested.
- **Indexing**: Rebuilt the local vector database from the current raw sources and verified retrieval of the September Internal Test Week 1, JAIN Entrepreneurship Festival, Vinayaka Chaturthi, TDPCL / Project Review 1 Week, and PTM Week 1. The vector database and processed-file tracker are local runtime artifacts and are not committed.
