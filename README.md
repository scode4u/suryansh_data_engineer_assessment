# Data Engineering Assessment

Welcome!  
This exercise evaluates your core **data-engineering** skills:

| Competency | Focus                                                         |
| ---------- | ------------------------------------------------------------- |
| SQL        | relational modelling, normalisation, DDL/DML scripting        |
| Python ETL | data ingestion, cleaning, transformation, & loading (ELT/ETL) |

---

## 0 Prerequisites & Setup

> **Allowed technologies**

- **Python ≥ 3.8** – all ETL / data-processing code
- **MySQL 8** – the target relational database
- **Pydantic** – For data validation
- List every dependency in **`requirements.txt`** and justify selection of libraries in the submission notes.

---

## 1 Clone the skeleton repo

```
git clone https://github.com/100x-Home-LLC/data_engineer_assessment.git
```

✏️ Note: Rename the repo after cloning and add your full name.

**Start the MySQL database in Docker:**

```
docker-compose -f docker-compose.initial.yml up --build -d
```

- Database is available on `localhost:3306`
- Credentials/configuration are in the Docker Compose file
- **Do not change** database name or credentials

For MySQL Docker image reference:
[MySQL Docker Hub](https://hub.docker.com/_/mysql)

---

### Problem

- You are provided with a raw JSON file containing property records is located in data/
- Each row relates to a property. Each row mixes many unrelated attributes (property details, HOA data, rehab estimates, valuations, etc.).
- There are multiple Columns related to this property.
- The database is not normalized and lacks relational structure.
- Use the supplied Field Config.xlsx (in data/) to understand business semantics.

### Task

- **Normalize the data:**

  - Develop a Python ETL script to read, clean, transform, and load data into your normalized MySQL tables.
  - Refer the field config document for the relation of business logic
  - Use primary keys and foreign keys to properly capture relationships

- **Deliverable:**
  - Write necessary python and sql scripts
  - Place your scripts in `src/`
  - The scripts should take the initial json to your final, normalized schema when executed
  - Clearly document how to run your script, dependencies, and how it integrates with your database.

---

## Submission Guidelines

- Edit the section to the bottom of this README with your solutions and instructions for each section at the bottom.
- Ensure all steps are fully **reproducible** using your documentation
- DO NOT MAKE THE REPOSITORY PUBLIC. ANY CANDIDATE WHO DOES IT WILL BE AUTO REJECTED.
- Create a new private repo and invite the reviewer https://github.com/mantreshjain and https://github.com/siddhuorama

---

**Good luck! We look forward to your submission.**


## Solutions and Instructions (Filed by Suryansh Singh)
1. Overview
This project delivers a complete ETL pipeline for normalizing the raw property dataset provided in the assessment.
The pipeline:
Reads the raw JSON file
Validates and cleans each record using Pydantic
Breaks down nested lists (Valuation, HOA, Rehab) into separate relational tables
Loads everything into a fully normalized MySQL database
The final schema is designed to support clean analytics, reporting, and future data growth.

2. Project Structure
data_engineer_assessment-main/
│
├── data/
│   └── fake_property_data_new.json
│
├── src/
│   ├── etl.py              # Main ETL logic
│   ├── models.py           # Pydantic models for validation and structure
│   ├── utils.py            # DB connection + schema initialization
│   └── sql/
│       └── schema.sql      # Normalized MySQL schema
│
├── docker-compose.initial.yml
├── docker-compose.final.yml
└── README.md

3. How to Run the Pipeline
Step A — Start MySQL (Docker)

Make sure Docker Desktop is running, then run:
docker compose -f docker-compose.initial.yml up -d

Step B — Create and activate a virtual environment
python -m venv venv
venv\Scripts\activate

Step C — Install dependencies
pip install -r requirements.txt

Step D — Run the ETL
cd src
python etl.py


4. Normalization Approach
Each property record includes nested lists for:
Valuation
HOA
Rehab

Instead of flattening, these lists are broken into 1-to-many tables, linked through a generated property_id.

This ensures:
No duplicated property data
Clean JOINs
Proper historical tracking
Accurate analytics

5. Database Schema Overview
properties – Main table
valuation – Multiple rows per property
hoa – HOA snapshots per property
rehab – Rehab estimates per property

6. Key Assumptions
Every record in the dataset includes Valuation, HOA, and Rehab arrays
SQFT_Total is consistently formatted as "xxxx sqft" eg. 8012 sqft
Missing numeric values are treated as NULL
No unique ID existed in the source → a clean incremental property_id is generated

7. Reproducibility
python etl.py


**Document your solution here:**

This project delivers a complete ETL pipeline that processes the raw property JSON provided in the assessment.
The dataset contains nested lists such as Valuation, HOA, and Rehab, so I standardized the structure and normalized all records into separate relational MySQL tables.

On each run, the pipeline:
Loads and validates the JSON data
Cleans fields like "5649 sqft" into numeric values
Generates a property_id for each record
Breaks nested lists into proper 1-to-many tables
Rebuilds the database schema
Loads all normalized tables into MySQL
The entire ETL is reproducible and runs end-to-end with a single command.

