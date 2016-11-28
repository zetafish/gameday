run-debug:
	python server.py adc1a51632 http://localhost:8000

install:
	pip install -r requirements.txt

run:
	gunicorn -k gevent -w 4 -b :5000 --timeout 180 server:app
