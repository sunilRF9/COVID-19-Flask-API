from celery import Celery 
app = Celery('celery_tasks',
        broker='amqp://admin:admin@localhost:5672/')
        #broker='amqp://admin:admin@rabbit:5672/')
