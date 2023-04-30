import csv
import json
import os

with open('json/course_aliases.json') as c:
    course_aliases = json.load(c)
with open('json/prof_aliases.json') as p:
    prof_aliases = json.load(p)

def read_all(raw_file, processed_file):
    with open(raw_file, 'r', encoding='UTF8') as raw, open(processed_file, 'w', newline='', encoding='UTF8') as processed:
        reader = csv.reader(raw)
        writer = csv.writer(processed)
        first = next(reader)
        if first != ["year", "semester", "carleton_code", "alternative_code", "course_name", "professor", "link_to_outline"]:
            return False
        writer.writerow(first)
        for row in reader:
            if row[4] in course_aliases:
                row[4] = course_aliases[row[4]]
            if row[5] in prof_aliases:
                row[5] = prof_aliases[row[5]]
            
            writer.writerow(row)

read_all("csv/raw.csv", "csv/processed.csv")      
                
        
        
