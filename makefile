test:
	@echo "Runing Pytest"
	pytest -vs --clean-alluredir --alluredir tmp/allure_results
report:
	@echo "Check pytest report."
	allure serve tmp/allure_results
