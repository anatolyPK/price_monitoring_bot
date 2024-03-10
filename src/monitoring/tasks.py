from celery import Celery
from celery.schedules import crontab

from config.logger import setup_logger
from src.monitoring.monitoring import start_monitoring, get_product_price_and_name_from_handlers


logger = setup_logger(__name__)


app = Celery('tasks')
app.config_from_object('config.celery_config')
app.autodiscover_tasks()


@app.task
def check_new_products_prices():
    start_monitoring()


@app.task
def task_get_product_price_and_name(url):
    result = get_product_price_and_name_from_handlers(url)
    return result


app.conf.beat_schedule = {
    'check_new_products_prices-every-30-seconds': {
        'task': 'src.monitoring.tasks.check_new_products_prices',
        'schedule': crontab(minute='*/3'),
    },
}
