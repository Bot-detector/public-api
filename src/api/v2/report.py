from fastapi import APIRouter, status
from fastapi.exceptions import HTTPException

from src.app.models.report import Report
from src.app.views.input.report import Detection
from src.app.views.response.ok import Ok
from src.core.kafka.report import report_engine

router = APIRouter(tags=["Report"])


@router.post("/reports", status_code=status.HTTP_201_CREATED, response_model=Ok)
async def post_reports(detection: list[Detection]):
    report = Report(kafka_engine=report_engine)
    data = await report.parse_data(detection)
    if not data:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="invalid data")
    await report.send_to_kafka(data)
    return Ok()
