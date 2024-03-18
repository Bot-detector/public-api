from fastapi import APIRouter, status
from fastapi.exceptions import HTTPException

from src.app.repositories.report import Report
from src.app.views.input.report import Detection
from src.app.views.response.ok import Ok

router = APIRouter(tags=["Report"])


@router.post("/report", status_code=status.HTTP_201_CREATED, response_model=Ok)
async def post_reports(detection: list[Detection]):
    report = Report()
    data = await report.parse_data(detection)
    if not data:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="invalid data")
    await report.send_to_kafka(data)
    return Ok()
