from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import requests
import logging
import smtplib
from email.message import EmailMessage

import matplotlib.pyplot as plt
from fpdf import FPDF

# --- CONFIGURATION ---
XM_API_URL = "https://servapibi.xm.com.co/"
METRIC_ID = "DemaReal"
START_DATE = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
END_DATE = datetime.now().strftime("%Y-%m-%d")
ENTITY = "Sistema"
RECIPIENTS = ["your_email@example.com"]
EMAIL_SENDER = "your_smtp_email@example.com"
EMAIL_PASSWORD = "your_smtp_password"

# --- DAG DEFINITION ---
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2025, 2, 27),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'xm_data_pipeline',
    default_args=default_args,
    description='Fetch data from XM API, generate a PDF, and send email',
    schedule_interval="0 12 * * 5",  # Runs every Friday at 12:00 PM UTC
    catchup=False,
)

def fetch_xm_data():
    """Fetches data from XM API"""
    try:
        payload = {
            "MetricId": METRIC_ID,
            "StartDate": START_DATE,
            "EndDate": END_DATE,
            "Entity": ENTITY,
            "Filter": []
        }
        response = requests.post(f"{XM_API_URL}hourly", json=payload)
        response.raise_for_status()
        data = response.json()
        logging.info(f"Data fetched: {data}")
        return data
    except Exception as e:
        logging.error(f"Error fetching data: {str(e)}")
        raise

def process_data():
    """Processes the data and generates a PDF report"""


    # Sample Data Processing (Replace with actual processing)
    timestamps = ["2025-02-21", "2025-02-22", "2025-02-23", "2025-02-24"]
    values = [100, 150, 120, 130]

    # Create Graph
    plt.figure(figsize=(10, 5))
    plt.plot(timestamps, values, marker="o", linestyle="-")
    plt.xlabel("Date")
    plt.ylabel("Value")
    plt.title(f"XM Data Report: {METRIC_ID}")
    plt.grid()
    plt.savefig("/tmp/report.pdf")

    logging.info("PDF report generated.")

def send_email():
    """Sends the generated PDF report via email"""
    msg = EmailMessage()
    msg["Subject"] = f"XM Weekly Report: {METRIC_ID}"
    msg["From"] = EMAIL_SENDER
    msg["To"] = RECIPIENTS
    msg.set_content("Find attached the weekly XM report.")

    with open("/tmp/report.pdf", "rb") as f:
        msg.add_attachment(f.read(), maintype="application", subtype="pdf", filename="report.pdf")

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(EMAIL_SENDER, EMAIL_PASSWORD)
            smtp.send_message(msg)
        logging.info("Email sent successfully!")
    except Exception as e:
        logging.error(f"Failed to send email: {str(e)}")
        raise

fetch_task = PythonOperator(
    task_id="fetch_xm_data",
    python_callable=fetch_xm_data,
    dag=dag,
)

process_task = PythonOperator(
    task_id="process_data",
    python_callable=process_data,
    dag=dag,
)

email_task = PythonOperator(
    task_id="send_email",
    python_callable=send_email,
    dag=dag,
)

fetch_task >> process_task >> email_task
