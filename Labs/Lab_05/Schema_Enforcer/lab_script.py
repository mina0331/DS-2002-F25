import csv
import json
import pandas as pd

# creating tabular data
data = [
    ["student_id", "major", "GPA","is_cs_major", "credits_taken"],
    [1, "Computer Science", 3.8, "Yes", "18.0"],
    [2, "Data Science", 3.85, "No", "32.0"],
    [3, "Economics", 3.58, "No", "65.0"],
    [4, "Statistics", 3.75, "No", "70.5"],
    [5, "Biology", 4.00, "No", "55.0"]
]

data_dic = [
  {
    "course_id": "DS2002",
    "section": "001",
    "title": "Data Science Systems",
    "level": 200,
    "instructors": [
      {"name": "Austin Rivera", "role": "Primary"}, 
      {"name": "Heywood Williams-Tracy", "role": "TA"} 
    ]
  },
  {
    "course_id": "CS3130",
    "section": "101",
    "title": "Computer Science Systems and Organization 2",
    "level": 300,
    "instructors": [
        {"name": "Charles Reiss", "role": "Primary"},
    ]
  },
  {
    "course_id": "CS3100",
    "section": "001", 
    "title": "Data Structures and Algo 2", 
    "level": 300, 
    "instructors": [
        {"name": "Aaron Bloomfield", "role": "Primary"},
    ]
  },
  {
    "course_id": "CS3240",
    "section": "002",
    "title": "Software Engineering", 
    "level": 300, 
    "instructors": [
        {"name": "Derrick Stone", "role": "Primary"},
    ]
  }
]



with open("raw_survey_data.csv", "w", newline= "") as file: 
    writer = csv.writer(file)
    writer.writerows(data)



with open("raw_course_catalog.json", "w", encoding = "utf-8") as f: 
    json.dump(data_dic, f, indent=4, ensure_ascii=False)
    #encoding = utf-8 meaning ensuring the file can handle any text from any language along with ensure_ascii=False


df = pd.read_csv("raw_survey_data.csv")
#loading the csv file into a data frame 

df["is_cs_major"] = df["is_cs_major"].replace({"Yes": True, "No": False})
#converting yes and no into proper python boolean types (true, false)
df = df.astype ({
    "credits_taken": "float64",
    "GPA": "float64"
})

df.to_csv("clean_survey_data.csv", index=False)
#omitting the index number
print("cleaning data saved into clean_survey_data.csv")

with open("raw_course_catalog.json", "r") as f:
    data = json.load(f)
    
instructors_df = pd.json_normalize(
    data, 
    record_path = ["instructors"],
    meta = ["course_id", "section", "title", "level"]
)

instructors_df.to_csv("clean_course_catalog.csv", index = False)
