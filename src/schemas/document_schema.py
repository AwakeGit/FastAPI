from pydantic import BaseModel, ConfigDict, Field
from typing import List


class DocumentCreate(BaseModel):
    name: str = Field(..., description="Название документа для загрузки")


class DocumentResponse(BaseModel):
    id: int = Field(..., description="Идентификатор документа")
    name: str = Field(..., description="Название документа")
    status: str = Field(..., description="Статус операции")
    message: str = Field(..., description="Сообщение операции")

    model_config = ConfigDict(from_attributes=True)


class DocumentDelete(BaseModel):
    id: int = Field(..., description="Идентификатор удаленного документа")
    status: str = Field(..., description="Статус операции")
    message: str = Field(..., description="Сообщение операции")

    model_config = ConfigDict(from_attributes=True)


class DocumentAnalyse(BaseModel):
    id: int = Field(..., description="Идентификатор документа для анализа")
    status: str = Field(..., description="Статус операции")
    message: str = Field(..., description="Сообщение операции")

    model_config = ConfigDict(from_attributes=True)


class DocumentTextResponse(BaseModel):
    id: int = Field(..., description="Идентификатор текста документа")
    document_id: int = Field(..., description="Идентификатор документа")
    text: str = Field(..., description="Текст документа")
    status: str = Field(..., description="Статус операции")
    message: str = Field(..., description="Сообщение операции")

    model_config = ConfigDict(from_attributes=True)


class DocumentTextsResponse(BaseModel):
    document_id: int = Field(..., description="Идентификатор документа")
    texts: List[DocumentTextResponse] = Field(..., description="Тексты документа")

    model_config = ConfigDict(from_attributes=True)
