#!/usr/local/bin/python

import sqlite3

ID = "_id"


def _connect_db():
    global cur
    global con
    # connect to the database
    con = sqlite3.connect('main.db')


# register a function to be called immediately when the interpreter terminates
def _close_db():
    con.commit()
    con.close()


def sendInsert(keys, vals, tabl_name):
    global con
    query_prefix = "INSERT INTO {} ({})".format(tabl_name, ','.join(keys))
    #print("query prefix is %s" % query_prefix) #temp
    vals_str = ','.join(["?"] * len(vals))
    query = query_prefix + " VALUES ({})".format(vals_str)
    pquery = query_prefix + " VALUES ({})".format(','.join(vals))
    print("QUERY IS: %s" % pquery)
    try:
        con.execute(query,vals)
    except Exception, e:
        print "Error %s" % (e)


def sendSelect():
    global con
    cur = con.cursor()
    query = "SELECT * FROM mainTbl"
    print("QUERY IS: %s" % query)
    try:
        cur.execute(query)
        return cur.fetchall()
    except Exception, e:
        print "Error %s" % (e)


def insert(data_to_insert, tabl_name):
    feilds = filter(lambda col: not isinstance(data_to_insert[col], dict) and not isinstance(data_to_insert[col], list),
                    data_to_insert.keys())
    vals = [str(data_to_insert[col]) for col in feilds]
    sendInsert(feilds, vals, tabl_name)
    for col in data_to_insert.keys():
        if isinstance(data_to_insert[col], dict):
            data_to_insert[col]["_id_{}".format(tabl_name)] = data_to_insert[ID]
            insert(data_to_insert[col], col)
        if isinstance(data_to_insert[col], list):
            for element in data_to_insert[col]:
                element_dict = {}
                element_dict['_id_{}'.format(tabl_name)] = data_to_insert[ID]
                element_dict[ID] = element
                insert(element_dict, col)


def fill_tables(j_dict):

    # open database connection
    _connect_db()
    for key in j_dict:
        insert(key, "mainTbl")

    print("MySQL insert is done!")

    #print sendSelect()

    # close database connection
    _close_db()