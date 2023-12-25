import json
from requests import get


url = "https://ipinfo.io/"+ "91.174.33.163" + "/json/"
for i in range(100):
    print(get(url).text)
    print(get("http://check.getipintel.net/check.php?ip="+"91.174.33.163"+"&contact=hi1234@gmx.com").text)