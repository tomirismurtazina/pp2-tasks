import json
with open("sample-data.json", "r") as f:
    dict=json.load(f)
data=dict["imdata"]
print("Interface Status")
print("================================================================================")
print("DN                                                 Description           Speed    MTU")
print("-------------------------------------------------- --------------------  ------  ------")
#print(dict["imdata"][0]["attributes"]["dn"], "         ", dict["imdata"][0]["attributes"]["descr"], "                     ", dict["imdata"][0]["attributes"]["speed"], "   ", dict["imdata"][0]["attributes"]["mtu"])
#print(dict["imdata"][1]["attributes"]["dn"], "         ", dict["imdata"][1]["attributes"]["descr"], "                     ", dict["imdata"][1]["attributes"]["speed"], "   ", dict["imdata"][1]["attributes"]["mtu"])
#print(dict["imdata"][2]["attributes"]["dn"], "         ", dict["imdata"][2]["attributes"]["descr"], "                     ", dict["imdata"][2]["attributes"]["speed"], "   ", dict["imdata"][2]["attributes"]["mtu"])
i=0
for k in data:
    while i<3:
        l=k["l1PhysIf"]
        at=l["attributes"]
        dn=at["dn"]
        d=at["descr"]
        s=at["speed"]
        m=at["mtu"]
        print(f"{dn:50} {d:21} {s:7} {m:15}")
        i+=1
