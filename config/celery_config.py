from datetime import timedelta

from config.database_config import DB_USER, DB_PASS, DB_HOST, DB_NAME

broker_url = 'redis://redis:6379/0'
result_backend = 'redis://redis:6379/0'


task_serializer = 'json'
result_serializer = 'json'
accept_content = ['json']
timezone = 'Asia/Vladivostok'
enable_utc = True


