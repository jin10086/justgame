import requests
from pymongo import MongoClient
from multiprocessing import Pool


db = MongoClient()["just"]["transactions"]
db1 = MongoClient()["just"]["ref"]
address_all = db.distinct('raw_data.contract.parameter.value.owner_address')

s = requests.Session()

url = "https://api.trongrid.io/wallet/triggersmartcontract"

def runPool(f, arr):
    with Pool() as pool:
        pool.map(f, arr)

def go(address):
    refS = 0
    for i in range(6):  ## 0-5级邀请
        parameter = address.rjust(64,'0') + str(i).rjust(64,'0')
        data = {
            "contract_address": "41e3cf5eefe3a2abf35a344ae8a3b2f4bb29810cbd",
            "owner_address": "410e5034e571bea5eced424290afa5835a282cb7c4",
            "function_selector": "referralDataOf(address,uint256)",
            "parameter": parameter,
            "call_value": 0,
            "fee_limit": 1000000000,
        }
        z1 = s.post(url,json=data)
        v = '0x'+ z1.json()['constant_result'][0][64:]
        refS += (int(v,16)/1e6)
    print('address:',address,' ','ref:',refS)
    db1.insert_one({'address':address,"ref":refS})

if __name__ == "__main__":
    runPool(go,address_all)