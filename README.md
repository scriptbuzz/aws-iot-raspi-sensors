# AWS IoT Raspberry Pi Sensors

In this project, I use the AWS IoT Core service to monitor and control a Raspberry Pi over the internet based on readings from environmental and motion sensors built into the Raspberry Pi Sense HAT. 

The Raspberry Pi has built-in support for WiFi, which allows it to be connected over the internet to AWS services. The Sense HAT features an array of sensors including a gyroscope, accelerometer, magnetometer, temperature sensor, barometric pressure sensor, and humidity sensor. Additional outward sensors can be attached to the Raspberry Pi as needed.

The values of sensor readings are passed from the Raspberry Pi via an MQTT topic subscribed to by the AWS IoT Core service. An AWS IoT Rule routes the MQTT topic values to Amazon SNS, DynamoDB, and AWS Lambda. Lambda evaluates the data and sends back control commands to the MQTT topic when a sensor value goes above or below a certain threshold set by the developer.

The payload contains the following data items:
* `SENSOR_TYPE`: The type of sensor (e.g., TEMP, HUMIDITY, PRESSURE)
* `VALUE`: The recorded sensor reading
* `NOW`: The datetime stamp of the reading
* `NODE_ID`: A unique IoT device identifier/serial number

## Project Video Demo
To see the project in action, watch this YouTube video:
[https://www.youtube.com/watch?v=f7IWtVbQ5dQ](https://www.youtube.com/watch?v=f7IWtVbQ5dQ)

## AWS Architecture
Please refer to the AWS architecture diagram included at the bottom of this page.

## Project Components
* [Raspberry Pi](https://www.raspberrypi.org/)
* [Raspberry Pi Sense HAT](https://www.raspberrypi.org/products/sense-hat/)
* [AWS Account](https://portal.aws.amazon.com/billing/signup?type=enterprise#/start)
* WiFi network with internet access

## Prerequisites
1. **Python**: Python 3.x is highly recommended.
2. **Sense HAT Library**: You will need the Sense HAT library installed on your Raspberry Pi:
   ```bash
   sudo apt-get update
   sudo apt-get install sense-hat
   ```
3. **AWS IoT Python SDK**: Must be installed on your Raspberry Pi.

## File Descriptions
* `aws-iot-test01.py`: Demonstrates local Sense HAT behavior, fetching and printing the sensor readings, and outputting local LED matrix messages.
* `basicPubSub.py`: The main script that connects the Raspberry Pi to AWS IoT using your certificates, publishes sensor data, and listens (subscribes) for returning command actions.
* `IoTLambdaSensorResponse.py`: The AWS Lambda code to evaluate IoT Core data, trigger SNS notifications on threshold breaches, and publish control commands back to the device.

## Setup & Configuration

### AWS Account Setup
1. **Lambda Function:** Create a Lambda function in your AWS account using `IoTLambdaSensorResponse.py` as your baseline code.
2. **Configuration:** Customize the code with your account-specific resource properties:
   - Ensure the `TopicArn` points to your SNS Topic ARN.
   - Update your default region in the `boto3.client` calls if you are not using `us-east-1`.
3. **IAM Permissions:** Your Lambda's assigned IAM Execution Role will need permissions to:
   - Publish to Amazon SNS (`sns:Publish`)
   - Publish to AWS IoT Core (`iot:Publish`)

### Raspberry Pi Setup
1. Follow the instructions on the AWS guide to install the AWS IoT Python SDK v1 on your Raspberry Pi:
   [AWS IoT SDK Guide](https://docs.aws.amazon.com/greengrass/latest/developerguide/IoT-SDK.html)

2. Register a "Thing" in your AWS IoT Core console and explicitly download your:
   - Certificate (`.pem.crt`)
   - Private Key (`-private.pem.key`)
   - Root CA

3. Use the `basicPubSub.py` script provided in this repository (which extends the SDK's basic pub/sub example) alongside your retrieved AWS IoT endpoint and certificates.

## Usage

You can test local sensor readings first with:
```bash
python3 aws-iot-test01.py
```

To run the full AWS IoT connection script, you will need to start `basicPubSub.py` utilizing the arguments required by the AWS IoT SDK:
```bash
python3 basicPubSub.py -e <your-aws-iot-endpoint.amazonaws.com> -r <root-CA-file> -c <certificate-file> -k <private-key-file>
```

---
![AWS Architecture Diagram](mbx-aws-iot-raspi-sensors.jpg)
