=============
PNG to JPG converter

## Requirements
* Celery
* RabbitMQ
* Python
 * django
 * django-celery
 * pillow

## Execution
1) Make sure you add your env/Scripts folder in your system path
2) Start the Broker, in this case RabbitMQ
3) Start celery (from the project root): 
	celery -A pngconverter.models worker -l info --concurrency 3
4) Run the server

