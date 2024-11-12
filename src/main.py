from fastapi import FastAPI, Depends, Query
from fastapi import UploadFile, File

from src.core.celery_worker import extract_text_from_image_task
from src.core.database import get_db
from src.schemas.document_schema import (
    DocumentResponse,
    DocumentDelete,
    DocumentAnalyse,
    DocumentTextResponse,
)
from src.services.document_service import (
    delete_document,
    get_text_document,
    create_document_from_file,
)
from src.utils.decorators import exception_handler

from sqlalchemy.ext.asyncio import AsyncSession

app = FastAPI(
    title="Document Processing API",
    description="API для загрузки, удаления и анализа документов",
    version="1.0.0",
)


@app.post(
    "/upload_doc",
    response_model=DocumentResponse,
    summary="Загрузить документ",
    tags=["Документы"],
)
@exception_handler
async def upload_document_endpoint(
    file: UploadFile = File(...),
    document_name: str = "",
    session: AsyncSession = Depends(get_db),
) -> DocumentResponse:
    if not document_name:
        document_name = file.filename
    document_id = await create_document_from_file(file, session, document_name)
    return DocumentResponse(
        id=document_id,
        name=document_name,
        status="success",
        message="Документ успешно загружен",
    )


@exception_handler
@app.delete(
    "/delete_doc",
    response_model=DocumentDelete,
    summary="Удалить документ",
    tags=["Документы"],
)
async def delete_document_endpoint(
    document_id: int = Query(..., description="Идентификатор документа для удаления"),
    session: AsyncSession = Depends(get_db),
) -> DocumentDelete:
    await delete_document(document_id, session)
    return DocumentDelete(
        id=document_id, status="success", message="Документ успешно удален"
    )


@app.post(
    "/doc_analyse",
    response_model=DocumentAnalyse,
    summary="Проанализировать документ",
    tags=["Документы"],
)
async def analyze_doc(document_id: int):
    extract_text_from_image_task.delay(document_id)

    return DocumentAnalyse(
        id=document_id,
        status="success",
        message="Документ успешно отправлен на анализ",
    )


@app.get(
    "/get_text/{document_id}",
    response_model=DocumentTextResponse,
    summary="Получение текста документа",
    tags=["Документы"],
)
@exception_handler
async def get_document_text(
    document_id: int, db: AsyncSession = Depends(get_db)
) -> DocumentTextResponse:
    document_name, document_text = await get_text_document(document_id, db)

    return DocumentTextResponse(
        id=document_id,
        document_id=document_id,
        name=document_name,
        text=document_text,
        status="success",
        message="Текст документа успешно получен",
    )
