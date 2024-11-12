# # tests/factories.py
# import factory
# from datetime import datetime
# from faker import Faker
# from src.models.document import Document, DocumentsText
#
#
# faker = Faker("ru_RU")
#
#
# class DocumentFactory(factory.alchemy.SQLAlchemyModelFactory):
#     class Meta:
#         model = Document
#         sqlalchemy_session = None
#         sqlalchemy_session_persistence = "commit"
#
#     name = factory.LazyAttribute(lambda x: faker.word())
#     date = factory.LazyAttribute(lambda x: datetime.now())
#     path = factory.LazyAttribute(lambda x: faker.file_path())
#
#
# class DocumentsTextFactory(factory.alchemy.SQLAlchemyModelFactory):
#     class Meta:
#         model = DocumentsText
#         sqlalchemy_session_persistence = "commit"
#         sqlalchemy_session = None
#
#     id_doc = factory.SubFactory(DocumentFactory)
#     text = factory.LazyAttribute(lambda x: faker.text())
