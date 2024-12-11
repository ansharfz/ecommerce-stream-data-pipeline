import apache_beam as beam
from apache_beam.io.kafka import ReadFromKafka
from apache_beam.options.pipeline_options import PipelineOptions
from confluent_kafka import Consumer
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroDeserializer
from confluent_kafka.serialization import MessageField, SerializationContext

schema_registry_config = {
        'url' : 'http://localhost:8881'
}

schema_registry_client = SchemaRegistryClient(schema_registry_config)

with open('schema/events.avsc', encoding='utf-8') as f:
    schema_str = f.read()

avro_deserializer = AvroDeserializer(schema_registry_client, schema_str)
consumer_config = {
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'event_data_group',
    'auto.offset.reset': 'earliest'
}

TOPIC = 'event_data'
beam_options = PipelineOptions([
    '--runner=FlinkRunner',
    '--flink_master=flink-jobmanager:8081',
    '--environment_type=DOCKER'
])

with beam.Pipeline(options=beam_options) as pipeline:
    read = (
        pipeline 
            | ReadFromKafka(
                consumer_config=consumer_config,
                topics=[TOPIC],
                with_metadata=False
                )
            )
    deserialize = (
        read
            | beam.ParDo(
                lambda element: avro_deserializer(
                element.value(),
                SerializationContext(element.topic(), MessageField.VALUE)
            )
        )
    )


consumer = Consumer(consumer_config)
consumer.subscribe([TOPIC])
msg = consumer.poll(5.0)
event = avro_deserializer(msg.value(), SerializationContext(msg.topic(), MessageField.VALUE))

print(event)
