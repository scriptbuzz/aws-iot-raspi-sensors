# aws-iot-raspi-sensors

  This project uses the AWS IoT Core service to monitor and control a Raspberry Pi over the internet based on readings of environmental and motion sensors. 

- To see the project in action, watch this YouTube video
-- https://www.youtube.com/watch?v=f7IWtVbQ5dQ

- Refer to the AWS architecture diagram at the end of this page. 

-  Project Components:
   -- Raspberry Pi - https://www.raspberrypi.org/
   -- Raspberry Pi Sense Hat - https://www.raspberrypi.org/products/sense-hat/
   -- AWS Account
   -- Wifi network + internet access

# aws account setup

- Create a Lambda function in your account using this code as basis. Customize as needed

  https://github.com/scriptbuzz/aws-iot-raspi-sensors/blob/master/IoTLambdaSensorResponse.py

# raspberry pi setup

- Follow the instructions on the AWS guide to install the AWS IoT Python SDK on your Raspberry Pi

  https://docs.aws.amazon.com/greengrass/latest/developerguide/IoT-SDK.html


- The AWS IoT SDK creates a file basicPubSub.py. Update this file based on my code bekow.

  https://github.com/scriptbuzz/aws-iot-raspi-sensors/blob/master/basicPubSub.py

- Create and run the following file

  https://github.com/scriptbuzz/aws-iot-raspi-sensors/blob/master/aws-iot-test01.py

# aws arcbitecture diagram 
  ![GitHub Logo](mbx-aws-iot-raspi-sensors.jpg)
