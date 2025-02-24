import csv
from datetime import datetime
from uuid import uuid4

from confluent_kafka import Producer
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroSerializer
from confluent_kafka.serialization import (
    MessageField,
    SerializationContext,
    StringSerializer,
)


def to_miliseconds(date_str):
    date_format = "%Y-%m-%d %H:%M:%S %Z"
    dt = datetime.strptime(date_str, date_format)
    miliseconds = int(dt.timestamp() * 1000)
    return miliseconds

def stream_data():

    producer_conf = {
        'bootstrap.servers' : 'kafka-cluster-1:9092',
        'allow.auto.create.topics' : True
    }

    producer = Producer(producer_conf)

    schema_registry_conf = {
        'url' : 'http://schema-registry:8081'
    }
    schema_registry_client = SchemaRegistryClient(schema_registry_conf)

    string_serializer = StringSerializer('utf_8')

    with open('/schema/events.avsc', encoding='utf-8') as f:
        schema_str = f.read()

    avro_serializer = AvroSerializer(schema_registry_client, schema_str)

    TOPIC = 'cart_events'
    n_data = 20
    with open('/data/events.csv', 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        fieldnames = next(reader)
        reader = csv.DictReader(f, fieldnames)
        for n in range(n_data):
            data = next(reader)
            data['event_time'] = to_miliseconds(data['event_time'])
            producer.produce(topic=TOPIC,
                             key=string_serializer(str(uuid4())),
                             value=avro_serializer(
                                data, SerializationContext(TOPIC, MessageField.VALUE)
                                )
                            )
            producer.flush()

if __name__ == '__main__':
    stream_data()
