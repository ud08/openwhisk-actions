import requests
import json
import urllib3
def main(params):    
    username = params["username"]
    password = params["password"]
    tenant = params["tenant"]
    BASE_URL = params["BASE_URL"]
    temp = params["catalog_name"]
    subnetmask = params["subnetmask"]
    gateway = params["gateway"]
    ip = params["ip"]
    name = params["name"]
    dns = params["dns"]
    suffix = params["suffix"]
    urllib3.disable_warnings()
    data = {"username":username,"password":password,"tenant":tenant}
    data = json.dumps(data)
    header= {"Content-Type":"application/json","Accept":"application/json"}
    req = requests.post("https://"+BASE_URL+"/identity/api/tokens/",headers=header,data=data,verify=False)
    token = req.json()['id']
    headers = {"Authorization":"Bearer "+token, "Content-Type" : "application/json", "Accept" : "application/json"}
    req2 = requests.get("https://"+BASE_URL+"/catalog-service/api/consumer/entitledCatalogItemViews",headers=headers,verify=False)
    for item in req2.json()['content']:
        if(item['name']==temp):
            id = item['catalogItemId']
            links = item['links']
    for item in links:
        if(item['rel']=='GET: Request Template'):
            getlink = item['href']
        elif(item['rel']=='POST: Submit Request'):
            postlink = item['href']
    req3 = requests.get(getlink,headers=headers,verify=False)
    data = req3.json()
    data["data"]["vSphere__vCenter__Machine_1"]["data"]["VirtualMachine.Network0.Address"] = ip
    data["data"]["vSphere__vCenter__Machine_1"]["data"]["VirtualMachine.Network0.DnsSuffix"] = suffix
    data["data"]["vSphere__vCenter__Machine_1"]["data"]["VirtualMachine.Network0.Gateway"] = gateway
    data["data"]["vSphere__vCenter__Machine_1"]["data"]["VirtualMachine.Network0.Name"] = name
    data["data"]["vSphere__vCenter__Machine_1"]["data"]["VirtualMachine.Network0.PrimaryDns"] = dns
    data["data"]["vSphere__vCenter__Machine_1"]["data"]["VirtualMachine.Network0.SubnetMask"] = subnetmask
    data = json.dumps(data)
    req4 = requests.post(postlink,headers=headers,data=data,verify=False)
    return req4.json()



# main({"username":"administrator","password":"pM0dularc!","tenant":"ICDS","BASE_URL":"192.168.56.5","catalog_name":"Sree-Linux-copy","subnetmask":"255.255.252.0","gateway":"192.168.56.1","dns":"192.168.56.2","suffix":"icds.online","ip":"192.168.57.15","name":"DPortGroup"})