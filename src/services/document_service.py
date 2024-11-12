import shutil


from datetime import datetime, timezone
from sqlalchemy.orm import joinedload
from src.models.document import Document, DocumentsText
from src.utils.exceptions import (
    FileTooLargeError,
    DocumentNotFoundError,
    DocumentAlreadyExistsError,
    DocumentNotSavedError,
)
from sqlalchemy import delete

from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
import os
from sqlalchemy import select


MAX_FILE_SIZE = 5 * 1024 * 1024

DOCUMENTS_DIR = "./documents"
os.makedirs(DOCUMENTS_DIR, exist_ok=True)


async def create_document_from_file(
    file: UploadFile, session: AsyncSession, document_name: str = None
):
    if file.size > MAX_FILE_SIZE:
        raise FileTooLargeError()

    if not os.path.splitext(document_name)[1]:
        extension = os.path.splitext(file.filename)[-1]
        document_name += extension

    result = await session.execute(
        select(Document).where(Document.name == document_name)
    )
    document = result.scalar_one_or_none()
    if document:
        raise DocumentAlreadyExistsError()

    await file.seek(0)

    os.makedirs(DOCUMENTS_DIR, exist_ok=True)
    file_path = os.path.join(DOCUMENTS_DIR, document_name)

    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise DocumentNotSavedError()

    new_document = Document(
        name=document_name, path=file_path, date=datetime.now(timezone.utc)
    )
    session.add(new_document)
    try:
        await session.commit()
        await session.refresh(new_document)
    except Exception as e:
        await session.rollback()
        os.remove(file_path)
        raise DocumentNotSavedError()

    return new_document.id


async def delete_document(document_id: int, session: AsyncSession):
    await session.execute(
        delete(DocumentsText).where(DocumentsText.id_doc == document_id)
    )
    result = await session.execute(select(Document).where(Document.id == document_id))
    document = result.scalar_one_or_none()

    if not document:
        raise DocumentNotFoundError(f"Документ с id {document_id} не найден")

    file_path = document.path
    if os.path.exists(file_path):
        os.remove(file_path)

    await session.delete(document)
    await session.commit()


async def get_text_document(document_id: int, db: AsyncSession):
    stmt = (
        select(Document)
        .options(joinedload(Document.document_texts))
        .where(Document.id == document_id)
    )
    result = await db.execute(stmt)
    document = result.unique().scalar_one_or_none()

    if not document:
        raise DocumentNotFoundError(f"Документ с id {document_id} не найден")

    document_text_entry = (
        document.document_texts[0] if document.document_texts else None
    )

    if not document_text_entry:
        raise DocumentNotFoundError(f"Текст для документа с id {document_id} не найден")

    return document.name, document_text_entry.text
