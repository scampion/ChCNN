FROM tensorflow/tensorflow
RUN mkdir /code 
ADD . /code 
WORKDIR /code
RUN pip install kafka-python
RUN pip install -r requirements.txt
RUN pip install keras
CMD python run.py
