from fastapi import APIRouter, HTTPException, UploadFile, File
from app.models.paper import LiteratureReviewRequest, DraftReviewRequest
from app.agents.literature_review_agent import generate_literature_review
from app.agents.draft_review_agent import review_draft
from app.utils.pdf_processor import extract_text_from_pdf_bytes

router = APIRouter(prefix="/api/review", tags=["review"])

@router.post("/literature", response_model=dict)
async def generate_literature_review_endpoint(request: LiteratureReviewRequest):
    try:
        result = await generate_literature_review(request.topic, request.max_papers)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/draft", response_model=dict)
async def review_draft_endpoint(request: DraftReviewRequest):
    try:
        result = await review_draft(request.draft_text, request.title)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/draft/upload", response_model=dict)
async def review_draft_upload(file: UploadFile = File(...)):
    try:
        content = await file.read()
        if file.content_type == "application/pdf":
            text = extract_text_from_pdf_bytes(content)
            if not text:
                raise HTTPException(status_code=400, detail="Could not extract text from PDF")
        else:
            text = content.decode("utf-8", errors="ignore")
        
        result = await review_draft(text, file.filename)
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
