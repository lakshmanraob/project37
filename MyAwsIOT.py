from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient

class AwsUpdate:
    def __init__(self, certificatePath, topic):
        CERTIFICATE_PATH = certificatePath
        # '/Users/labattula/Documents/lakshman/certificate/'

        CA_PATH = CERTIFICATE_PATH + "rootca.pem"
        PRIVATE_KEY = CERTIFICATE_PATH + "00faeb520f-private.pem.key"
        CERTIFICATE = CERTIFICATE_PATH + "00faeb520f-certificate.pem.crt"

        self.SUBSCRIBE_TOPIC_NAME = topic

        # SUBSCRIBE_TOPIC_NAME = "myPi/Info"
        # SUBSCRIBE_EMOTION = "myPI/emotion"

        self.myMQTTClient = AWSIoTMQTTClient("ia2xx4li8e6ncyj")
        self.myMQTTClient.configureEndpoint("a2xx4li8e6ncyj.iot.us-east-1.amazonaws.com", 8883)
        self.myMQTTClient.configureCredentials(CA_PATH, PRIVATE_KEY, CERTIFICATE)
        self.myMQTTClient.configureOfflinePublishQueueing(-1)
        self.myMQTTClient.configureDrainingFrequency(2)
        self.myMQTTClient.configureConnectDisconnectTimeout(10)
        self.myMQTTClient.configureMQTTOperationTimeout(5)

        self.myMQTTClient.connect()

    def publish(self, payload, topic):
        if topic:
            self.myMQTTClient.publish(topic, payload, 0)
        else:
            self.myMQTTClient.publish(self.SUBSCRIBE_TOPIC_NAME, payload, 0)