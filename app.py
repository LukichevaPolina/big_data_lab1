from configurations import data_producer_topic_config, data_producer_config, data_processor_config, data_processor_topic_config

import streamlit as st 
import json
from confluent_kafka import Consumer, Producer
import pandas as pd
from model import Predictor

#st.sidebar
st.set_page_config(
    page_title="Real-Time Data Dashboard",
    layout="wide",
)

if "price" not in st.session_state:
    st.session_state["price"] = []

conf_consume = {**data_producer_config, 'group.id': 'data_processors'}
consumer = Consumer(conf_consume)
consumer.subscribe([data_producer_topic_config])

producer = Producer(data_processor_config)

while True:
    msg = consumer.poll(1000)
    predictor = Predictor()

    if msg is not None:
        stock_data = json.loads(msg.value().decode('utf-8'))
        stock_data = json.loads(stock_data)
        prediction = predictor.predict(stock_data)

        result = {'age': stock_data['person_age'],
                  'loan_amnt': stock_data['loan_amnt'],
                  'prediction': int(prediction[0])}
        producer.produce(data_processor_topic_config, key='1', value=json.dumps(result))
        producer.flush()
        # st.session_state["price"].append(stock_data['price'])
    
    # chart_holder.line_chart(st.session_state["price"])

