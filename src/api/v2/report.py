from fastapi import APIRouter
from src.app.report import Report

router = APIRouter(tags=["Report"])

@router.post("/reports")
async def post_reports():
    pass