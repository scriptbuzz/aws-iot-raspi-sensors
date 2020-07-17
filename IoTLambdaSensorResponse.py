# Name: M Bitar
# Date: March 15, 2020
# Project: AWS IoT Sensor Rule
# TODO: Replace the account specific resource properties with yours such as the SNS Topic ARN and region

from __future__ import print_function
  
import json
import boto3

print('Loading function')
  
def lambda_handler(event, context):
  client = boto3.client('iot-data', region_name='us-east-1')
  sns = boto3.client('sns')
  
  # Parse the JSON message 
  eventText = json.dumps(event)

  # Print the parsed JSON message to the console. You can view this text in the Monitoring tab in the AWS Lambda console or in the Amazon CloudWatch Logs console.
  print('Received event: ', eventText)  
  
  SENSOR_TYPE = event['SENSOR_TYPE']
  VALUE = event['VALUE']
  print("SENSOR_TYPE:  ", SENSOR_TYPE)
  print("VALUE: ", VALUE)
  
  new_payload=""
  
  if (SENSOR_TYPE == "HUMIDITY") and float(VALUE) > 30:
    new_payload = "ALARM"
  elif (SENSOR_TYPE == "TEMP") and float(VALUE) > 30:
    new_payload = "ALARM"
  elif (SENSOR_TYPE == "PRESSURE") and float(VALUE) > 1200:
    new_payload = "ALARM"

  print("new_payload: ", new_payload)
  
  if new_payload == "ALARM": 
    response_sns = sns.publish (
      TopicArn = 'arn:aws:sns:us-east-1:999999999999:IoT_Sensor_Notify',
      Message =  ("WARNING! SENSOR THRESHOLD BREACHED.   " + eventText)
    )
  
  response = client.publish(
          topic='sdk/test/Python',
          qos=1,
          payload=new_payload
      )
      
  print(response)
  
 
