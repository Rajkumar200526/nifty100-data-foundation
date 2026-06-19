load:
	python src/etl/loader.py

ratios:
	python ratios.py

test:
	pytest tests/

report:
	python report.py

dashboard:
	python dashboard.py

api:
	python api.py

clean:
	del /q output\*