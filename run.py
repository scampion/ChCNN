import json

import numpy as np
from keras.models import model_from_json

from data_utils import Data
from filter import Model, md5

np.set_printoptions(precision=2)

class ChCNN(Model):
    config = json.load(open("./config.json"))
    validation_data = Data(data_source=config["data"]["validation_data_source"],
                           alphabet=config["data"]["alphabet"],
                           input_size=config["data"]["input_size"],
                           num_of_classes=config["data"]["num_of_classes"])

    with open('model.json', 'r') as f:
        model = model_from_json(f.read())
        model.load_weights("model.h5")

    def predict(self, message):
        data = self.validation_data.str_to_indexes(message.decode())
        a = self.model.predict([[data]])
        self.log(message, a)
        return a

    @staticmethod
    def log(message, a):
        print(["{:0.2f}".format(round(x, 2)) for x in a[0].tolist()], message[0:150].decode().replace('\n', ' '))


if __name__ == '__main__':
    version = md5(['model.json', 'model.h5'])
    ChCNN(version).run()
