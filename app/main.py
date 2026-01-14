from typing import Any

from fastapi import FastAPI, APIRouter, Depends, Request, status
from fastapi.templating import Jinja2Templates
from sqlmodel.ext.asyncio.session import AsyncSession

from app import deps
from app.config import ROOT


TEMPLATES = Jinja2Templates(directory=str(ROOT / "app/templates"))

app: FastAPI = FastAPI(title="AI Transcript Summarizer", version="1.0.0")
api_router = APIRouter()


@api_router.get("/", status_code=status.HTTP_200_OK)
async def root(request: Request, db: AsyncSession = Depends(deps.get_db)) -> Any:
    return TEMPLATES.TemplateResponse(
        "index.html",
        {
            "request": request,
            "title": "AI Transcript Summarizer",
            "version": app.version,
        },
    )


app.include_router(api_router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app", host="0.0.0.0", port=8005, log_level="debug", reload=True
    )
