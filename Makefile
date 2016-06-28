test: ve/bin/python
	./ve/bin/flake8 waterquality --max-complexity=7
	./ve/bin/python runtests.py

ve/bin/python: setup.py
	rm -rf ve
	virtualenv ve
	./ve/bin/pip install "Django<1.9"
	./ve/bin/pip install django-googlecharts==1.0-alpha-1 --index-url https://pypi.ccnmtl.columbia.edu/
	./ve/bin/pip install pysqlite==2.6.3 --index-url https://pypi.ccnmtl.columbia.edu/
	./ve/bin/pip install .
	./ve/bin/pip install flake8

clean:
	rm -rf ve
	find . -name '*.pyc' -exec rm {} \;
