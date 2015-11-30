PNG to JPG converter
=============

## Features
* Queue system
* Error checking and detailed feedback
* Download the converted images (from the links in the left)
* Real time status without reloading the page
* Uploading progress bar
* Wooden server simulator (adds delay to processes, for testing purposes)
* Automatic queue restarting in case the server is shutdown
* Others that I may be forgetting... :O

## Requirements
* Celery
* RabbitMQ
* Python 3.4
 * django
 * django-celery
 * pillow

## Execution
1. Install the dependencies and make sure you add your env/Scripts folder to your system path
2. Start the Broker, in this case RabbitMQ
3. Start celery (from the project root): 
	celery -A pngconverter.models worker -l info --concurrency 3
4. Run the server


