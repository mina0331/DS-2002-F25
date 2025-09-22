.PHONY: all fetch analyze clean 

all: analyze

analyze: fetch
	@echo "--- Analyzing---"
	bash ./analyze_data.sh
	@echo "--- Pipeline complete ---"

fetch: 
	@echo "-- Fetching data --"
	bash ./fetch_metars.sh
	
clean: 
	@echo "--- Cleaning up ---"
	rm -rf raw_metars
	rm -f weather_report.csv

	
