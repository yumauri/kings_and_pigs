init:
	pip3 install -r requirements.txt

run:
	python3 -m kings_and_pigs

# rcc:
# 	/usr/local/Cellar/qt/6.0.2/bin/rcc -binary sectograph/resources/rc.qrc -o sectograph/resources/rc.rcc

format:
	black launcher.py kings_and_pigs

.PHONY: init run rcc format
