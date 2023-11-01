
import pickle
import  numpy as np

import requests

p1={"lat":14.419463,"lon":75.915380}
rest_url = "https://rest.isric.org"
prop_query_url = f"{rest_url}/soilgrids/v2.0/properties/query"

props = {"property":"silt","depth":"0-5cm","value":"mean"}
res1=requests.get(prop_query_url,params={**p1 , **props})
#print(res1)
print(res1.json()['properties']["layers"][0]["depths"][0]["values"])

res=res1.json()['properties']["layers"][0]["depths"][0]["values"]

print("Silt = {}".format(res["mean"]/10))

silt=res["mean"]/10

props = {"property":"sand","depth":"0-5cm","value":"mean"}
res1=requests.get(prop_query_url,params={**p1 , **props})
#print(res1)
print(res1.json()['properties']["layers"][0]["depths"][0]["values"])

res=res1.json()['properties']["layers"][0]["depths"][0]["values"]

print("Sand = {}".format(res["mean"]/10))

sand=res["mean"]/10

props = {"property":"phh2o","depth":"0-5cm","value":"mean"}
res1=requests.get(prop_query_url,params={**p1 , **props})
#print(res1)
print(res1.json()['properties']["layers"][0]["depths"][0]["values"])

res=res1.json()['properties']["layers"][0]["depths"][0]["values"]

print("Ph = {}".format(res["mean"]/10))

ph=res["mean"]/10

props = {"property":"clay","depth":"0-5cm","value":"mean"}
res1=requests.get(prop_query_url,params={**p1 , **props})
#print(res1)
print(res1.json()['properties']["layers"][0]["depths"][0]["values"])

res=res1.json()['properties']["layers"][0]["depths"][0]["values"]
print("clay = {}".format(res["mean"]/10))

clay=res["mean"]/10

props = {"property":"nitrogen","depth":"0-5cm","value":"mean"}
res1=requests.get(prop_query_url,params={**p1 , **props})
#print(res1)
print(res1.json()['properties']["layers"][0]["depths"][0]["values"])

res=res1.json()['properties']["layers"][0]["depths"][0]["values"]

print("nitrogen = {}".format(res["mean"]/10))

nitrogen=res["mean"]/10

data = np.array([[ph]])

print("data1 = ",data)
#data = np.array([[6.23,2.10,22.0,34,5.0]])

print("data = ",data)
#data = np.array([[6.23,2.10]])
file = open("Knnnew.pkl",'rb')
object_file = pickle.load(file)
prediction = object_file.predict(data)
print("Recomended crop is = ",prediction[0])