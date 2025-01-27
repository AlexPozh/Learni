from celery import Celery

celery_app = Celery(
    "learni", 
    broker="redis://redis:6379/0",    #TODO здесь нужно будет менять `localhost` на название контенера `redis` внутри `docker compose` 
    backend="redis://redis:6379/1"    #TODO здесь нужно будет менять `localhost` на название контенера `redis` внутри `docker compose` 
)

# Автоматическая регистрация задач из модуля tasks
celery_app.autodiscover_tasks(["tasks.tasks"])