import os
from datetime import datetime
from pathlib import Path

from celery import Celery

from app.celery_worker.utils import data_parser, write_xlsx_file

CELERY_BROKER_URL = os.environ.get("CELERY_BROKER_URL")
CELERY_RESULT_BACKEND = os.environ.get("CELERY_RESULT_BACKEND")

celery_app = Celery(
    "tasks",
    broker=CELERY_BROKER_URL,
    backend=CELERY_RESULT_BACKEND,
)


@celery_app.task
def data_report_task(data: list) -> dict:
    file_name = f"{datetime.now().strftime('%d-%m-%Y-%H-%M')}.xlsx"
    path = Path("data_reports", file_name)
    parsed_data = data_parser(data=data)
    write_xlsx_file(data=parsed_data, file_path=path)
    return {"path": str(path), "file_name": file_name}
