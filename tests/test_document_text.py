# from src.models.document import DocumentsText
# import pytest
#
#
# @pytest.mark.asyncio
# async def test_documents_text_creation(async_session, document):
#     document_text = DocumentsText(
#         id_doc=document.id, text="Пример текста для документа"
#     )
#     async_session.add(document_text)
#     await async_session.commit()
#
#     result = await async_session.get(DocumentsText, document_text.id)
#     assert result is not None
#     assert result.text == "Пример текста для документа"
#     assert result.id_doc == document.id
