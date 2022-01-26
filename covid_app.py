import requests
from datetime import datetime, timedelta
import time
import json
import boto3
client = boto3.client('sns')

age = 25
pin_vapi=[]
#167
#pin_mumbai=[395]
pin_mumbai=[400008]
pin_khordha=[]
pincodes = pin_vapi + pin_mumbai +pin_khordha
num_days = 6

print_flag = 'Y'

print("Starting search for Covid vaccine slots!")

actual = datetime.now(tz=None) + timedelta(hours=5,minutes=30)
print(actual)
list_format = [actual + timedelta(days=i) for i in range(num_days)]
actual_dates = [i.strftime("%d-%m-%Y") for i in list_format]
list_vapi=[]
list_mumbai=[]
list_khordha=[]
def lambda_handler(event, context):

    
  
    for pincode in pincodes:   
        for given_date in actual_dates:

            #URL = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id={}&date={}".format(pincode, given_date)
            URL = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode={}&date={}".format(pincode, given_date) 
            header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36','Cache-Control':'max-age=0'} 
            
            result = requests.get(URL, headers=header)

            if result.ok:
                response_json = result.json()
                
                if response_json["centers"]:
                    if(print_flag.lower() =='y'):
                        for center in response_json["centers"]:
                            for session in center["sessions"]:
                                if (session["min_age_limit"] <= age and session["available_capacity"] > 0 ) :
                                    if(pincode in pin_vapi):
                                        obj={}
                                        
                                        obj['Block Name']= center["block_name"]
                                        obj['Center name']= center["name"]
                                        obj['Pincode']  = center['pincode']
                                        obj['Available on']=(given_date)
                                        
                                        
                                        obj['Price']= center["fee_type"]
                                        obj['Availablity']= session["available_capacity"]
    
                                        if(session["vaccine"] != ''):
                                            obj['Age Limit']=session['min_age_limit']
                                            obj['Vaccine type']= session["vaccine"]
                                            obj['Dose 1 shots']=session["available_capacity_dose1"]
                                            obj['Dose 2 shots']=session['available_capacity_dose2']
                                        
                                        if obj['Dose 1 shots'] >0:
                                            
                                            list_vapi.append(obj)
                                        
                                        
                                    if(pincode in pin_mumbai):
                                        obj={}
                                        obj['Block Name']= center["block_name"]
                                        obj['Center name']= center["name"]
                                        obj['Pincode']  = center['pincode']
                                        obj['Available on']=(given_date)
                                        
                                        
                                        obj['Price']= center["fee_type"]
                                        obj['Availablity']= session["available_capacity"]
    
                                        if(session["vaccine"] != ''):
                                            obj['Age Limit']=session['min_age_limit']
                                            obj['Vaccine type']= session["vaccine"]
                                            obj['Dose 1 shots']=session["available_capacity_dose1"]
                                            obj['Dose 2 shots']=session['available_capacity_dose2']
                                        
                                        if obj['Dose 2 shots']>1:
                                            
                                            list_mumbai.append(obj)
                                        
                                    
                                    if(pincode in pin_khordha):
                                        obj={}
                                        obj['Block Name']= center["block_name"]
                                        obj['Center name']= center["name"]
                                        obj['Pincode']  = center['pincode']
                                        obj['Available on']=(given_date)
                                        
                                        
                                        obj['Price']= center["fee_type"]
                                        obj['Availablity']= session["available_capacity"]
    
                                        if(session["vaccine"] != ''):
                                            obj['Age Limit']=session['min_age_limit']
                                            obj['Vaccine type']= session["vaccine"]
                                            obj['Dose 1 shots']=session["available_capacity_dose1"]
                                            obj['Dose 2 shots']=session['available_capacity_dose2']
                                        
                                        if obj['Dose 2 shots']>0 and obj['Vaccine type']=='COVAXIN':
                                        
                                            list_khordha.append(obj)
                                        
                                    
                                        
                                    
                                        
                                    
                                
                                
                                   
                                    #counter = counter + 1
            else:
                print("No Response!")
    print(list_vapi)
    print(list_mumbai)
    print(list_khordha)
    
    if len(list_vapi) == 0 or len(list_vapi) == None:
        print("No slot found for Vapi")
    else:
            
        response = client.publish(
        TargetArn='arn:aws:sns:ap-south-1:150175094156:vapi',
        Message=json.dumps({'default': json.dumps(list_vapi,indent=4, separators=(',', ': '))}),
        MessageStructure='json'
        )
        
    if len(list_mumbai) == 0 or len(list_mumbai) == None:
        print("No slot found for Mumbai")
    else:
       
        response = client.publish(
        TargetArn='arn:aws:sns:ap-south-1:150175094156:mumbai',
        Message=json.dumps({'default': json.dumps(list_mumbai,indent=4, separators=(',', ': '))}),
        MessageStructure='json'
        )
        
    if len(list_khordha) == 0 or len(list_khordha) == None:
        print("No slot found for Khordha")
    else:
        
        response = client.publish(
        TargetArn='arn:aws:sns:ap-south-1:150175094156:khordha',
        Message=json.dumps({'default': json.dumps(list_khordha,indent=4, separators=(',', ': '))}),
        MessageStructure='json'
        )
       