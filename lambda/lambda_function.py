
import os
import json
import csv
import io
import boto3
import pymysql

s3 = boto3.client("s3")
BUCKET_NAME = "vaibhav-olist-data-pipeline-261016"

TABLES = {
    "customers": {
        "file": "olist_customers_dataset.csv",
        "table": "olist_customers",
        "columns": """
            customer_id VARCHAR(50) PRIMARY KEY,
            customer_unique_id VARCHAR(50),
            customer_zip_code_prefix INT,
            customer_city VARCHAR(100),
            customer_state CHAR(2)
        """,
        "fields": [
            "customer_id", "customer_unique_id",
            "customer_zip_code_prefix", "customer_city",
            "customer_state"
        ],
        "int_fields": ["customer_zip_code_prefix"]
    },
    "orders": {
        "file": "olist_orders_dataset.csv",
        "table": "olist_orders",
        "columns": """
            order_id VARCHAR(50) PRIMARY KEY,
            customer_id VARCHAR(50),
            order_status VARCHAR(30),
            order_purchase_timestamp VARCHAR(30),
            order_approved_at VARCHAR(30),
            order_delivered_carrier_date VARCHAR(30),
            order_delivered_customer_date VARCHAR(30),
            order_estimated_delivery_date VARCHAR(30)
        """,
        "fields": [
            "order_id", "customer_id", "order_status",
            "order_purchase_timestamp", "order_approved_at",
            "order_delivered_carrier_date",
            "order_delivered_customer_date",
            "order_estimated_delivery_date"
        ],
        "int_fields": []
    },
    "order_items": {
        "file": "olist_order_items_dataset.csv",
        "table": "olist_order_items",
        "columns": """
            order_id VARCHAR(50) NOT NULL,
            order_item_id INT NOT NULL,
            product_id VARCHAR(50),
            seller_id VARCHAR(50),
            shipping_limit_date VARCHAR(30),
            price DECIMAL(12,2),
            freight_value DECIMAL(12,2),
            PRIMARY KEY (order_id, order_item_id)
        """,
        "fields": [
            "order_id", "order_item_id", "product_id",
            "seller_id", "shipping_limit_date", "price",
            "freight_value"
        ],
        "int_fields": ["order_item_id"]
    },
    "order_payments": {
        "file": "olist_order_payments_dataset.csv",
        "table": "olist_order_payments",
        "columns": """
            order_id VARCHAR(50) NOT NULL,
            payment_sequential INT NOT NULL,
            payment_type VARCHAR(30),
            payment_installments INT,
            payment_value DECIMAL(12,2),
            PRIMARY KEY (order_id, payment_sequential)
        """,
        "fields": [
            "order_id", "payment_sequential", "payment_type",
            "payment_installments", "payment_value"
        ],
        "int_fields": ["payment_sequential", "payment_installments"]
    },
    "products": {
        "file": "olist_products_dataset.csv",
        "table": "olist_products",
        "columns": """
            product_id VARCHAR(50) PRIMARY KEY,
            product_category_name VARCHAR(100),
            product_name_lenght INT,
            product_description_lenght INT,
            product_photos_qty INT,
            product_weight_g INT,
            product_length_cm INT,
            product_height_cm INT,
            product_width_cm INT
        """,
        "fields": [
            "product_id", "product_category_name",
            "product_name_lenght", "product_description_lenght",
            "product_photos_qty", "product_weight_g",
            "product_length_cm", "product_height_cm",
            "product_width_cm"
        ],
        "int_fields": [
            "product_name_lenght", "product_description_lenght",
            "product_photos_qty", "product_weight_g",
            "product_length_cm", "product_height_cm",
            "product_width_cm"
        ]
    }
}


def lambda_handler(event, context):
    connection = None

    try:
        event = event or {}
        dataset = event.get("dataset", "customers").lower()

        if dataset not in TABLES:
            raise ValueError(
                "dataset must be customers, orders, order_items, "
                "order_payments, or products"
            )

        config = TABLES[dataset]
        file_key = event.get(
            "file_key", "kaggle/raw/" + config["file"]
        )

        response = s3.get_object(Bucket=BUCKET_NAME, Key=file_key)
        csv_content = response["Body"].read().decode("utf-8-sig")
        reader = csv.DictReader(io.StringIO(csv_content))

        connection = pymysql.connect(
            host=os.environ["DB_HOST"],
            user=os.environ["DB_USER"],
            password=os.environ["DB_PASSWORD"],
            port=int(os.environ.get("DB_PORT", "3306")),
            database="olistdb",
            connect_timeout=10,
            read_timeout=120,
            write_timeout=120,
            cursorclass=pymysql.cursors.DictCursor
        )

        table = config["table"]
        fields = config["fields"]
        int_fields = config["int_fields"]
        total = 0
        batch = []

        with connection.cursor() as cursor:
            cursor.execute(
                f"CREATE TABLE IF NOT EXISTS {table} "
                f"({config['columns']})"
            )

            placeholders = ", ".join(["%s"] * len(fields))
            column_names = ", ".join(fields)
            primary_key = (
                ["customer_id"] if dataset == "customers" else
                ["order_id"] if dataset == "orders" else
                ["order_id", "order_item_id"] if dataset == "order_items" else
                ["order_id", "payment_sequential"] if dataset == "order_payments" else
                ["product_id"]
            )
            updates = ", ".join(
                f"{field}=VALUES({field})"
                for field in fields if field not in primary_key
            )

            insert_sql = (
                f"INSERT INTO {table} ({column_names}) "
                f"VALUES ({placeholders}) "
                f"ON DUPLICATE KEY UPDATE {updates}"
            )

            for row in reader:
                values = []
                for field in fields:
                    value = row.get(field, "")
                    if value == "":
                        value = None
                    if field in int_fields:
                        value = int(value) if value is not None else None
                    values.append(value)

                batch.append(tuple(values))

                if len(batch) >= 500:
                    cursor.executemany(insert_sql, batch)
                    total += len(batch)
                    batch = []

            if batch:
                cursor.executemany(insert_sql, batch)
                total += len(batch)

            cursor.execute(f"SELECT COUNT(*) AS total FROM {table}")
            db_count = cursor.fetchone()["total"]

        connection.commit()

        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": f"{dataset} CSV loaded successfully",
                "rows_processed": total,
                "database_rows": db_count,
                "table": table,
                "file_key": file_key
            })
        }

    except Exception as e:
        print("Pipeline error:", str(e))
        if connection:
            connection.rollback()
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }

    finally:
        if connection:
            connection.close()
