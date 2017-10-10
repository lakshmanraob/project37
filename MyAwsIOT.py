from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import time


class AwsUpdate:
    def __init__(self):
        topic = 'myPi/Info'
        # CERTIFICATE_PATH = '/Users/labattula/Documents/lakshman/certificate/'
        CERTIFICATE_PATH = "/Users/labattula/Documents/lakshman/Personal Folders/pythonWork/project37/awsiotcerts/"

        CA_PATH = CERTIFICATE_PATH + "rootCA.pem"
        PRIVATE_KEY = CERTIFICATE_PATH + "eabf0b3d86-certificate.pem.crt"
        CERTIFICATE = CERTIFICATE_PATH + "eabf0b3d86-private.pem.key"

        self.SUBSCRIBE_TOPIC_NAME = topic

        # SUBSCRIBE_TOPIC_NAME = "myPi/Info"
        # SUBSCRIBE_EMOTION = "myPI/emotion"
        clientId = "basicPubSub"
        host = "a2xx4li8e6ncyj.iot.us-east-1.amazonaws.com"

        # self.myMQTTClient = AWSIoTMQTTClient("ia2xx4li8e6ncyj")
        # self.myMQTTClient.configureEndpoint("a2xx4li8e6ncyj.iot.us-east-1.amazonaws.com", 8883)
        # self.myMQTTClient.configureCredentials(CA_PATH, PRIVATE_KEY, CERTIFICATE)
        # self.myMQTTClient.configureOfflinePublishQueueing(-1)
        # self.myMQTTClient.configureDrainingFrequency(2)
        # self.myMQTTClient.configureConnectDisconnectTimeout(10)
        # self.myMQTTClient.configureMQTTOperationTimeout(5)

        print(CA_PATH)
        print(PRIVATE_KEY)
        print(CERTIFICATE)

        self.myAWSIoTMQTTClient = AWSIoTMQTTClient(clientId)
        self.myAWSIoTMQTTClient.configureEndpoint(host, 8883)
        self.myAWSIoTMQTTClient.configureCredentials(CA_PATH, PRIVATE_KEY, CERTIFICATE)

        # AWSIoTMQTTClient connection configuration
        self.myAWSIoTMQTTClient.configureAutoReconnectBackoffTime(1, 32, 20)
        self.myAWSIoTMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
        self.myAWSIoTMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
        self.myAWSIoTMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
        self.myAWSIoTMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec

        print("connecting..")
        # Connect and subscribe to AWS IoT
        self.myAWSIoTMQTTClient.connect()


        # self.myAWSIoTMQTTClient.connect()
        print("connected")

    def disconnect(self):
        if self.myAWSIoTMQTTClient:
            self.myAWSIoTMQTTClient.disconnect()
        else:
            print("disconnect failure")

    def publish(self, payload, topic):
        if topic:
            self.myAWSIoTMQTTClient.publish(topic, payload, 0)
        else:
            self.myAWSIoTMQTTClient.publish(self.SUBSCRIBE_TOPIC_NAME, payload, 0)


if __name__ == "__main__":
    awsupdate = AwsUpdate()
    update = 0
    data = {}
    while True:
        data['face_index'] = update
        print(data)
        # awsupdate.publish(str(data), "faces", 1)
        awsupdate.publish("faces", "New Message " + str(data), 1)
        print("published    ")
        update += 1
        time.sleep(1)
        data = {}
        if update == 5:
            awsupdate.disconnect()
            break
