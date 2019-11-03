import hashlib
import json, time

from kafka import KafkaConsumer, KafkaProducer


class Model:

    def __init__(self, version, bootstrap_servers='kafka:9092'):
        self.consumer = KafkaConsumer('requests', group_id=self.__class__.__name__, bootstrap_servers=bootstrap_servers)
        self.producer = KafkaProducer(bootstrap_servers=bootstrap_servers)
        self.version = version

    def predict(self, message):
        pass

    def run(self):
        for request in self.consumer:
            s = time.time()
            results = self.predict(request.value)
            msg = {'request': str(request.value),
                   'response': {'name': self.__class__.__name__,
                                'version': self.version,
                                'results': results.tolist()
                                }
                   }
            self.producer.send('responses', json.dumps(msg).encode())


def md5(files):
    m = hashlib.md5()
    for fl in files:
        with open(fl, 'rb') as f:
            m.update(f.read())
    return m.hexdigest()
