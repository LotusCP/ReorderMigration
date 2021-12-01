import database
import json
import util
import datetime
from openpyxl import load_workbook
from requests.auth import HTTPBasicAuth


def buildAPI():
    orders = database.orders()
    count = 0
    for i in range(4):
        print(database.orders()[i][19])
        lineItems = database.orderitems(orders[i][19])
        totalPrice = database.orders()[i][24] + database.orders()[i][25]
        parentJSON = {
            "ref": str(database.orders()[i][1]),
            "type": database.orders()[i][2],
            "customerId": database.orders()[i][22],
            "orderSubTotalWithDiscount": database.orders()[i][24],
            "orderSubtotal": database.orders()[i][24],
            "deliveryCharges": database.orders()[i][25],
            # what is this? is it subtotal?
            "totalPrice": totalPrice,
            "couponDiscount": 0,
            "grandTotal": totalPrice,  # is it subtotal?
            "totalOrderSaving": 0,  # TBC - how to derive or hardcode as 0
            "clubCard": {
                "clubPointsRedeem": 0,
                "clubPointsDiscount": 0
            },
            "paymentTransaction": [  # relook at this - need payment method / paid amt
                {
                    "paymentMethod": "CreditCard",
                    "paymentType": "POLCC",
                    "authorizedAmount": 0,
                    "status": ""
                }
            ],
            "deliveryDate": str(database.orders()[i][6]),
            "fulfilmentChoice": {
                "deliveryType": str(database.orders()[i][8]),
                "currency": "MYR",  # hardcoded value to RM since only MY instance
                "deliveryInstruction": "",  # sent as blank
                "pickupLocationRef": str(database.orders()[i][9]),
                "deliveryAddress": {
                    "ref": str(database.orders()[i][10]),
                    "name": database.orders()[i][11],
                    "street": database.orders()[i][15],
                    "region": "",  # sent as blank
                    "city": database.orders()[i][12],
                    "state": database.orders()[i][13],
                    "country": database.orders()[i][14],
                    "postcode": str(database.orders()[i][16]),
                    "latitude": database.orders()[i][17],
                    "longitude": database.orders()[i][18]
                }
            },
            "deliveryAddress": {
                "firstName": database.orders()[i][11],
                "lastName": "",
                "mobileNo": "",  # missing
                "email": "",  # missing
                "addressLine1": database.orders()[i][15],
                "city": database.orders()[i][12],
                "state": database.orders()[i][13],
                "country": str(database.orders()[i][14]),
                "postcode": str(database.orders()[i][16]),
                "latitude": database.orders()[i][17],
                "longitude": database.orders()[i][18]
            },
            "billingAddress": {
                "addressLine1": database.orders()[i][15],
                "city": database.orders()[i][12],
                "state": database.orders()[i][13],
                "country": str(database.orders()[i][14]),
                "postcode": str(database.orders()[i][16]),
            },
            "fftiRequired": False,
        }
        items = []
        for line in lineItems:
            paid = float(line[6])*float(line[2])
            item = {
                # "ref": line[0],
                "productRef": str(line[1]),
                "quantity": float(line[2]),
                "unitPrice": float(line[6]),
                "paidPrice": paid,
                "totalDiscount": 0,
                "totalPrice": paid,
                "orderDetails": {
                    "totalWeight": 0,  # missing
                    "weightUOM": line[3],
                    "orderBy": "qty",  # missing
                    "unitWeight": float(line[2]),
                    "isWeightedItem": False if line[3] == "Each" else True
                },
                "itemPromotion": [
                    {
                        "promotionType": "",
                        "promotionDiscount": 0
                    }
                ],
                "url": {
                    "imageURL": "",  # missing
                    "prodPageLink": ""  # missing
                }
            }
            items.append(item)

        parentJSON["items"] = items

        print(parentJSON)
        output = json.dumps(parentJSON, indent=4)
        res = util.callLoadAPI(output)

        if res.status_code == 200:
            print("Success: " + str(database.orders()[i][20]))
            print(res.status_code)
        else:
            util.errorWrite(str(database.orders()[i][20]), parentJSON,
                            res.status_code, str(datetime.datetime.now()))
            print("Failed: " + str(database.orders()[i][20]))
        count += 1
        if count == 5:
            break


buildAPI()
