from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroDeserializer
from pyflink.common import Types, WatermarkStrategy
from pyflink.datastream import StreamExecutionEnvironment
from pyflink.datastream.connectors import KafkaSource
from pyflink.datastream.connectors.kafka import KafkaOffsetsInitializer, KafkaSource

schema_registry_config = {
        'url' : 'http://schema-registry:8881'
}

schema_registry_client = SchemaRegistryClient(schema_registry_config)

with open('/schema/events.avsc', encoding='utf-8') as f:
    schema_str = f.read()

avro_deserializer = AvroDeserializer(schema_registry_client, schema_str)

kafka_config = {
    'bootstrap.servers': 'kafka-cluster-1:9092',
    'group.id': 'event_data_group'
}

TOPIC = 'event_data'

env = StreamExecutionEnvironment.get_execution_environment()

env.add_jars('file:///opt/flink/lib/flink-sql-connector-kafka-3.2.0-1.19.jar')
