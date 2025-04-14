# Heart Disease ETL Pipeline

This project implements a complete **ETL (Extract–Transform–Load)** pipeline for the **UCI Heart Disease Dataset** using Python and a fully Dockerized setup.

## Project Overview

- **Extract**: Downloads the dataset from `ucimlrepo`.
- **Transform**: Handles missing values, validates types, removes duplicates, and standardizes data for analysis.
- **Load**: Loads the clean data into a PostgreSQL database.

---

## How to Run

### Prerequisites

- Docker
- Docker Compose

### Run the Pipeline

1. Clone the repository:
   ```bash
   git clone https://github.com/farzadam/ibik-etl.git
   cd ibik-etl
   ```

2. Launch everything via Docker Compose:
   ```bash
   docker-compose up --build
   ```

3. The ETL process runs automatically from `main.py`:
   - Dataset is extracted and saved to `data/raw/`
   - Transformed using config in `config/config.yaml`
   - Loaded into PostgreSQL (`etldb`, table `heart_disease`)

---
To verify the healthcheck you can run:
   ```bash
   docker-compose ps
   ```


## Accessing PostgreSQL in Docker

After running the ETL pipeline using Docker Compose, a PostgreSQL container named `etl-postgres` will be running with the following credentials:

- **Host**: `localhost`
- **Port**: `5432`
- **Database**: `etldb`
- **User**: `etluser`
- **Password**: `etlpass`

### Access the PostgreSQL shell

You can access the running database container via:

```bash
docker exec -it etl-postgres psql -U etluser -d etldb
```

Once inside the `psql` shell, you can run SQL queries. For example:

```sql
SELECT * FROM heart_disease LIMIT 5;
```

This will return the first 5 rows of the cleaned and transformed dataset loaded by the ETL pipeline.

---

## Project Structure

```bash
.
├── config/
│   └── config.yaml         # ETL parameters (imputation strategy, db config, etc.)
├── data/                   # Raw and transformed data 
├── etl/
│   ├── extract.py          # Downloads data
│   ├── transform.py        # Cleans, imputes, and processes the data
│   ├── load.py             # Uploads data to PostgreSQL
│   ├── utils.py
│   └── schema.py           # Dataset Schema         
├── main.py                 
├── Dockerfile              # Python image for ETL
├── docker-compose.yml      # Brings up ETL + PostgreSQL together
├── logging_config.py       # Logger configuration
└── config_schema.py        # Config file schema
```

---

## Design Decisions

**Modularized ETL**: Each pipeline step (extract, transform, load) is modular, self-contained, and testable in isolation.

**Config-Driven Imputation**: Missing value handling is configurable via YAML, supporting multiple strategies (e.g., median, most_frequent, knn) on a per-column basis.

**Schema Validation**: Uses `pandera` to enforce data schema and ensure type correctness before loading.

**Robust Logging**: Centralized and structured logging reports progress, validation results, and errors with contextual detail.

**Dockerized Workflow**: The pipeline runs inside Docker for platform independence and reproducibility.

**Health-Checked PostgreSQL**: Docker Compose uses a proper `pg_isready` health check to delay ETL startup until the database is ready.

**Command-Line Config Override**: Pipeline supports --config CLI argument to flexibly swap configuration files.

---

## Clean Code Principles

- Fully documented
- Easily configurable via YAML
- Minimal assumptions or hardcoded values
- Ready for unit testing and extension

---
