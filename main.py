from confluent_kafka import Producer
from configurations import data_producer_topic_config, data_producer_config
import pandas as pd
import json
import random
import time


def produce_data():
    producer = Producer(data_producer_config)
    dataset = pd.read_csv("credit_risk_dataset_infer.csv")

    while True:
        idx = random.randint(0, dataset.shape[0] - 1)
        sample = dataset.iloc[idx]

        producer.produce(data_producer_topic_config, key='1', value=json.dumps(sample.to_json()))

        producer.flush()
        print(f'Produced sample: {idx}')
        time.sleep(100 + random.uniform(0, 5.0))

if __name__ == "__main__":
    produce_data()