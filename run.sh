uvicorn src.main:app --reload
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
celery -A src.core.celery_worker.celery_app worker --loglevel=info
celery -A src.core.celery_worker.celery_app flower



docker-compose up --build
docker-compose exec app alembic revision --autogenerate -m "Initial migration"
docker-compose exec app alembic upgrade head
docker-compose exec app -A src.core.celery_worker.celery_app flower