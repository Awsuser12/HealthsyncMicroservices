import psycopg2
from flask import Flask, jsonify
from datetime import datetime

app = Flask(__name__)

# Redshift configuration
REDSHIFT_CONFIG = {
    "dbname": "dev",  # Redshift username
    "user": "awsuser",
    "password": "Admin$100",  # Redshift password
    "host": "redshift-cluster-1.cmst8p4oj0qe.us-east-1.redshift.amazonaws.com:5439/dev",  # Replace with actual cluster endpoint
    "port": "5439",  # Default Redshift port
}

def connect_to_redshift():
    """Establish a connection to Redshift."""
    try:
        connection = psycopg2.connect(
            dbname=REDSHIFT_CONFIG["dbname"],
            user=REDSHIFT_CONFIG["user"],
            password=REDSHIFT_CONFIG["password"],
            host=REDSHIFT_CONFIG["host"],
            port=REDSHIFT_CONFIG["port"]
        )
        return connection
    except Exception as e:
        print(f"Error connecting to Redshift: {e}")
        return None

@app.route('/aggregate', methods=['GET'])
def aggregate_data():
    """Aggregate data and store it in Redshift."""
    try:
        # Example metrics
        data = {
            "doctor_id": 123,
            "appointments_count": 15,
            "common_condition": "Hypertension",
            "aggregated_date": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

        connection = connect_to_redshift()
        if not connection:
            return jsonify({"error": "Failed to connect to Redshift"}), 500

        with connection:
            with connection.cursor() as cursor:
                # Create table if not exists
                cursor.execute("""
                CREATE TABLE IF NOT EXISTS aggregated_metrics (
                    doctor_id INT,
                    appointments_count INT,
                    common_condition VARCHAR(255),
                    aggregated_date TIMESTAMP
                );
                """)

                # Insert aggregated data
                cursor.execute("""
                INSERT INTO aggregated_metrics (doctor_id, appointments_count, common_condition, aggregated_date)
                VALUES (%s, %s, %s, %s);
                """, (data["doctor_id"], data["appointments_count"], data["common_condition"], data["aggregated_date"]))

        return jsonify({"message": "Aggregated data stored in Redshift"}), 200
    except psycopg2.Error as db_error:
        print(f"Database error during aggregation: {db_error}")
        return jsonify({"error": "Database error occurred"}), 500
    except Exception as e:
        print(f"Unexpected error during aggregation: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        if 'connection' in locals() and connection:
            connection.close()

if __name__ == "__main__":
    import logging
    logging.basicConfig(level=logging.INFO)
    app.run(host='0.0.0.0', port=5003)
