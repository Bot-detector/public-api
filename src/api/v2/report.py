from fastapi import APIRouter

router = APIRouter(tags=["Report"])

@router.post("/reports")
async def post_reports():
    pass