from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy import Integer, ForeignKey, String, TIMESTAMP, func
from src.models.base_model import Base


class Document(Base):
    __tablename__ = "documents"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(64), unique=True)
    path: Mapped[str] = mapped_column(String, nullable=False)
    date: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), index=True, server_default=func.now()
    )
    document_texts: Mapped[list["DocumentsText"]] = relationship(
        "DocumentsText", back_populates="document"
    )


class DocumentsText(Base):
    __tablename__ = "documents_text"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True, index=True
    )
    id_doc: Mapped[int] = mapped_column(
        Integer, ForeignKey("documents.id"), nullable=False
    )
    text: Mapped[str] = mapped_column(String, nullable=False)

    document: Mapped["Document"] = relationship(
        "Document", back_populates="document_texts"
    )
