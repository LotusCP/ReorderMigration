import pyodbc


def connect():
    # 'tcp:reorderhistory.database.windows.net,1433'  # 127.0.0.1, 1433'
    server = '127.0.0.1, 1433'
    database = 'CPMigration'  # 'Reorderhistory'  # 'CPMigration'
    username = 'sa'  # 'eugene'  # 'sa'
    password = 'reallyStrongPwd123'  # 'lotus123!'  # 'reallyStrongPwd123'
    cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=' +
                          server+';DATABASE='+database+';UID='+username+';PWD=' + password)
    cursor = cnxn.cursor()
    return cursor


def orders():
    cursor = connect()
    res = []
    # "SELECT * FROM [CPMigration].[dbo].[orders-MY-MC1];"
    tsql = "SELECT * FROM [dbo].[first-Orders-MC2];"
    with cursor.execute(tsql):
        row = cursor.fetchone()
        while row:
            #print (str(row[0]) + " " + str(row[1]))
            res.append(row)
            row = cursor.fetchone()
    return res


def orderitems(orderkey):
    cursor = connect()
    res = []
    tsql = "SELECT * FROM [dbo].[combined] where orderkey = '{0}';".format(
        orderkey)
    # "SELECT * FROM [CPMigration].[dbo].[orderItems-MY-MC1] where orderkey = {0};".format(
    # orderkey)
    with cursor.execute(tsql):
        row = cursor.fetchone()
        while row:
            res.append(row)
            row = cursor.fetchone()

    # print(res)
    return res


def getOrderitems(orderkey):
    cursor = connect()
    res = []
    tsql = "SELECT count(ITEMSPRODUCTREF) FROM [CPMigration].[dbo].[orderItems-MY-MC1] where orderkey = {0};".format(
        orderkey)
    with cursor.execute(tsql):
        row = cursor.fetchone()
        while row:
            res.append(row)
            row = cursor.fetchone()

    # print(res)
    return res
