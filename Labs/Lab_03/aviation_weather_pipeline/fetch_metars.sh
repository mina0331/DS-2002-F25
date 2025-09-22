#!/bin/bash

set -e

API_URL="https://aviationweather.gov/api/data/metar"
OUTPUT_DIR="raw_metars"
AIRPORT_CODES_FILE="airport_codes.txt"

mkdir -p $OUTPUT_DIR

echo "Fetching METAR data for airports..."

while read -r airport_code; do
    if [ -z "$airport_code" ]; then
        continue 
    fi
    
    URL="$API_URL?ids=$airport_code&format=json"
    OUTPUT_FILE="$OUTPUT_DIR/${airport_code}.json"
    
    echo "  -> Fetching data for $airport_code..."
    
    curl -s "$URL" -o "$OUTPUT_FILE" 2>&1
    #directing the standard error to standard output so that error messages are visible. 
    
    if [ $? -ne 0 ]; then
        echo "Error: curl failed for $airport_code." >&2
        exit 1
        #$?: a special variable that holds the exit status of the previous command
        #if it's not equal to 0, exit 
    fi
    
    if [ ! -s "$OUTPUT_FILE" ] || [ "$(jq 'length' "$OUTPUT_FILE")" -eq 0 ]; then
        echo "Warning: No METAR data found for $airport_code. THE API returned an empty response."
    else 
        echo "  -> Data for $airport_code saved successfully."
    fi

done < "$AIRPORT_CODES_FILE"
echo "Data fetching complete. Check the '$OUTPUT_DIR' directory."
    

