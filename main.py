from confluent_kafka import Producer
import pandas as pd
import json
import random
import time

bootstrap_servers = 'localhost:9095'
topic = 'stock_topic'

conf = {'bootstrap.servers': bootstrap_servers}

def produce_data():
    producer = Producer(conf)
    dataset = pd.read_csv("credit_risk_dataset_infer.csv")

    while True:
        idx = random.randint(0, dataset.shape[0] - 1)
        sample = dataset.iloc[idx]

        producer.produce(topic, key='1', value=json.dumps(sample.to_json()))

        producer.flush()
        print(f'Produced sample: {idx}')
        time.sleep(10 + random.uniform(0, 5.0))

if __name__ == "__main__":
    produce_data()