import util
import database

# Get number of order items loaded


def count(file):
    total = 0
    counter = 1
    res = util.readFile(file)
    for item in res:
        print(counter)
        count = database.getOrderitems(item)
        total += count[0][0]
        print(item)
        print(count[0][0])
        counter += 1
    return total


# Get number of orders loaded. if order was not loaded, log the orderline key
def getOrdersLoaded():
    orders = database.orders()
    total = 0
    for i in range(len(orders)):
        ref = str(database.orders()[i][1])
        res = util.callGETAPI(ref)
        if res["data"]["order"] != None:
            total += 1
            print(ref + " Success")
        else:
            util.errorWriteLoaded(ref)
            print(ref)

    return total


# print(getOrdersLoaded())
count('request-error.txt')
