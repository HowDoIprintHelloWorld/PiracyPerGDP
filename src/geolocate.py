import json
from requests import get
import pandas as pd


def proxyCheck(ip: str, strictness: int):
    urlProxyCheck = "http://check.getipintel.net/check.php?ip="+ ip +"&contact=hi2234@gmx.com"
    try:
        probability = get(urlProxyCheck, timeout=2).text
        probability = float(probability)
        return probability >= strictness
    except Exception as e:
        return True


def getGeoLocation(ip):
    try:
        urlGeolocate = "https://ipinfo.io/"+ ip + "/json/"
        data = get(urlGeolocate, timeout=2).text
        data = json.loads(data)
        data = {key: val for key, val in data.items() if key in ["city", "region", "country"]}
        return data
    except Exception as e:
        return {}


def getAllInfoOfIp(ip):
    key = "f0h147-821538-j6i739-476d63" # Key 1
    key = "yl1b8f-022h76-64f599-504273" # Key 2
    key = "8t7308-8s766a-ax0722-7k0296"
    url = f"http://proxycheck.io/v2/{ip}?key={key}&vpn=1&asn=1&cur=0&risk=1&port=1&seen=1&days=7&tag=msg"
    data = get(url, timeout=2).text
    data = json.loads(data)
    if data["status"] == "denied":
        print(data["message"])
        return {}, False
    data = data[ip]
    print(f"Got data on IP {ip}: ", data["country"], data["proxy"])
    return {"country": data["country"], "proxy": data["proxy"] != "no"}, True
    



def readCSV():
    df = pd.read_csv("ipAddresses.csv", index_col=False)
    return df


"""
def getDataOnAllIps(ips):
    allData = []
    for ip in ips:
        isProxy = proxyCheck(ip, 0.9)
        location = getGeoLocation(ip) if not isProxy else {}
        data = {"ip": ip, "isProxy": isProxy}
        data.update(location) 
        allData += data
    print(allData)
"""

def getDataOnAllIps(df):
    try:
        for ipData in df.itertuples():
            if ipData.evaluated:
                continue
            data, worked = getAllInfoOfIp(ipData.ip)
            if not worked:
                break
            df.at[ipData.Index, "country"] = data["country"]
            df.at[ipData.Index, "proxy"] = data["proxy"]
            df.at[ipData.Index, "evaluated"] = True
    except (Exception, KeyboardInterrupt) as e:
        print("Stopped due to exception:", e)
        pass
    return df


df = readCSV()
df = getDataOnAllIps(df)
df.to_csv("ipAddresses.csv", index=False)
# print(data, worked)
# getAllInfoOfIp("145.126.57.35")
