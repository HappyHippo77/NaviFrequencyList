import json
import sqlite3
from sqlite3 import Error
import csv


def create_connection(path):
    connection = None
    try:
        connection = sqlite3.connect(path)
        print("Connection to SQLite DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection


frequency_db = create_connection(
    'C:/Users/Conner/Desktop/Coding/Python/Discord.py/Ewo2/cogs/frequency/word_frequency.db')

output_db = create_connection('output/Na\'vi Frequency List.db')


def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
    except Error as e:
        if str(e) != 'UNIQUE constraint failed: words.word_info':
            print(f"The error '{e}' occurred")


def execute_read_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f"The error '{e}' occurred")


execute_query(output_db, """
CREATE TABLE IF NOT EXISTS words (
  word TEXT PRIMARY KEY,
  count INTEGER,
  meaning TEXT,
  type TEXT
);
""")


words = execute_read_query(frequency_db, "SELECT * FROM words ORDER BY count DESC")

separator = "\t"

execute_query(output_db, "DELETE FROM words")
json_output = {}
words_listed = 0
words_counted = 0
with open('output/Na\'vi Frequency List.csv', 'w', encoding='utf-8') as csv_file:
    csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    for word in words:
        # DB OUTPUT
        execute_query(output_db, """
                                INSERT INTO
                                  words (word, count, meaning, type)
                                VALUES
                                ('""" + word[0] + """', """ + str(word[1]) + """, '""" + word[2] + """', '""" + word[3] + """')
                                """)

        # CSV OUTPUT
        row = [word[0], word[1], word[2], word[3]]
        csv_writer.writerow(row)

        # JSON OUTPUT
        json_output[word[0]] = {"count": word[1], "meaning": word[2], "type": word[3]}

        # README SETUP
        words_listed += 1
        words_counted += word[1]

with open('output/Na\'vi Frequency List.json', 'w', encoding='utf-8') as f:
    json.dump(json_output, f, indent=4, ensure_ascii=False)

# README OUTPUT
with open("output/README.md", 'w', encoding='utf-8') as f:
    f.write(
"""
# Na'vi Language Frequency List

#### This list is not a complete collection of all the words in the language.

It was compiled automatically by scanning various sources and using an API to gather the required information.  
The list includes the word, its meaning, its part of speech, and the number of times it was counted in all of the source material.  
If you need the list in another file format, send an issue with a request for it and I'll do what I can.  

Info:  
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;・Words listed: """ + str(words_listed) + """  
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;・Total words counted: """ + str(words_counted) + """

Sources:  
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;・#💙nìna’vi-nì’aw (Kelutral Discord Server) [https://www.kelutral.org/]  
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;・#🐣nìna’vi-sngä’iyufpi (Kelutral Discord Server) [https://www.kelutral.org/]  
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;・Fmawn ta 'Rrta (All releases since 08/22/2020) [https://fmawnrrta.weebly.com/]  
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;・Fmawn ta Nahura [https://fmawntanahura.wordpress.com/]  
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;・Pìlok Wllìmä [https://wimiso.nl/x-navi/pilok/]  

APIs and Libraries:  
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;・Wllìm's API [https://reykunyu.wimiso.nl/]  
""")
