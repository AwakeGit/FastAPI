import asyncio
from sqlalchemy import select

from celery import Celery
import os
import pytesseract
from PIL import Image

from src.core.database import new_session

from src.models.document import DocumentsText, Document
from src.utils.exceptions import DocumentNotSavedError, DocumentNotFoundError


celery_app = Celery(
    "tasks",
    broker="amqp://guest:guest@localhost:5672//",
    # broker="amqp://guest:guest@rabbitmq:5672//",
    # celery=Celery("tasks"),
    backend="rpc://",
)


@celery_app.task
def extract_text_from_image_task(document_id: int):
    import nest_asyncio

    nest_asyncio.apply()
    asyncio.run(extract_text_from_image(document_id))


async def extract_text_from_image(document_id: int):
    async with new_session() as session:
        stmt = select(Document).where(Document.id == document_id)
        result = await session.execute(stmt)
        document = result.scalar_one_or_none()

        if not document:
            raise DocumentNotFoundError(f"Документ с id {document_id} не найден")

        try:
            image = Image.open(document.path)
            document_text = pytesseract.image_to_string(image)
        except Exception as e:
            return {"status": "error", "message": f"Ошибка OCR: {e}"}

        text_entry = DocumentsText(id_doc=document_id, text=document_text)
        session.add(text_entry)

        try:
            await session.commit()
            await session.refresh(text_entry)
        except Exception as e:
            await session.rollback()
            raise DocumentNotSavedError(f"Ошибка при сохранении: {e}")

        return {
            "id": document_id,
            "name": document.name,
            "text": document_text,
            "status": "success",
            "message": "Текст документа успешно сохранен",
        }
