import requests
import base64
import json
def req(query):
	info={
	     'text':query,
	     'source_id': 110000,
	     'last_task':{},
	     'controller_position':{'001':0.7,'002':0.3},
	    'request_id':123456,
	     }
	#res=requests.post('http://192.168.29.83:18083/push',json=json.dumps(info))
	#res=requests.post('http://129.146.177.165:8083/push ',json=json.dumps(info))
	res=requests.post('http://192.168.29.238:11436/push',json=json.dumps(info))
	#print(info)
    #print(res.content)
    return json.loads(res.content)

content = ""
index=0
for line in open("base.txt"):
    line = line.strip()
    print("++++++++++++")
    res = req(line)
    print("=============")
    #['task_list']
    print(res)
    content += f"{str(index).zfill(5)}\t{line}\t{res}\n"
    index+=1
    #break

#with open("res_all100.txt","w") as f1:
#    f1.write(content)
