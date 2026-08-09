# Norway Future Skills & Job Market Intelligence

A portfolio data-analysis project exploring **current skill demand, digital skills, AI-related demand, and geographic differences in the Norwegian job market** using 10,000 job postings from NAV Arbeidsplassen.

## Project question

> **What skills are currently demanded in Norway, where is digital demand concentrated, and what skills tend to accompany AI-related work?**

The project originally started with the broader question:

> *How is AI changing the Norwegian labor market, and what skills will matter in the future?*

Because the dataset is a **current snapshot rather than a historical time series**, the analysis does not claim that AI caused changes over time. Instead, it focuses on **current labor-market demand and associations**.

---

## Key findings

- **10,000** Norwegian job postings analyzed
- **10,997** unique observed skill labels
- **975 jobs (9.75%)** contained at least one high-confidence core digital skill
- **1,509 jobs (15.09%)** contained at least one expanded validated digital skill
- **87 jobs (0.87%)** were identified as AI-linked using a conservative ESCO-based definition
- Frequently demanded digital skills included:
  - Digitalisering
  - IT
  - Dataanalyse
  - Python
  - Informasjonssikkerhet
  - IT-sikkerhet
  - Java
  - DevOps
  - Maskinlæring
- AI-linked jobs frequently appeared alongside skills related to:
  - Python
  - programming
  - data analysis
  - statistics
  - SQL
  - data platforms
  - software development
  - automation
- **Oslo** had the largest absolute volume of digital-skill jobs
- **Kongsberg** showed the highest core digital concentration among the 15 largest city markets in the sample, at approximately **32.6%**
- Trondheim and Bergen also showed relatively high digital intensity

---

## Why this project?

Job-market datasets often contain thousands of inconsistent skill labels, mixed languages, missing classifications, and highly fragmented job titles.

The goal was therefore not only to count skills, but to build a reproducible workflow that could answer practical questions such as:

- Which skills are most frequently requested?
- Which Norwegian cities have stronger digital-skill demand?
- Which skills can be confidently classified as digital?
- How large is explicit AI-related demand?
- What complementary capabilities should someone learn alongside AI?
- What kinds of jobs are connected to those skills?

---

## Data

Job postings were collected from **NAV Arbeidsplassen** and cleaned into a fixed analysis dataset containing **10,000 postings**.

Main cleaned fields include:

- `job_id`
- `title`
- `company`
- `published`
- `expires`
- `city`
- `occupation`
- `category`
- `skills`
- availability flags such as `has_city`, `has_occupation`, and `has_skills`

### Raw data

The full raw NAV response is **not committed to the repository**.

`data/raw/` is intentionally ignored because:

- the raw dataset is relatively large
- it can be recollected with `src/collect_nav_jobs.py`
- a new collection represents a new labor-market snapshot and may produce different results

The repository includes the **processed dataset used for the published analysis**, allowing the analytical notebooks to be reproduced with the same snapshot.

---

## Project workflow

```text
NAV Arbeidsplassen
        ↓
src/collect_nav_jobs.py
        ↓
data/raw/all_jobs.json
        ↓
src/clean_jobs.py
        ↓
data/processed/jobs_clean.csv
        ↓
00_data_source_exploration.ipynb
        ↓
01_data_quality_eda.ipynb
        ↓
02_skill_analysis.ipynb
        ↓
03_ai_future_skills.ipynb
```

---

## Notebook structure

### `00_data_source_exploration.ipynb`

Documents the structure of the raw NAV JSON response.

Focus:

- source structure
- `_source` records
- nested properties
- preprocessing handoff

This notebook intentionally avoids duplicating later EDA.

### `01_data_quality_eda.ipynb`

Validates the cleaned dataset before analysis.

Focus:

- dataset structure
- duplicates
- missingness and placeholders
- location quality
- occupation-field quality
- skill extraction
- job–skill long-format transformation

Important finding:

The source occupation field had poor analytical quality, so it was **not used as a primary variable** in later analysis.

### `02_skill_analysis.ipynb`

Builds the current skill-demand baseline.

Focus:

- most demanded skills
- number of skills per job
- long-tail skill distribution
- skill demand by city
- geographic comparison of major job markets

Skill demand is measured using **unique job postings**, not raw row counts.

### `03_ai_future_skills.ipynb`

Analyzes digital and AI-related demand.

Focus:

- exploratory semantic clustering
- ESCO-based digital classification
- exact vs context-aware skill mapping
- core vs expanded digital-skill sets
- digital jobs by skill, title, category, and city
- AI-linked skills
- AI-linked jobs
- complementary skill enrichment
- AI geography

---

## Digital-skill methodology

A simple manually maintained keyword list was deliberately avoided.

Instead, the project uses **ESCO** — the European Skills, Competences, Qualifications and Occupations taxonomy — as an external labor-market reference.

### Classification approach

1. Build a multilingual ESCO skill reference
2. Match NAV skills exactly where possible
3. Enrich unmatched skills with representative job titles and categories
4. Retrieve candidate ESCO concepts with multilingual sentence embeddings
5. Rerank plausible candidates using a CrossEncoder
6. Check whether the selected ESCO concept belongs to the official ESCO digital-skills collection

Two result sets are retained:

### Core digital skills

Unambiguous exact matches to officially digital ESCO concepts.

This is the **high-confidence baseline**.

### Expanded digital skills

Core skills plus validated context-aware semantic mappings.

This broader set is used as a **sensitivity analysis**, not as an equally certain replacement for the core set.

---

## AI-linked methodology

Digital does not automatically mean AI.

AI demand is therefore analyzed separately.

The analysis identifies ESCO concepts whose official:

- preferred labels
- alternative labels
- descriptions
- or definitions

explicitly reference **artificial intelligence**.

Observed NAV skills mapped to those concepts define the AI-linked job sample.

This produced:

- **87 AI-linked jobs**
- **0.87% of the total sample**

The analysis then compares skills appearing in AI-linked jobs with their prevalence across the full dataset.

### Skill enrichment

Two signals are especially useful:

- **AI job frequency** — how many AI-linked jobs contain the skill
- **Lift** — how much more common the skill is in AI-linked jobs than in the overall sample

This helps distinguish generally common skills from capabilities that are especially associated with AI-related work.

---

## Practical interpretation

The findings suggest a layered learning strategy for someone targeting technical work in Norway:

1. **Build broad digital competence**
2. **Develop data-analysis and programming skills**
3. **Add software-development and data-platform capabilities**
4. **Specialize further in AI and machine learning**

The job-posting evidence suggests that AI knowledge is most useful when combined with a broader technical foundation rather than learned in isolation.

---

## Geographic insights

Digital demand differs depending on whether we look at **volume** or **specialization**.

- **Oslo** has the largest absolute number of digital-skill opportunities
- **Kongsberg** has a much stronger digital concentration relative to its local sampled market
- **Trondheim** and **Bergen** also show relatively strong digital intensity
- Stavanger expands substantially under the broader digital definition, reflecting additional engineering and technology terminology

This distinction matters for job seekers:

> A city can have fewer total jobs but a larger share of digitally intensive opportunities.

---

## Repository structure

```text
Norway-future-skills/
│
├── data/
│   ├── external/
│   │   └── esco/
│   ├── processed/
│   │   ├── jobs_clean.csv
│   │   ├── job_skills.csv
│   │   ├── skill_frequency.csv
│   │   ├── skills_jobs_analysis.csv
│   │   ├── core_digital_skills.csv
│   │   ├── expanded_digital_skills.csv
│   │   ├── ai_linked_skills.csv
│   │   ├── ai_linked_jobs.csv
│   │   └── ...
│   └── raw/                # ignored by Git
│
├── notebooks/
│   ├── 00_data_source_exploration.ipynb
│   ├── 00_learning_notes.ipynb
│   ├── 01_data_quality_eda.ipynb
│   ├── 02_skill_analysis.ipynb
│   └── 03_ai_future_skills.ipynb
│
├── src/
│   ├── collect_nav_jobs.py
│   └── clean_jobs.py
│
├── .gitignore
├── requirements.txt
└── README.md
```

---

## Reproducing the analysis

### 1. Clone the repository

```bash
git clone https://github.com/NazaninFarzady/Norway-future-skills.git
cd Norway-future-skills
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows:

```bash
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Reproduce the published analysis

The processed dataset used for the project is already included.

Run the notebooks in this order:

```text
00_data_source_exploration.ipynb
01_data_quality_eda.ipynb
02_skill_analysis.ipynb
03_ai_future_skills.ipynb
```

> The AI/ESCO notebook includes embedding and CrossEncoder models and therefore takes substantially longer to run than the earlier notebooks.

### Optional: collect a new job-market snapshot

```bash
python src/collect_nav_jobs.py
python src/clean_jobs.py
```

This will create a **new dataset**, so results may differ from the findings reported in this README.

---

## Limitations

- The dataset contains **10,000 collected job postings**, not the complete Norwegian labor market.
- The analysis represents a **snapshot of current demand**, not a historical trend.
- The project therefore does not make causal claims that AI has changed the labor market over time.
- The occupation field had poor coverage and malformed values and was excluded from primary analysis.
- Employer-provided job titles and categories are fragmented and not standardized occupational classifications.
- Semantic ESCO mappings contain more uncertainty than exact matches.
- The AI-linked definition is intentionally conservative and does not represent every possible AI-related role or skill.

---

## Tools and technologies

- Python
- pandas
- matplotlib
- scikit-learn
- Sentence Transformers
- CrossEncoder reranking
- ESCO taxonomy
- Jupyter Notebook
- Git / GitHub

---

## Next step

The analytical phase is complete.

The next stage is to build a **Power BI dashboard** that turns the notebook findings into a concise visual story around:

1. Norwegian skill demand
2. digital-skill demand
3. AI-linked demand and complementary skills
4. geographic differences

---

## Author

**Nazanin Farzady**

Portfolio project focused on data analysis, labor-market intelligence, skill demand, and AI-related workforce trends in Norway.
