from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.models import Variable, Connection
from airflow.utils.email import send_email
from datetime import datetime, timedelta
import requests
from airflow.utils.log.logging_mixin import LoggingMixin
import matplotlib.pyplot as plt
from fpdf import FPDF
import os
import tempfile
import pandas as pd
import os
from airflow.utils.log.logging_mixin import LoggingMixin

log = LoggingMixin().log
# --- CONFIGURATION (Externalized) ---
XM_API_URL = Variable.get("xm_api_url", default_var="https://servapibi.xm.com.co/")
METRIC_ID = Variable.get("xm_metric_id", default_var="DemaReal")
ENTITY = Variable.get("xm_entity", default_var="Sistema")
RECIPIENTS = Variable.get("xm_recipients", deserialize_json=True, default_var=["carlosaenz.26@hotmail.com"])


# --- DAG DEFINITION ---
default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2025, 3, 1),  # Updated to today for no catch-up
    "email": RECIPIENTS,
    "email_on_failure": True,  # Notify on failure
    "email_on_retry": False,
    "retries": 3,  # More retries for robustness
    "retry_delay": timedelta(minutes=1),
}

dag = DAG(
    "xm_data_pipeline",
    default_args=default_args,
    description="Fetch XM data, generate plot and Excel, and send via email",
    schedule_interval="0 12 * * 5",  # Every Friday at 12:00 PM UTC
    catchup=False,
)

# Task Functions
def fetch_xm_data(ti, **context):
    """Fetches data from XM API and pushes it to XCom"""
    try:
        start_date = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
        end_date = datetime.now().strftime("%Y-%m-%d")
        payload = {
            "MetricId": METRIC_ID,
            "StartDate": start_date,
            "EndDate": end_date,
            "Entity": ENTITY,
            "Filter": []
        }
        log.info(f"Fetching data from {XM_API_URL}hourly with payload: {payload}")
        response = requests.post(f"{XM_API_URL}hourly", json=payload, timeout=10)
        response.raise_for_status()
        data = response.json()
        log.info(f"Data fetched successfully: {len(data.get('Items', []))} records")
        ti.xcom_push(key="xm_data", value=data)
    except Exception as e:
        log.error(f"Error fetching data: {str(e)}")
        raise

####################################################
def process_data(ti, **context):
    """Processes fetched XM data, generates a plot, writes to Excel, and pushes file paths to XCom."""
    try:
        # Step 1: Pull data from XCom
        log.info("Pulling data from XCom for task 'fetch_xm_data'")
        data = ti.xcom_pull(key="xm_data", task_ids="fetch_xm_data")
        if not data:
            log.error("No data received from fetch_xm_data")
            raise ValueError("No data received from fetch_xm_data task")
        log.info(f"Successfully pulled data: {len(data.get('Items', []))} items")

        # Step 2: Organize the data
        try:
            log.info("Organizing XM data")
            items = data.get("Items", [])
            if not items:
                log.error("No 'Items' found in data")
                raise ValueError("No 'Items' in XM data")

            timestamps = [entry["Date"] for entry in items]
            hourly_data = []
            for entry in items:
                sistema = next((e for e in entry["HourlyEntities"] if e["Id"] == "Sistema"), None)
                if not sistema:
                    log.warning(f"No 'Sistema' data for date {entry['Date']}")
                    continue
                values = sistema["Values"]
                hourly_values = {f"Hour{str(i).zfill(2)}": float(values.get(f"Hour{str(i).zfill(2)}", 0)) for i in range(1, 25)}
                hourly_data.append({"Date": entry["Date"], **hourly_values})
            daily_avg_values = [sum([v for k, v in day.items() if k != "Date"]) / 24 for day in hourly_data]
            log.info(f"Organized data for {len(hourly_data)} days")
        except Exception as e:
            log.error(f"Failed to organize data: {str(e)}")
            raise

        # Step 3: Generate the plot
        try:
            log.info("Generating plot")
            with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_fig:
                plt.figure(figsize=(10, 5))
                plt.plot(timestamps, daily_avg_values, marker="o", linestyle="-")
                plt.xlabel("Date")
                plt.ylabel("Average Daily Value")
                plt.title(f"XM Data Report: {data['Metric']['Id']}")
                plt.grid()
                plt.savefig(temp_fig.name)
                plt.close()
                plot_file = temp_fig.name
            log.info(f"Plot saved to {plot_file}")
        except Exception as e:
            log.error(f"Failed to generate plot: {str(e)}")
            raise

        # Step 4: Write data to Excel
        try:
            log.info("Writing data to Excel")
            with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as temp_excel:
                df = pd.DataFrame(hourly_data)
                df.to_excel(temp_excel.name, index=False)
                excel_file = temp_excel.name
            log.info(f"Excel file written to {excel_file}")
        except Exception as e:
            log.error(f"Failed to write Excel file: {str(e)}")
            raise

        # Step 5: Push file paths to XCom
        try:
            log.info("Pushing file paths to XCom")
            ti.xcom_push(key="plot_file", value=plot_file)
            ti.xcom_push(key="excel_file", value=excel_file)
            log.info(f"Pushed plot_file={plot_file} and excel_file={excel_file} to XCom")
        except Exception as e:
            log.error(f"Failed to push to XCom: {str(e)}")
            raise
    except Exception as e:
        log.error(f"Process_data failed: {str(e)}")
        raise
######################################################################
from airflow.utils.email import send_email  # Ensure this import is present

def send_email_task(ti, **context):
    """Sends the generated plot and Excel file via email using smtp_default connection."""
    plot_file = None
    excel_file = None
    try:
        log.info("Pulling file paths from XCom")
        plot_file = ti.xcom_pull(key="plot_file", task_ids="process_data")
        excel_file = ti.xcom_pull(key="excel_file", task_ids="process_data")
        if not plot_file or not excel_file:
            log.error(f"Missing files: plot_file={plot_file}, excel_file={excel_file}")
            raise ValueError("Missing file paths from process_data")
        log.info(f"Pulled plot_file={plot_file}, excel_file={excel_file}")

        if not os.path.exists(plot_file) or not os.path.exists(excel_file):
            log.error(f"Files not found: plot_file={plot_file}, excel_file={excel_file}")
            raise FileNotFoundError("One or both files missing on disk")

        log.info("Sending email")
        subject = f"XM Weekly Report: {ti.dag_id}"
        body = "Attached are the weekly XM report plot and data Excel file."
        send_email(  # This now calls airflow.utils.email.send_email
            to=ti.dag_run.conf.get("email_to", "info@zrenew.com"),
            subject=subject,
            html_content=body,
            files=[plot_file, excel_file],
            conn_id="smtp_default"
        )
        log.info("Email sent successfully")

        # Clean up files only on success
        for f in [plot_file, excel_file]:
            if os.path.exists(f):
                try:
                    os.remove(f)
                    log.info(f"Cleaned up file: {f}")
                except Exception as e:
                    log.warning(f"Failed to clean up {f}: {str(e)}")
    except Exception as e:
        log.error(f"Failed to send email: {str(e)}", exc_info=True)
        raise


#################################################################################
# Task Definitions
fetch_task = PythonOperator(
    task_id="fetch_xm_data",
    python_callable=fetch_xm_data,
    provide_context=True,
    dag=dag,
)

process_task = PythonOperator(
    task_id="process_data",
    python_callable=process_data,
    provide_context=True,
    dag=dag,
)

email_task = PythonOperator(
    task_id="send_email",
    python_callable=send_email_task,
    provide_context=True,
    dag=dag,
)

# Task Dependencies
fetch_task >> process_task >> email_task