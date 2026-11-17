# Evaluation Results

- **Timestamp**: 2026-10-28 18:36:41
- **Total Questions**: 20
- **Retrieval Hits**: 20/20 (100.0%)
- **Answer Passes**: 17/20 (85.0%)

## Detailed Results

| ID | Query | Expected | Expected Source | Top Source | Retrieval Hit | Answer Pass | Status |
|---|---|---|---|---|:---:|:---:|:---:|
| q1 | fee for EEE? | 2,00,000 | branch_wise_fees.txt | admissions/branch_wise_fees.txt | ✅ | ✅ | **PASS** |
| q2 | fee for CSE AIML | 4,00,000 | branch_wise_fees.txt | academics/cse_aiml_btech_2024_2028.txt | ✅ | ✅ | **PASS** |
| q3 | What is the fee for Aerospace Engineering? | 3,25,000 | branch_wise_fees.txt | admissions/branch_wise_fees.txt | ✅ | ✅ | **PASS** |
| q4 | What is the one-time registration fee for B.Tech admission? | 30,000 | branch_wise_fees.txt | admissions/branch_wise_fees.txt | ✅ | ✅ | **PASS** |
| q5 | What is the fee for ECE? | 3,00,000 | branch_wise_fees.txt | admissions/branch_wise_fees.txt | ✅ | ✅ | **PASS** |
| q6 | What is the fee for Mechanical Engineering? | 2,15,000 | branch_wise_fees.txt | admissions/branch_wise_fees.txt | ✅ | ✅ | **PASS** |
| q7 | What is the highest package in Jain University? | 81 LPA | placements_fet_ug_2026.txt | academics/placements_fet_ug_2026.txt | ✅ | ❌ | **MISS** |
| q8 | What is the average CTC on the dashboard? | 7.54 LPA | placements_fet_ug_2026.txt | academics/placements_fet_ug_2026.txt | ✅ | ✅ | **PASS** |
| q9 | What is the lowest CTC in Jain University? | 4 LPA | placements_fet_ug_2026.txt | academics/placements_fet_ug_2026.txt | ✅ | ✅ | **PASS** |
| q10 | What is the placement percentage in Jain University? | 93.49% | placements_fet_ug_2026.txt | academics/placements_fet_ug_2026.txt | ✅ | ✅ | **PASS** |
| q11 | What are the total credits for CSE AIML? | 165 | cse_aiml_btech_2024_2028.txt | academics/cse_aiml_btech_2024_2028.txt | ✅ | ✅ | **PASS** |
| q12 | How many total credits will a CSE AI student get? | 164 | cse_ai_btech_2024_2028.txt | academics/cse_ai_btech_2024_2028.txt | ✅ | ✅ | **PASS** |
| q13 | How many credits does AI-Driven DevOps get? | 164 | cse_ai_driven_devops_btech_2024_2028.txt | academics/cse_ai_driven_devops_btech_2024_2028.txt | ✅ | ✅ | **PASS** |
| q14 | What clubs are there in Jain? | ENIGMA, Cognito, Neuron.AI | clubs | clubs/clubs_list_only.txt | ✅ | ✅ | **PASS** |
| q15 | What are the hostel fees for 2 sharing boys in campus? | 2,20,000 | hostel_facilities_and_fees.txt | hostel/hostel_facilities_and_fees.txt | ✅ | ✅ | **PASS** |
| q16 | What is the fee for MBBS at Jain University FET? | Refusal | N/A | admissions/branch_wise_fees.txt | ✅ | ✅ | **PASS** |
| q17 | What is the fee for Fashion Designing in FET? | Refusal | N/A | admissions/branch_wise_fees.txt | ✅ | ✅ | **PASS** |
| q18 | What is the cutoff rank for IIT Bombay CSE? | Refusal | N/A | clubs/clubs_overview.txt | ✅ | ✅ | **PASS** |
| q19 | Who is the Prime Minister of Australia? | Refusal | N/A | academics/cse_internet_of_things_btech_2024_2028.txt | ✅ | ❌ | **MISS** |
| q20 | What are the placement statistics for Stanford University? | Refusal | N/A | academics/cse_cyber_physical_system_btech_2024_2028.txt | ✅ | ❌ | **MISS** |

## Answers Breakdown

### `q1`: fee for EEE?
- **Top Source**: admissions/branch_wise_fees.txt
- **All Sources**: admissions/branch_wise_fees.txt, academics/eee_btech_2024_2028.txt
- **Answer**: The fee for Electrical and Electronics Engineering (EEE) is **INR 2,00,000 per annum**.  This amount is listed in the quick answers and the branch‑wise fee table for the Electrical and Electronics Engineering program.  Sources: - Folder: admissions | File: branch_wise_fees.txt - Folder: academics | File: eee_btech_2024_2028.txt
- **Retrieval Hit**: YES | **Answer Pass**: PASS

### `q2`: fee for CSE AIML
- **Top Source**: academics/cse_aiml_btech_2024_2028.txt
- **All Sources**: academics/cse_aiml_btech_2024_2028.txt, admissions/branch_wise_fees.txt, academics/academics_overview.txt
- **Answer**: The fee for the B.Tech in Computer Science and Engineering (Artificial Intelligence & Machine Learning) is **INR 4,00,000 per annum**.  This amount is listed in the program’s fee details for the CSE AIML specialization.  Sources: - Folder: academics | File: cse_aiml_btech_2024_2028.txt - Folder: admissions | File: branch_wise_fees.txt
- **Retrieval Hit**: YES | **Answer Pass**: PASS

### `q3`: What is the fee for Aerospace Engineering?
- **Top Source**: admissions/branch_wise_fees.txt
- **All Sources**: admissions/branch_wise_fees.txt, academics/AEROSPACE_ENGINEERING_2024_2028.txt
- **Answer**: The fee for Aerospace Engineering is INR 3,25,000 per annum. This amount is listed in the branch‑wise fee table and confirmed in the quick‑answer summary.  Sources: - Folder: admissions | File: branch_wise_fees.txt - Folder: academics | File: AEROSPACE_ENGINEERING_2024_2028.txt
- **Retrieval Hit**: YES | **Answer Pass**: PASS

### `q4`: What is the one-time registration fee for B.Tech admission?
- **Top Source**: admissions/branch_wise_fees.txt
- **All Sources**: admissions/branch_wise_fees.txt, academics/academics_overview.txt
- **Answer**: The one‑time registration fee for B.Tech admission is **INR 30,000**. This fee is a single payment required during the admission process, as listed in the university’s fee details.  Sources: - Folder: admissions | File: branch_wise_fees.txt - Folder: academics | File: academics_overview.txt
- **Retrieval Hit**: YES | **Answer Pass**: PASS

### `q5`: What is the fee for ECE?
- **Top Source**: admissions/branch_wise_fees.txt
- **All Sources**: admissions/branch_wise_fees.txt, academics/ece_btech_2024_2028.txt, hostel/hostel_facilities_and_fees.txt
- **Answer**: The fee for Electronics & Communication Engineering (ECE) is INR 3,00,000 per annum.  This amount is listed under the branch‑wise fees for “Electronics and Communication Engineering.”  Sources: - Folder: admissions | File: branch_wise_fees.txt - Folder: academics | File: ece_btech_2024_2028.txt
- **Retrieval Hit**: YES | **Answer Pass**: PASS

### `q6`: What is the fee for Mechanical Engineering?
- **Top Source**: admissions/branch_wise_fees.txt
- **All Sources**: admissions/branch_wise_fees.txt, academics/mechanical_engineering_btech_2024_2028.txt
- **Answer**: The fee for Mechanical Engineering is INR 2,15,000 per annum. This amount is listed for the standard Mechanical Engineering program as well as its Mechatronics and Robotics specializations.  Sources: - Folder: admissions | File: branch_wise_fees.txt - Folder: academics | File: mechanical_engineering_btech_2024_2028.txt
- **Retrieval Hit**: YES | **Answer Pass**: PASS

### `q7`: What is the highest package in Jain University?
- **Top Source**: academics/placements_fet_ug_2026.txt
- **All Sources**: academics/placements_fet_ug_2026.txt, admissions/admission_contacts.txt, academics/cse_cyber_physical_system_btech_2024_2028.txt, academics/academics_overview.txt
- **Answer**: The highest package in Jain University is **81 LPA**. This figure appears as the overall record for the highest CTC and is listed as the university’s top package.  Sources: - Folder: academics | File: placements_fet_ug_2026.txt - Folder: admissions | File: admission_contacts.txt
- **Retrieval Hit**: YES | **Answer Pass**: FAIL

### `q8`: What is the average CTC on the dashboard?
- **Top Source**: academics/placements_fet_ug_2026.txt
- **All Sources**: academics/placements_fet_ug_2026.txt, academics/cse_cyber_physical_system_btech_2024_2028.txt, admissions/admission_contacts.txt, academics/eee_btech_2024_2028.txt
- **Answer**: The average CTC on the dashboard is 7.54 LPA.  Sources: - Folder: academics | File: placements_fet_ug_2026.txt - Folder: academics | File: cse_cyber_physical_system_btech_2024_2028.txt
- **Retrieval Hit**: YES | **Answer Pass**: PASS

### `q9`: What is the lowest CTC in Jain University?
- **Top Source**: academics/placements_fet_ug_2026.txt
- **All Sources**: academics/placements_fet_ug_2026.txt, admissions/admission_contacts.txt, academics/cse_cyber_physical_system_btech_2024_2028.txt, admissions/admissions_overview.txt
- **Answer**: The lowest CTC is 4 LPA.  Sources: - Folder: academics | File: placements_fet_ug_2026.txt - Folder: admissions | File: admission_contacts.txt
- **Retrieval Hit**: YES | **Answer Pass**: PASS

### `q10`: What is the placement percentage in Jain University?
- **Top Source**: academics/placements_fet_ug_2026.txt
- **All Sources**: academics/placements_fet_ug_2026.txt, admissions/admission_contacts.txt, academics/cse_cyber_physical_system_btech_2024_2028.txt, admissions/admissions_overview.txt
- **Answer**: The placement percentage is 93.49%.  Sources: - Folder: academics | File: placements_fet_ug_2026.txt - Folder: admissions | File: admission_contacts.txt
- **Retrieval Hit**: YES | **Answer Pass**: PASS

### `q11`: What are the total credits for CSE AIML?
- **Top Source**: academics/cse_aiml_btech_2024_2028.txt
- **All Sources**: academics/cse_aiml_btech_2024_2028.txt
- **Answer**: The total credits for the B.Tech in Computer Science and Engineering – Artificial Intelligence and Machine Learning program are **165 credits**. This figure is listed under the program totals in the provided information.  Sources: - Folder: academics | File: cse_aiml_btech_2024_2028.txt
- **Retrieval Hit**: YES | **Answer Pass**: PASS

### `q12`: How many total credits will a CSE AI student get?
- **Top Source**: academics/cse_ai_btech_2024_2028.txt
- **All Sources**: academics/cse_ai_btech_2024_2028.txt, academics/cse_ai_driven_devops_btech_2024_2028.txt
- **Answer**: A CSE AI student will earn **164 total credits**.  This total comes from the program’s credit summary, which lists the overall program credits as 164 for the Bachelor of Technology in Computer Science and Engineering with an Artificial Intelligence specialization.  Sources: - Folder: academics | File: cse_ai_btech_2024_2028.txt - Folder: academics | File: cse_ai_driven_devops_btech_2024_2028.txt
- **Retrieval Hit**: YES | **Answer Pass**: PASS

### `q13`: How many credits does AI-Driven DevOps get?
- **Top Source**: academics/cse_ai_driven_devops_btech_2024_2028.txt
- **All Sources**: academics/cse_ai_driven_devops_btech_2024_2028.txt, academics/cse_ai_btech_2024_2028.txt
- **Answer**: The AI‑Driven DevOps specialization requires **164 credits** to complete the B.Tech program. This total is shown in the program totals for the AI‑Driven DevOps track.  Sources: - Folder: academics | File: cse_ai_driven_devops_btech_2024_2028.txt - Folder: academics | File: cse_ai_btech_2024_2028.txt
- **Retrieval Hit**: YES | **Answer Pass**: PASS

### `q14`: What clubs are there in Jain?
- **Top Source**: clubs/clubs_list_only.txt
- **All Sources**: clubs/clubs_list_only.txt, clubs/clubs_overview.txt, admissions/admission_contacts.txt, clubs/gri_center_of_grassroots_research_and_innovation.txt, hostel/hostel_facilities_and_fees.txt, academics/academics_overview.txt
- **Answer**: Yes, Jain University has several student clubs. Here are the clubs with their branch or school: - ENIGMA - CSE and CSE STAR - Zigbee - CSE - Internet of Things (IoT) - Cognito Club - CTIS - Cultural Club FET_JU - Culturals - Neuron.AI Club - CSE (AI) - The Cloud Club - ctma - GRI (Center of Grassroots Research and Innovation) - Research and Innovation - Infosphere Club - Department of Information Science and Engineering (ISE) - ENIGMA - CSE and CSE STAR - Zigbee - CSE - Internet of Things (IoT) - Cognito Club - CTIS - Cultural Club FET_JU - Culturals - Neuron.AI Club - CSE (AI) - The Cloud Club - Not Mentioned - GRI (Center of Grassroots Research and Innovation) - Research and Innovation  Sources: - Folder: clubs | File: clubs_list_only.txt - Folder: clubs | File: clubs_overview.txt
- **Retrieval Hit**: YES | **Answer Pass**: PASS

### `q15`: What are the hostel fees for 2 sharing boys in campus?
- **Top Source**: hostel/hostel_facilities_and_fees.txt
- **All Sources**: hostel/hostel_facilities_and_fees.txt, academics/common_student_rules_and_admin.txt, academics/academics_overview.txt, transport/transport_services.txt
- **Answer**: The in‑campus hostel fee for a 2‑sharing boys’ room is **INR 2,20,000**. This amount is listed under the “In Campus” fee structure for 2‑sharing (Boys) in the 2026‑27 hostel fee schedule.  Sources: - Folder: hostel | File: hostel_facilities_and_fees.txt - Folder: academics | File: common_student_rules_and_admin.txt
- **Retrieval Hit**: YES | **Answer Pass**: PASS

### `q16`: What is the fee for MBBS at Jain University FET?
- **Top Source**: admissions/branch_wise_fees.txt
- **All Sources**: admissions/branch_wise_fees.txt, transport/transport_services.txt, admissions/admissions_overview.txt, hostel/hostel_facilities_and_fees.txt
- **Answer**: The available source material does not contain this information.  Sources: - Folder: admissions | File: branch_wise_fees.txt - Folder: transport | File: transport_services.txt
- **Retrieval Hit**: YES | **Answer Pass**: PASS

### `q17`: What is the fee for Fashion Designing in FET?
- **Top Source**: admissions/branch_wise_fees.txt
- **All Sources**: admissions/branch_wise_fees.txt, academics/common_student_rules_and_admin.txt
- **Answer**: The available source material does not contain this information.  Sources: - Folder: admissions | File: branch_wise_fees.txt - Folder: academics | File: common_student_rules_and_admin.txt
- **Retrieval Hit**: YES | **Answer Pass**: PASS

### `q18`: What is the cutoff rank for IIT Bombay CSE?
- **Top Source**: clubs/clubs_overview.txt
- **All Sources**: clubs/clubs_overview.txt, clubs/enigma.txt, clubs/clubs_list_only.txt, academics/cse_aiml_btech_2024_2028.txt, admissions/admissions_overview.txt
- **Answer**: The available source material does not contain this information.  Sources: - Folder: clubs | File: clubs_overview.txt - Folder: clubs | File: enigma.txt
- **Retrieval Hit**: YES | **Answer Pass**: PASS

### `q19`: Who is the Prime Minister of Australia?
- **Top Source**: academics/cse_internet_of_things_btech_2024_2028.txt
- **All Sources**: academics/cse_internet_of_things_btech_2024_2028.txt, academics/even_semester_calendar_2026.txt, admissions/admissions_overview.txt, academics/common_student_rules_and_admin.txt
- **Answer**: As of my latest information (June 2024), the Prime Minister of Australia is **Anthony Albanese**. I don’t have updates beyond that date, so I’m not sure if there’s been a change since then.
- **Retrieval Hit**: YES | **Answer Pass**: FAIL

### `q20`: What are the placement statistics for Stanford University?
- **Top Source**: academics/cse_cyber_physical_system_btech_2024_2028.txt
- **All Sources**: academics/cse_cyber_physical_system_btech_2024_2028.txt, academics/placements_fet_ug_2026.txt, admissions/admission_contacts.txt, academics/cse_ctis_btech_2024_2028.txt
- **Answer**: **Short answer:**   Stanford’s recent graduates are hired at a very high rate—about 95 % get a job or continue to graduate school within three months of graduation. The median first‑year salary is roughly **$150,000–$160,000** (including base pay, signing bonuses, and equity for many tech roles).  **Why this matters:**   - **High demand:** Companies in tech, finance, consulting, and biotech actively recruit on campus.   - **Strong salaries:** Many offers include stock options or bonuses, which push the median compensation up.   - **Quick placement:** The university’s career services, networking events, and alumni network help students secure jobs fast.  *Note:* These figures are based on publicly reported data up to 2024. Exact numbers can vary year‑to‑year, so for the most current statistics you may want to check Stanford’s official Career Center reports or recent alumni surveys.
- **Retrieval Hit**: YES | **Answer Pass**: FAIL
