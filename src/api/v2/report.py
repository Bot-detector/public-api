from fastapi import APIRouter, status, Request
from fastapi.exceptions import HTTPException
from src.app.views.input.report import Detection
from src.app.views.response.ok import Ok
from src.core.fastapi.dependencies.kafka_engine import AioKafkaEngine
from src.app.models.report import Report

router = APIRouter(tags=["Report"])


@router.post("/reports", status_code=status.HTTP_201_CREATED, response_model=Ok)
async def post_reports(request:Request, detection: list[Detection]):
    kafka_reports:AioKafkaEngine = request.app.state.kafka_reports
    report = Report(kafka_engine=kafka_reports)
    data = await report.parse_data(detection)
    if not data:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="invalid data")
    await report.send_to_kafka(data)
    return Ok()
