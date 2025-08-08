from dagster import job, op, schedule

@op
def scrape_telegram_data():
    pass  # implement scraping here

@op
def load_raw_to_postgres():
    pass  # implement loading here

@op
def run_dbt_transformations():
    import subprocess
    subprocess.run(["dbt", "run"], check=True)

@op
def run_yolo_enrichment():
    pass  # implement YOLO here

@job
def run_pipeline():
    scrape_telegram_data()
    load_raw_to_postgres()
    run_dbt_transformations()
    run_yolo_enrichment()

@schedule(cron_schedule="0 0 * * *", job=run_pipeline, execution_timezone="UTC")
def daily_pipeline_schedule():
    return {}
