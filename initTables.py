import sys
import sqlite3
import os
import atexit
from JsonToMySQL import fill_tables
import json

#from pprint import pprint

databaseexists = os.path.isfile('main.db')
# connect to the database
_conn = sqlite3.connect('main.db')


# register a function to be called immediately when the interpreter terminates
def _close_db():
    _conn.commit()
    _conn.close()


atexit.register(_close_db)


# our application API:

def create_tables():
    if not databaseexists:
        _conn.executescript("""
            CREATE TABLE mainTbl (
                _id                     TEXT         NOT NULL,
                name                    TEXT         NOT NULL,
                provider                TEXT         NOT NULL,
                privateAccountOwner     TEXT         NOT NULL,
                canUsePrivateRepos      INT          NOT NULL,
                __v                     INT          NOT NULL
            );

            CREATE TABLE limits (
                fieldX        INT          NOT NULL,
                fieldY        INT          NOT NULL,
                fieldZ        TEXT         NOT NULL,
                _id_mainTbl   TEXT         NOT NULL         REFERENCES mainTbl(_id)
            );

            CREATE TABLE build (
                parallel      INT          NOT NULL,
                nodes         INT          NOT NULL,
                _id_mainTbl   TEXT         NOT NULL         REFERENCES mainTbl(_id)
            );

            CREATE TABLE admins (
                _id           TEXT         NOT NULL,
                _id_mainTbl   TEXT         NOT NULL         REFERENCES mainTbl(_id)
            );
        """)


def extractFromJson(jsonFile):
    try:
        j_file = open(jsonFile)
        return json.load(j_file)
    except:
        print("FAILED OPENNING JSON FILE {}".format(jsonFile))
        exit(1)



def main(args):
    create_tables()
    if len(sys.argv) < 2:
        print("add path to json file")
        exit(1)

    #extract from Json:
    j_dict = extractFromJson(sys.argv[1])
    #pprint(j_dict)
    fill_tables(j_dict)


if __name__ == '__main__':
    main(sys.argv)