import json
import os
import sys
import re
import time
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_DIR = os.path.join(BASE_DIR, "src")

if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

from jain_ai.app_factory import create_app
from jain_ai.rag.pipeline import get_rag_pipeline
from jain_ai.services.chat_service import handle_chat_turn
from jain_ai.services.session_service import clear_chat_history


def evaluate(questions_file=None, output_file="eval_results.md"):
    if questions_file is None:
        questions_file = os.path.join(BASE_DIR, "tests", "eval_questions.json")

    with open(questions_file, "r", encoding="utf-8") as f:
        questions = json.load(f)

    app = create_app()
    pipeline = get_rag_pipeline()
    pipeline.initialize()

    results = []
    total = len(questions)
    retrieval_hits = 0
    answer_passes = 0

    print(f"Starting evaluation on {total} questions at {datetime.now().isoformat()}...\n")

    with app.test_request_context("/"):
        for q in questions:
            qid = q.get("id", "")
            query = q["query"]
            expected = q.get("expect", [])
            if isinstance(expected, str):
                expected = [expected]
            expected_source = q.get("expected_source", "")
            refuse_expected = q.get("refuse", False)

            clear_chat_history()

            # 1. Evaluate Retrieval
            context_bundle = pipeline.build_context_bundle(query)
            sources = context_bundle.get("sources", [])
            retrieved_sources_str = ", ".join(f"{s.get('folder')}/{s.get('file')}" for s in sources)
            top_source = f"{sources[0].get('folder')}/{sources[0].get('file')}" if sources else "None"

            retrieval_hit = False
            if expected_source:
                # Top source match or anywhere in retrieved sources
                retrieval_hit = any(expected_source.lower() in s.get("file", "").lower() for s in sources)
            else:
                retrieval_hit = True if refuse_expected else False

            if retrieval_hit:
                retrieval_hits += 1

            time.sleep(1.0)
            # 2. Evaluate Answer Generation
            answer = handle_chat_turn(query, None)

            answer_pass = False
            normalized_answer = re.sub(r"\s+", " ", answer.lower()).strip()

            if refuse_expected:
                refusal_markers = [
                    "does not contain",
                    "not contain this information",
                    "could not find",
                    "does not have information",
                    "source material does not",
                    "no information",
                    "cannot find",
                    "available source material does not contain",
                ]
                answer_pass = any(marker in normalized_answer for marker in refusal_markers)
            else:
                # All expected substrings must be in the answer
                answer_pass = all(re.sub(r"\s+", " ", item.lower()).strip() in normalized_answer for item in expected)

            if answer_pass:
                answer_passes += 1

            status_str = "PASS" if (retrieval_hit and answer_pass) else "MISS"
            print(f"[{qid}] {query[:50]:<50} | Retrieval: {'YES' if retrieval_hit else 'NO'} | Answer: {'PASS' if answer_pass else 'FAIL'} | Overall: {status_str}")

            results.append({
                "id": qid,
                "query": query,
                "expected": expected,
                "expected_source": expected_source,
                "refuse": refuse_expected,
                "retrieval_hit": retrieval_hit,
                "top_source": top_source,
                "all_sources": retrieved_sources_str,
                "answer_pass": answer_pass,
                "answer": answer.replace("\n", " ").strip(),
                "status": status_str,
            })

    retrieval_pct = (retrieval_hits / total) * 100 if total else 0
    answer_pct = (answer_passes / total) * 100 if total else 0

    print("\n" + "=" * 60)
    print(f"EVALUATION SUMMARY")
    print(f"Total Questions : {total}")
    print(f"Retrieval Hits  : {retrieval_hits}/{total} ({retrieval_pct:.1f}%)")
    print(f"Answer Passes   : {answer_passes}/{total} ({answer_pct:.1f}%)")
    print("=" * 60)

    # Format Markdown Report
    lines = [
        f"# Evaluation Results",
        f"",
        f"- **Timestamp**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"- **Total Questions**: {total}",
        f"- **Retrieval Hits**: {retrieval_hits}/{total} ({retrieval_pct:.1f}%)",
        f"- **Answer Passes**: {answer_passes}/{total} ({answer_pct:.1f}%)",
        f"",
        f"## Detailed Results",
        f"",
        f"| ID | Query | Expected | Expected Source | Top Source | Retrieval Hit | Answer Pass | Status |",
        f"|---|---|---|---|---|:---:|:---:|:---:|",
    ]

    for r in results:
        exp_display = "Refusal" if r["refuse"] else ", ".join(r["expected"])
        lines.append(
            f"| {r['id']} | {r['query']} | {exp_display} | {r['expected_source'] or 'N/A'} | {r['top_source']} | "
            f"{'✅' if r['retrieval_hit'] else '❌'} | {'✅' if r['answer_pass'] else '❌'} | **{r['status']}** |"
        )

    lines.append("")
    lines.append("## Answers Breakdown")
    lines.append("")
    for r in results:
        lines.append(f"### `{r['id']}`: {r['query']}")
        lines.append(f"- **Top Source**: {r['top_source']}")
        lines.append(f"- **All Sources**: {r['all_sources']}")
        lines.append(f"- **Answer**: {r['answer']}")
        lines.append(f"- **Retrieval Hit**: {'YES' if r['retrieval_hit'] else 'NO'} | **Answer Pass**: {'PASS' if r['answer_pass'] else 'FAIL'}")
        lines.append("")

    report_content = "\n".join(lines)
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(report_content)

    print(f"\nReport written to {output_file}")
    return retrieval_hits, answer_passes, total


if __name__ == "__main__":
    out_file = sys.argv[1] if len(sys.argv) > 1 else "eval_results.md"
    evaluate(output_file=out_file)
