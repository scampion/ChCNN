import json
import hashlib
import time

import numpy as np
from kafka import KafkaConsumer, KafkaProducer

from data_utils import Data

from keras.models import model_from_json

m = hashlib.md5()

with open('model.json', 'r') as f:
    model = model_from_json(f.read())
    model.load_weights("model.h5")

m.update(open('model.json', 'r').read().encode())
m.update(open('model.h5', 'rb').read())
md5 = m.hexdigest()
print(md5)

config = json.load(open("./config.json"))
validation_data = Data(data_source=config["data"]["validation_data_source"],
                       alphabet=config["data"]["alphabet"],
                       input_size=config["data"]["input_size"],
                       num_of_classes=config["data"]["num_of_classes"])

consumer = KafkaConsumer('realtime',  group_id='chcnn', bootstrap_servers=['localhost:9092'])
producer = KafkaProducer(bootstrap_servers='localhost:9092')

for message in consumer:
    s = time.time()
    data = validation_data.str_to_indexes(str(message.value))
    result = model.predict([[data]])
    print("score: %0.3f | msg: %s | time: %0.3fsec" % (float(result[0][6]), str(message.value)[:60], time.time() - s))
    producer.send('results', json.dumps({'msg': str(message.value),
                                          'model': {'name': 'chcnn',
                                                    'version': md5,
                                                    'result': float(result[0][6])}
                                          }).encode())
