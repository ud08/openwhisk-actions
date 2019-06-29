import requests
def main(params):
    dict = {}
    r = requests.get("http://192.168.60.12:32660/api/ipam/prefixes")
    dict = r.json()
    prefixId = ""
    for prefix in dict["results"]:
        if prefix["prefix"] == params["prefix"] :
            prefixId = prefix["id"]
    avail_ips= []
    print(prefixId)
    if prefixId == "" :
        return {"Error" : "No such pool exists"}
    ip = requests.get("http://192.168.60.12:32660/api/ipam/prefixes/"+str(prefixId)+"/available-ips/",auth=('admin','admin'))

    if len(ip.json()) < params["number"] : 
        return {"error": "Number of IP you requested in givrn pool are not available"}
    for i in range(params["number"]):
        avail_ips.append(ip.json()[i]['address'])
        data = {"address":ip.json()[i]['address'], "status":1}
        url = "http://192.168.60.12:32660/api/ipam/ip-addresses/"
        headers = {"Authorization":"Token 0123456789abcdef0123456789abcdef01234567  "}
        r = requests.post(url,headers=headers,data=data)
        r = requests.post("http://192.168.60.12:32660/api/ipam/ip-addresses/",data=data,auth=('admin','admin'))
    dic = {"Available IPs":avail_ips}
    return dic

