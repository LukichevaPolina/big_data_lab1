from configurations import data_processor_config, data_processor_topic_config

import streamlit as st 
import json
from confluent_kafka import Consumer, Producer
import pandas as pd
from model import Predictor
from matplotlib import pyplot as plt


#st.sidebar
st.set_page_config(
    page_title="Real-Time Data Dashboard",
    layout="wide",
)

if "price" not in st.session_state:
    st.session_state["price"] = []

conf_consume = {**data_processor_config, 'group.id': 'data_processors'}
consumer = Consumer(conf_consume)
consumer.subscribe([data_processor_topic_config])
hists = st.empty()

while True:
    msg = consumer.poll(1000)
    predictor = Predictor()

    if msg is not None:
        stock_data = json.loads(msg.value().decode('utf-8'))
        
        st.session_state["price"].append(stock_data)

    
    collected_data = pd.DataFrame(st.session_state["price"])
    fig, ax = plt.subplots(figsize=(5, 2))
    collected_data.hist(ax=ax, alpha=0.5)
    ax.set_xlabel('Price in dollars')
    hists.pyplot(fig)

