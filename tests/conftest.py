# # tests/conftest.py
#
# import pytest
#
# from src.core.database import new_session
# from tests.factories import DocumentFactory, DocumentsTextFactory
# from src.models.document import DocumentsText, Document
#
#
# @pytest.fixture
# async def async_session():
#     async with new_session() as session:
#         yield session
#
#
# @pytest.fixture
# async def document(async_session):
#     DocumentFactory._meta.sqlalchemy_session = async_session
#     document = DocumentFactory()
#     async_session.add(document)
#     await async_session.commit()
#     return document
#
#
# @pytest.fixture
# async def documents_text(async_session, document):
#     DocumentsTextFactory._meta.sqlalchemy_session = async_session
#     document_text = DocumentsTextFactory(id_doc=document.id)
#     async_session.add(document_text)
#     await async_session.commit()
#     return document_text
