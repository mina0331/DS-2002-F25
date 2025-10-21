#!/bin/sh

echo "Refreshing all card sets in card_set_lookup/ ..."

for FILE in card_set_lookup/*.json; do
    SET_ID=$(basename "$FILE" .json)

    echo "Updating data for set ID: '$SET_ID' ..."

    curl -s "https://api.pokemontcg.io/v2/cards?q=set.id:${SET_ID}" -o "$FILE"

    echo "Data for set '$SET_ID' has been written into $FILE"

done 

echo "All card sets have been refreshed. "


