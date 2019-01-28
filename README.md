# JsonToSql
Parse a JSON file and dynamically pass all its documents into a MySQL database table

To run Json to MySQL Program:
- go to project's directory
- run: python initTables.py [json file path]

(example: python initTables.py accounts.json)

Output:
The output is a sqlite DB called: "main.db"

Note:
1. python 3.4 (and above) is needed in order to run the program
2. Libraries that is needed to be installed:
    - sqlite3
    - json

Enjoy!
