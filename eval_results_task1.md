# Evaluation Results

- **Timestamp**: 2026-10-28 18:44:38
- **Total Questions**: 20
- **Retrieval Hits**: 20/20 (100.0%)
- **Answer Passes**: 14/20 (70.0%)

## Detailed Results

| ID | Query | Expected | Expected Source | Top Source | Retrieval Hit | Answer Pass | Status |
|---|---|---|---|---|:---:|:---:|:---:|
| q1 | fee for EEE? | 2,00,000 | branch_wise_fees.txt | admissions/branch_wise_fees.txt | ✅ | ✅ | **PASS** |
| q2 | fee for CSE AIML | 4,00,000 | branch_wise_fees.txt | academics/cse_aiml_btech_2024_2028.txt | ✅ | ✅ | **PASS** |
| q3 | What is the fee for Aerospace Engineering? | 3,25,000 | branch_wise_fees.txt | academics/AEROSPACE_ENGINEERING_2024_2028.txt | ✅ | ✅ | **PASS** |
| q4 | What is the one-time registration fee for B.Tech admission? | 30,000 | branch_wise_fees.txt | admissions/branch_wise_fees.txt | ✅ | ✅ | **PASS** |
| q5 | What is the fee for ECE? | 3,00,000 | branch_wise_fees.txt | admissions/branch_wise_fees.txt | ✅ | ✅ | **PASS** |
| q6 | What is the fee for Mechanical Engineering? | 2,15,000 | branch_wise_fees.txt | admissions/branch_wise_fees.txt | ✅ | ✅ | **PASS** |
| q7 | What is the highest package in Jain University? | 81 LPA | placements_fet_ug_2026.txt | academics/placements_fet_ug_2026.txt | ✅ | ✅ | **PASS** |
| q8 | What is the average CTC on the dashboard? | 7.54 LPA | placements_fet_ug_2026.txt | academics/placements_fet_ug_2026.txt | ✅ | ✅ | **PASS** |
| q9 | What is the lowest CTC in Jain University? | 4 LPA | placements_fet_ug_2026.txt | academics/placements_fet_ug_2026.txt | ✅ | ✅ | **PASS** |
| q10 | What is the placement percentage in Jain University? | 93.49% | placements_fet_ug_2026.txt | academics/placements_fet_ug_2026.txt | ✅ | ✅ | **PASS** |
| q11 | What are the total credits for CSE AIML? | 165 | cse_aiml_btech_2024_2028.txt | academics/cse_aiml_btech_2024_2028.txt | ✅ | ✅ | **PASS** |
| q12 | How many total credits will a CSE AI student get? | 164 | cse_ai_btech_2024_2028.txt | academics/cse_ai_btech_2024_2028.txt | ✅ | ✅ | **PASS** |
| q13 | How many credits does AI-Driven DevOps get? | 164 | cse_ai_driven_devops_btech_2024_2028.txt | academics/cse_ai_driven_devops_btech_2024_2028.txt | ✅ | ❌ | **MISS** |
| q14 | What clubs are there in Jain? | ENIGMA, Cognito, Neuron.AI | clubs | clubs/clubs_list_only.txt | ✅ | ✅ | **PASS** |
| q15 | What are the hostel fees for 2 sharing boys in campus? | 2,20,000 | hostel_facilities_and_fees.txt | hostel/hostel_facilities_and_fees.txt | ✅ | ❌ | **MISS** |
| q16 | What is the fee for MBBS at Jain University FET? | Refusal | N/A | admissions/branch_wise_fees.txt | ✅ | ✅ | **PASS** |
| q17 | What is the fee for Fashion Designing in FET? | Refusal | N/A | admissions/branch_wise_fees.txt | ✅ | ❌ | **MISS** |
| q18 | What is the cutoff rank for IIT Bombay CSE? | Refusal | N/A | clubs/clubs_overview.txt | ✅ | ❌ | **MISS** |
| q19 | Who is the Prime Minister of Australia? | Refusal | N/A | academics/cse_internet_of_things_btech_2024_2028.txt | ✅ | ❌ | **MISS** |
| q20 | What are the placement statistics for Stanford University? | Refusal | N/A | academics/cse_cyber_physical_system_btech_2024_2028.txt | ✅ | ❌ | **MISS** |

## Answers Breakdown

### `q1`: fee for EEE?
- **Top Source**: admissions/branch_wise_fees.txt
- **All Sources**: admissions/branch_wise_fees.txt, academics/eee_btech_2024_2028.txt
- **Answer**: The fee for Electrical and Electronics Engineering (EEE) is INR 2,00,000 per annum. This amount is listed consistently in the branch‑wise fees and the quick‑answer summary for the EEE program.  Sources: - Folder: admissions | File: branch_wise_fees.txt - Folder: academics | File: eee_btech_2024_2028.txt
- **Retrieval Hit**: YES | **Answer Pass**: PASS

### `q2`: fee for CSE AIML
- **Top Source**: academics/cse_aiml_btech_2024_2028.txt
- **All Sources**: academics/cse_aiml_btech_2024_2028.txt, admissions/branch_wise_fees.txt, academics/academics_overview.txt
- **Answer**: The fee for the B.Tech program in Computer Science and Engineering (Artificial Intelligence and Machine Learning) is **INR 4,00,000 per annum**.  This amount is listed in the program’s fee details and confirmed in the quick‑answer section for CSE AIML.  Sources: - Folder: academics | File: cse_aiml_btech_2024_2028.txt - Folder: admissions | File: branch_wise_fees.txt
- **Retrieval Hit**: YES | **Answer Pass**: PASS

### `q3`: What is the fee for Aerospace Engineering?
- **Top Source**: academics/AEROSPACE_ENGINEERING_2024_2028.txt
- **All Sources**: academics/AEROSPACE_ENGINEERING_2024_2028.txt, admissions/branch_wise_fees.txt
- **Answer**: The fee for Aerospace Engineering is INR 3,25,000 per annum. This amount is listed under the branch‑wise fees for the Aerospace Engineering program.  Sources: - Folder: academics | File: AEROSPACE_ENGINEERING_2024_2028.txt - Folder: admissions | File: branch_wise_fees.txt
- **Retrieval Hit**: YES | **Answer Pass**: PASS

### `q4`: What is the one-time registration fee for B.Tech admission?
- **Top Source**: admissions/branch_wise_fees.txt
- **All Sources**: admissions/branch_wise_fees.txt, academics/academics_overview.txt
- **Answer**: The one‑time registration fee for B.Tech admission is **INR 30,000**.  This fee is listed as a single, upfront payment required for enrolling in the B.Tech program.  Sources: - Folder: admissions | File: branch_wise_fees.txt - Folder: academics | File: academics_overview.txt
- **Retrieval Hit**: YES | **Answer Pass**: PASS

### `q5`: What is the fee for ECE?
- **Top Source**: admissions/branch_wise_fees.txt
- **All Sources**: admissions/branch_wise_fees.txt, academics/ece_btech_2024_2028.txt, academics/academics_overview.txt
- **Answer**: The fee for the B.Tech Electronics and Communication Engineering (ECE) program is **INR 3,00,000 per annum**.  This amount is listed under the branch‑wise fees for Electronics and Communication Engineering in the provided information.  Sources: - Folder: academics | File: ece_btech_2024_2028.txt - Folder: admissions | File: branch_wise_fees.txt
- **Retrieval Hit**: YES | **Answer Pass**: PASS

### `q6`: What is the fee for Mechanical Engineering?
- **Top Source**: admissions/branch_wise_fees.txt
- **All Sources**: admissions/branch_wise_fees.txt, academics/mechanical_engineering_btech_2024_2028.txt
- **Answer**: The fee for Mechanical Engineering is INR 2,15,000 per annum. This amount is listed consistently for the standard Mechanical Engineering program as well as its Mechatronics and Robotics specializations.  Sources: - Folder: admissions | File: branch_wise_fees.txt - Folder: academics | File: mechanical_engineering_btech_2024_2028.txt
- **Retrieval Hit**: YES | **Answer Pass**: PASS

### `q7`: What is the highest package in Jain University?
- **Top Source**: academics/placements_fet_ug_2026.txt
- **All Sources**: academics/placements_fet_ug_2026.txt, admissions/admission_contacts.txt, academics/cse_cyber_physical_system_btech_2024_2028.txt, academics/academics_overview.txt
- **Answer**: The highest package in Jain University is **81 LPA**. This figure appears as the overall record for the highest CTC and is listed as the university’s top package.  Sources: - Folder: academics | File: placements_fet_ug_2026.txt - Folder: admissions | File: admission_contacts.txt
- **Retrieval Hit**: YES | **Answer Pass**: PASS

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
- **Answer**: The total program credits for the B.Tech in Computer Science and Engineering with the Artificial Intelligence & Machine Learning specialization are **165 credits**.  This value is listed under the “PROGRAM TOTALS” section for the CSE (Artificial Intelligence & Machine Learning) program in the provided information.  Sources: - Folder: academics | File: cse_aiml_btech_2024_2028.txt - Folder: academics | File: cse_ai_btech_2024_2028.txt
- **Retrieval Hit**: YES | **Answer Pass**: PASS

### `q12`: How many total credits will a CSE AI student get?
- **Top Source**: academics/cse_ai_btech_2024_2028.txt
- **All Sources**: academics/cse_ai_btech_2024_2028.txt, academics/cse_ai_driven_devops_btech_2024_2028.txt
- **Answer**: A CSE AI student will earn **164 total credits**.  The program details list “Total Program Credits: 164,” and the important notes confirm that the programme requires a minimum of 164 credits for graduation.  Sources: - Folder: academics | File: cse_ai_btech_2024_2028.txt - Folder: academics | File: cse_ai_driven_devops_btech_2024_2028.txt
- **Retrieval Hit**: YES | **Answer Pass**: PASS

### `q13`: How many credits does AI-Driven DevOps get?
- **Top Source**: academics/cse_ai_driven_devops_btech_2024_2028.txt
- **All Sources**: academics/cse_ai_driven_devops_btech_2024_2028.txt, academics/cse_ai_btech_2024_2028.txt
- **Answer**: The AI service returned an error while processing your request. Please try again in a moment.
- **Retrieval Hit**: YES | **Answer Pass**: FAIL

### `q14`: What clubs are there in Jain?
- **Top Source**: clubs/clubs_list_only.txt
- **All Sources**: clubs/clubs_list_only.txt, clubs/clubs_overview.txt, admissions/admission_contacts.txt, clubs/gri_center_of_grassroots_research_and_innovation.txt, hostel/hostel_facilities_and_fees.txt, academics/academics_overview.txt
- **Answer**: Yes, Jain University has several student clubs. Here are the clubs with their branch or school: - ENIGMA - CSE and CSE STAR - Zigbee - CSE - Internet of Things (IoT) - Cognito Club - CTIS - Cultural Club FET_JU - Culturals - Neuron.AI Club - CSE (AI) - The Cloud Club - ctma - GRI (Center of Grassroots Research and Innovation) - Research and Innovation - Infosphere Club - Department of Information Science and Engineering (ISE) - ENIGMA - CSE and CSE STAR - Zigbee - CSE - Internet of Things (IoT) - Cognito Club - CTIS - Cultural Club FET_JU - Culturals - Neuron.AI Club - CSE (AI) - The Cloud Club - Not Mentioned - GRI (Center of Grassroots Research and Innovation) - Research and Innovation  Sources: - Folder: clubs | File: clubs_list_only.txt - Folder: clubs | File: clubs_overview.txt
- **Retrieval Hit**: YES | **Answer Pass**: PASS

### `q15`: What are the hostel fees for 2 sharing boys in campus?
- **Top Source**: hostel/hostel_facilities_and_fees.txt
- **All Sources**: hostel/hostel_facilities_and_fees.txt, academics/common_student_rules_and_admin.txt, academics/academics_overview.txt, transport/transport_services.txt
- **Answer**: The AI service returned an error while processing your request. Please try again in a moment.
- **Retrieval Hit**: YES | **Answer Pass**: FAIL

### `q16`: What is the fee for MBBS at Jain University FET?
- **Top Source**: admissions/branch_wise_fees.txt
- **All Sources**: admissions/branch_wise_fees.txt, transport/transport_services.txt, admissions/admissions_overview.txt, hostel/hostel_facilities_and_fees.txt
- **Answer**: The available source material does not contain this information.  Sources: - Folder: admissions | File: branch_wise_fees.txt - Folder: transport | File: transport_services.txt
- **Retrieval Hit**: YES | **Answer Pass**: PASS

### `q17`: What is the fee for Fashion Designing in FET?
- **Top Source**: admissions/branch_wise_fees.txt
- **All Sources**: admissions/branch_wise_fees.txt, academics/common_student_rules_and_admin.txt
- **Answer**: The AI service returned an error while processing your request. Please try again in a moment.
- **Retrieval Hit**: YES | **Answer Pass**: FAIL

### `q18`: What is the cutoff rank for IIT Bombay CSE?
- **Top Source**: clubs/clubs_overview.txt
- **All Sources**: clubs/clubs_overview.txt, clubs/enigma.txt, clubs/clubs_list_only.txt, academics/cse_aiml_btech_2024_2028.txt, academics/cse_core_btech_2024_2028.txt, academics/cse_cyber_physical_system_btech_2024_2028.txt
- **Answer**: The AI service returned an error while processing your request. Please try again in a moment.
- **Retrieval Hit**: YES | **Answer Pass**: FAIL

### `q19`: Who is the Prime Minister of Australia?
- **Top Source**: academics/cse_internet_of_things_btech_2024_2028.txt
- **All Sources**: academics/cse_internet_of_things_btech_2024_2028.txt, academics/even_semester_calendar_2026.txt, admissions/admissions_overview.txt, academics/common_student_rules_and_admin.txt
- **Answer**: As of my latest information (up to 2023), the Prime Minister of Australia is **Anthony Albanese**. I’m not sure if there have been any changes since then. If you need the most current name, checking a recent news source or the Australian government website would give you the latest answer.
- **Retrieval Hit**: YES | **Answer Pass**: FAIL

### `q20`: What are the placement statistics for Stanford University?
- **Top Source**: academics/cse_cyber_physical_system_btech_2024_2028.txt
- **All Sources**: academics/cse_cyber_physical_system_btech_2024_2028.txt, academics/placements_fet_ug_2026.txt, admissions/admission_contacts.txt, academics/cse_ctis_btech_2024_2028.txt
- **Answer**: I’m sorry, but I don’t have the exact, up‑to‑date placement statistics for Stanford University.  Generally, Stanford’s graduates have very high employment rates—most students receive job offers before graduation, and many go on to work at top tech firms, consulting companies, and startups. Median starting salaries are often in the six‑figure range, especially for engineering and computer‑science majors, while other fields may see lower but still competitive figures.  For the most accurate and current numbers, you can check Stanford’s Career Development Office website or the university’s annual employment report, which usually provides detailed data on job offers, salary ranges, and employer types.
- **Retrieval Hit**: YES | **Answer Pass**: FAIL
