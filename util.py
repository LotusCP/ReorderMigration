import pandas as pd
from openpyxl import load_workbook
import requests
from requests.auth import HTTPBasicAuth


def readFile(filename):
    file1 = open(filename, 'r')
    lines = file1.readlines()
    count = 0
    res = []
    for line in lines:
        count += 1
        line = line.strip()
        orderkey = line.split(",", 1)
        res.append(orderkey[0])

    return res


def writeFile(filename, orderkey, msg):
    file_object = open(filename, 'a')
    file_object.write(orderkey + ", " + msg + "\n")
    file_object.close()


def errorWrite(orderkey, req, err, time):

    workbook_name = 'errorlog.xlsx'
    wb = load_workbook(workbook_name)
    page = wb.active

    # New data to write:
    orders = [[str(orderkey), str(err), time]]

    for info in orders:
        page.append(info)

    # This saves the status error code along with orderline key and time of failure
    wb.save(filename=workbook_name)
    # This saves the request body of then failed orderline key
    writeFile('request-error.txt', orderkey, str(req))


# This is used to log the orderline key not found in OMS after loading
def errorWriteLoaded(ref):
    writeFile('errorOrderDetails.txt', ref)


def callLoadAPI(requestJSON):
    response = requests.post(
        "https://ppe-api.lotuss.com.my/proc/order/api/v1/orders/history",
        auth=HTTPBasicAuth('871f14d535bb40269819db33c1e3ddfb',
                           'e3e3002F0c324e398fdF92992bed53da'),
        data=requestJSON,
        headers={'Content-Type': 'application/json'}
    )

    return response


def callGETAPI(key):
    url = "https://qa-api.lotuss.com.my/sys/fluentoms/api/v1/orders?ref={}".format(
        key)
    response = requests.get(
        url,
        auth=HTTPBasicAuth('f2a63aecea1b4ee1a657a5f4c9a480b4',
                           '8069373E36434C13A76105aE3849990B'),
        headers={'X-Correlation-Id': '9235a8a0-a7c8-11eb-9a0d-38f9d3e90b55'}
    )

    return response.json()
