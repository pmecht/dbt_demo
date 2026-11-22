# dbt Demo

A local data analytics demo that generates synthetic sales data, loads it into DuckDB, and transforms it with dbt. The project demonstrates staging models, mart models, data tests, a dbt SQL macro, and a Python/Pandas dbt model.

## Stack

- dbt Core 1.12.7
- dbt-duckdb 1.11.1
- DuckDB
- Pandas
- Faker
- Windows Batch scripts

## Project structure

```text
.
├── dbt_project.yml          # dbt project configuration and model schemas
├── profiles.yml             # DuckDB development and production profiles
├── install.bat              # Creates the environment and loads source data
├── rundbt.bat               # Builds and tests dbt models
├── pyproject.toml           # Python dependencies and load command
├── macros/
│   └── calculate_order_total.sql
├── models/
│   ├── schema.yml           # dbt data tests
│   ├── staging/             # Cleaned source models (Silver)
│   └── marts/               # Analytics models (Gold)
└── python/
    ├── loaddb.py            # Generates and loads synthetic source data
    ├── calculate_order_total.py
    └── setup.py
```

## Data flow

```text
python/loaddb.py
        │
        ▼
sales.duckdb
  ├── customers
  ├── orders
  └── order_items
        │
        ▼
dbt staging models (Silver)
  ├── stg_customers
  ├── stg_orders
  └── stg_order_items
        │
        ▼
dbt marts (Gold)
  ├── dim_customers
  ├── fct_orders
  ├── fct_total_orders
  └── fct_total_orders_py
```

## Source data

Running the loader creates a local `sales.duckdb` database containing:

- **customers:** 100 generated customers
- **orders:** 500 orders over the previous 365 days
- **order_items:** 1–5 items per order

The generated values include customer names and email addresses, order statuses, delivery notes, unit prices, and quantities.

## Staging models

Located in `models/staging/`:

- `stg_customers.sql` trims customer names and email addresses.
- `stg_orders.sql` selects all order fields and retains only delivered orders.
- `stg_order_items.sql` exposes order item IDs, orders, prices, and quantities.

Staging models are materialized as views in the `silver` schema.

## Mart models

Located in `models/marts/`:

- `dim_customers.sql` creates a customer dimension.
- `fct_orders.sql` joins delivered orders to customer information.
- `fct_total_orders.sql` calculates order totals using the `calculate_order_total` SQL macro.
- `fct_total_orders_py.py` demonstrates the same aggregation with dbt's Python/Pandas interface.

Mart models are materialized as tables in the `gold` schema.

The order fact models calculate:

- `total_order_amount`
- `total_quantity`
- `total_order_items`

## Setup

### Prerequisites

- Windows
- Python 3
- A terminal

On Windows, the bundled scripts can create the virtual environment, install dependencies, and load the database:

```bat
install.bat
```

This script:

1. Creates `dbt_env/`.
2. Activates the virtual environment.
3. Installs the project in editable mode.
4. Runs the `load` command.
5. Creates or replaces the tables in `sales.duckdb`.

To run the setup manually:

```bat
python -m venv dbt_env
call dbt_env\Scripts\activate.bat
python -m pip install --upgrade pip
pip install -e .
load
```

## Run dbt

From the project root:

```bat
rundbt.bat
```

Or run dbt directly:

```bat
dbt build --profiles-dir .
```

The profile uses `sales.duckdb` as the DuckDB path and the `dev` target by default.

## Reload the source data

The source loader replaces the three source tables each time it runs:

```bat
load
```

## Common dbt commands

Run all models:

```bat
dbt run --profiles-dir .
```

Run all models and tests:

```bat
dbt build --profiles-dir .
```

Run only the staging models:

```bat
dbt run --select staging --profiles-dir .
```

Run only the mart models:

```bat
dbt run --select marts --profiles-dir .
```

Test the project:

```bat
dbt test --profiles-dir .
```

Inspect the generated manifest or documentation:

```bat
dbt docs generate --profiles-dir .
dbt docs serve --profiles-dir .
```

## Tests

`models/schema.yml` defines tests for:

- `stg_customers.customer_id`: unique and not null
- `fct_orders.order_id`: unique and not null
- `fct_orders.customer_id`: not null
