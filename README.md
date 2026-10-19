# AWS Olist ETL Data Pipeline

An end-to-end AWS data engineering project that loads Olist e-commerce CSV datasets from Amazon S3 into Amazon RDS for MySQL using Python AWS Lambda and AWS Step Functions, followed by SQL validation in DBeaver.

## Project Overview

This project demonstrates an ETL (Extract, Transform, Load) pipeline using AWS services.

### Key objectives
- Store raw CSV files in Amazon S3.
- Process datasets using Python AWS Lambda.
- Orchestrate five dataset loads with AWS Step Functions.
- Load records into Amazon RDS for MySQL.
- Validate database tables using SQL queries in DBeaver.
- Track execution success and failure.

## Architecture Diagram

![AWS Olist Data Pipeline Architecture](/architecture/vaibhav-olist-data-pipeline-architecture.png)

Editable diagram source:
 ![`architecture/architecture.drawio`](/image/Screenshot%20(1048).png)

### Data Flow

```text
Kaggle Olist CSV Files
          |
          v
Amazon S3 — kaggle/raw/
          |
          v
AWS Step Functions
          |
          +--> Lambda: Customers
          +--> Lambda: Orders
          +--> Lambda: Order Items
          +--> Lambda: Order Payments
          +--> Lambda: Products
                    |
                    v
             Amazon RDS MySQL
                    |
                    v
              DBeaver SQL Checks
```

## AWS Services Used

| Service | Purpose |
|---|---|
| Amazon S3 | Stores raw CSV files |
| AWS Lambda | Processes and loads CSV data using Python |
| AWS Step Functions | Orchestrates the dataset loading workflow |
| Amazon RDS for MySQL | Stores processed data in database tables |
| DBeaver | Runs SQL queries and validates results |

## Technologies

- Python
- SQL
- MySQL
- AWS S3
- AWS Lambda
- AWS Step Functions
- Amazon RDS
- DBeaver
- Git and GitHub

## Datasets and Verified Results

The following row counts were verified during the project run.

| Dataset | Database Table | Rows |
|---|---|---:|
| Customers | `olist_customers` | 99,441 |
| Orders | `olist_orders` | 99,441 |
| Order Items | `olist_order_items` | 112,650 |
| Order Payments | `olist_order_payments` | 103,886 |
| Products | `olist_products` | 32,951 |
| **Total** | **5 tables** | **448,369** |

These counts represent the verified run and should be checked again if the database is reloaded or changed.

## Repository Structure

```text
aws-olist-etl-pipeline/
├── architecture/
│   ├── architecture.png
│   └── architecture.drawio
├── lambda/
│   ├── lambda_function.py
│   └── requirements.txt
├── step-functions/
│   └── state-machine.asl.json
├── sql/
│   ├── verify_row_counts.sql
│   └── data_quality_checks.sql
├── screenshots/
│   ├── 01-s3-raw-csvs.png
│   ├── 02-lambda-customers-success.png
│   ├── 03-lambda-other-datasets.png
│   ├── 04-step-functions-success.png
│   ├── 05-rds-database.png
│   └── 06-dbeaver-row-counts.png
├── .gitignore
└── README.md
```

## Workflow

1. Download the public Olist dataset from Kaggle.
2. Upload the required raw CSV files to Amazon S3 under `kaggle/raw/`.
3. Configure Lambda with the required database connection and S3 access.
4. Test the Lambda function for each dataset.
5. Execute the Step Functions state machine.
6. Confirm successful execution and review error handling.
7. Run SQL row-count and data-quality checks in DBeaver.

## Dataset Source

The data is from the public Brazilian E-Commerce dataset by Olist:

https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce

Download the data from the original source. Avoid committing the full raw dataset to this repository.

## Screenshots

Add real screenshots from your own AWS Console and DBeaver session to the `screenshots/` folder.

| Screenshot | What it demonstrates |
|---|---|
| `01-s3-raw-csvs.png` | Raw CSV files stored in S3 |
| `02-lambda-customers-success.png` | Successful Lambda test |
| `03-lambda-other-datasets.png` | Other dataset processing results |
| `04-step-functions-success.png` | Successful Step Functions execution |
| `05-rds-database.png` | RDS database configuration |
| `06-dbeaver-row-counts.png` | SQL row-count verification |

Use genuine screenshots and crop or blur sensitive details before committing them.

## SQL Validation

The `sql/verify_row_counts.sql` script checks destination table counts.

The `sql/data_quality_checks.sql` script can be used to check:
- Missing identifiers
- Duplicate identifiers
- Invalid negative values
- Missing values in important columns

Run these checks in DBeaver after the pipeline completes.

## Security Best Practices

- Keep the S3 bucket private.
- Follow least-privilege IAM permissions.
- Restrict database access to approved security groups and access paths.
- Keep database passwords and access keys out of source code.
- Never commit `.pem`, `.key`, `.env`, credentials, or secret values.
- Remove sensitive account and connection information from screenshots.

## Important Note

This repository documents the project and its verified results. AWS resources must be configured in your own account. Review the repository code against the working Lambda function and Step Functions workflow before deploying any changes.

## Author

AWS Data Engineering Project — Python, SQL, Amazon S3, AWS Lambda, Step Functions, RDS MySQL, and DBeaver.

## Connect With Me

I'm interested in AWS Cloud, DevOps, and Data Engineering opportunities.

- **LinkedIn:** [Vaibhav Bhuse](https://www.linkedin.com/in/vaibhav-bhuse-530132288/)
- **GitHub:** [vaibhavbhuse42](https://github.com/vaibhavbhuse42)

Feel free to connect, share feedback, or discuss cloud and data engineering projects.