# IT Jobs Market Analytics Pipeline

This project is an end-to-end data engineering and analytics pipeline designed to
scraped job listings from **dev.bg**, transform them using **dbt**, store them
in **DuckDB**, and analyse them with **Polars / DuckDB SQL**.
The goal in to explore trends in the Bulgaria IT job market (skills, salaries,
companies, etc.)

## Project Overview

The project consists of 4 main components

### 1. Scraper (Scrapy + Playwright)

- Extract job listings from dev.bg across all categories

- Capture detailed fields such as job title, company, tech stack, salary,
location, job description, company profile info and posted dates.

- Saves results to a DuckDB database via a pileline

### 2. Data Warehouse (DuckDB)

- Central analytical database stored locally as a `.duckdb` file

- Stores raw scraped data and dbt-transformed fact/dimension tables

### 3. Transformations (dbt-duckdb)

- Cleans, standardizes and models the data using a star schema:
  - `fact_listing`
  - `dim_company`
  - `dim_location`
  - `dim_date`
  - `dim_category`
  - `bridge_listing_skill`
  - `bridge_listing_category`

- Includes tests for uniqueness, not-null constraints ...

### 4. Analytics (Polars + Python)

- Jupyter/Polars notebook

## Scraping Layer (Scrapy)

### Features

- Discovers all job categories from the dev.bg homepage

- Crawls listings with pagination

- Collects company-level metadata by navigating the company profile pages

- Ensures all scraped fields have a default value to avoid pipeline failures

### Key extracted fields

- `company_name`

- `job_title`

- `location`

- `salary` (min/max extraction performed in dbt)

- `tech_stack` (list)

- `category` (list)

- `listing_url`

- `date_posted`

- `date_scraped`

- `description`

- Company metadata:
  - `activity`, `sector`, `central_office`
  - `creation_date`, `number_employees`, `offices_in_bulgaria`, etc.

Output is passed to a DuckDB pipeline

## Storage layer (DuckDB)

The scraper writes directly to:

```text
/jobs_scraping/jobs.duckdb
```

DuckDB is chosen because of:

- High analytical performance

- Zero-dependency local database

- Strong Arrow/Polars interoperability

- Native parquet support

## dbt Transformations

The dbt project transforms raw scraped data into an analytics-ready star schema.

### Models include

#### Staging layer

- `staging_jobs`
  - Normalises fields
  - Splits salary into min/max
  - Cleans locations
  - Ensures data types

#### Dimensions Tables

- `dim_company`
- `dim_location`
- `dim_date` (generated using dbt Jinja loops)
- `dim_category`

#### Bridge Tables

- `bridge_listing_skill`
  - Converts tech-stack lists into one row per (listing_id, tech_id)
- `bridge_listing_category`
  - Converts category lists into one row per (listing_id, category_id)

#### Fact Table

- `fact_listing`
  - Links listings to company, location, posting date and scraped date

#### dbt Tests Used

- `unique`
- `not_null`
