import logging

import apache_beam as beam
from apache_beam.io import WriteToText
from apache_beam.io.kafka import ReadFromKafka
from apache_beam.options.pipeline_options import PipelineOptions
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroDeserializer
from confluent_kafka.serialization import MessageField, SerializationContext

schema_registry_config = {
        'url' : 'http://schema-registry:8081'
}

schema_registry_client = SchemaRegistryClient(schema_registry_config)

with open('schema/events.avsc', encoding='utf-8') as f:
    schema_str = f.read()

avro_deserializer = AvroDeserializer(schema_registry_client, schema_str)

consumer_config = {
    'bootstrap.servers': 'kafka-cluster-1:9092',
    'group.id': 'event_data_group',
    'auto.offset.reset': 'earliest'
}

TOPIC = 'event_data'

beam_options = PipelineOptions([
    '--runner=PortableRunner',
    '--flink_master=flink-jobmanager:8081',
    '--environment_type=EXTERNAL',
    '--environment_config=beam-worker-pool:50000',
    '--job_endpoint=beam-job-server:8099',
    '--temp_location=/tmp/temp',
    '--staging_location=/tmp/staging'
])

with beam.Pipeline(options=beam_options) as pipeline:
    _ = (pipeline
        | 'Create words' >> beam.Create(['to be or not to be'])
        | 'Split words' >> beam.FlatMap(lambda words: words.split(' '))
        | 'Write to file' >> WriteToText('test.txt')
    )

    pipeline.run().wait_until_finish()
    # data = (pipeline 
    #     | "Read data from Kafka" >> ReadFromKafka(
    #         consumer_config=consumer_config,
    #         topics=[TOPIC],
    #         with_metadata=False
    #     )
    #     | "Deserialize data from Avro format to Dictionary" >> beam.ParDo(
    #             lambda element: avro_deserializer(
    #                 element.value(),
    #                 SerializationContext(element.topic(), MessageField.VALUE)
    #             )
    #     )
    #     | 'Writing to stdout' >> beam.Map(logging.info)
    # )

    # result = pipeline.run().wait_until_finish()


# consumer = Consumer(consumer_config)
# consumer.subscribe([TOPIC])
# msg = consumer.poll(5.0)
# event = avro_deserializer(msg.value(), SerializationContext(msg.topic(), MessageField.VALUE))

# print(event)
