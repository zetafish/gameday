ZIP=kinesis.zip web.zip

.DEFAULT_GOAL=build


run-debug:
	python server.py adc1a51632 http://localhost:8000

install:
	pip install -r requirements.txt

run:
	gunicorn -k gevent -w 4 -b :5000 --timeout 180 server:app

kinesis.zip: kinesis.py
	zip $@ $<

publish.zip: publish.py
	zip $@ $<

web.zip: web.py
	zip $@ $<

build: $(ZIP)

clean:
	rm *.zip
