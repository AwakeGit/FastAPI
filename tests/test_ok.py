# from select import select
#
# import pytest
# from httpx import AsyncClient
#
# from src.main import app
# from src.models.document import Document, DocumentsText
# from src.core.database import new_session
#
#
# @pytest.mark.asyncio
# async def test_doc_delete():
#     # Создаем тестовый документ и связанный текст
#     async with new_session() as session:
#         # Создаем документ
#         test_document = Document(name="test_document.txt", path="/test/path")
#         session.add(test_document)
#         await session.flush()  # Фиксируем изменения для получения ID документа
#         doc_id = test_document.id
#
#         # Создаем связанный текст для документа
#         test_document_text = DocumentsText(text="Тестовый текст", id_doc=doc_id)
#         session.add(test_document_text)
#         await session.commit()  # Сохраняем изменения в базу данных
#
#     # Используем http-клиент для выполнения DELETE-запроса
#     async with AsyncClient(app=app, base_url="http://test") as client:
#         response = await client.delete(f"/delete_doc?document_id={doc_id}")
#
#     # Проверяем ответ от сервера
#     assert response.status_code == 200
#     assert response.json() == {
#         "id": doc_id,
#         "status": "success",
#         "message": "Документ успешно удален",
#     }
#
#     # Проверяем, что документ удален из базы данных
#     async with new_session() as session:
#         deleted_document = await session.get(Document, doc_id)
#         assert deleted_document is None  # Документ должен быть удален
#
#         # Также проверяем, что удален и связанный текст
#         related_text = await session.execute(
#             select(DocumentsText).filter_by(id_doc=doc_id)
#         )
#         assert related_text.scalar_one_or_none() is None  # Текст должен быть удален
