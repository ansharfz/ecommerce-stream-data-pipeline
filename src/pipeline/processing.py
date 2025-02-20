from pyflink.table import EnvironmentSettings, TableEnvironment

env_settings = EnvironmentSettings.in_streaming_mode()
table_env = TableEnvironment.create(env_settings)
table_env.get_config().set(
    "pipeline.jars", 
    "file:///opt/flink/jars/flink-connector-kafka-3.2.0-1.19.jar;\
    file:///opt/flink/jars/kafka-schema-registry-client-7.7.1.jar;\
    file:///opt/flink/jars/kafka-clients-3.7.1.jar;\
    file:///opt/flink/jars/avro-1.11.4.jar;\
    file:///opt/flink/jars/flink-avro-1.19.1.jar;\
    file:///opt/flink/jars/flink-avro-confluent-registry-1.19.1.jar;\
    file:///opt/flink/jars/jackson-core-2.16.1.jar;\
    file:///opt/flink/jars/jackson-databind-2.16.1.jar;\
    file:///opt/flink/jars/jackson-annotations-2.16.1.jar;\
    file:///opt/flink/jars/guava-33.1.0-jre.jar;\
    file:///opt/flink/jars/flink-connector-jdbc-3.2.0-1.19.jar;\
    file:///opt/flink/jars/postgresql-42.7.5.jar"
)

TOPIC = 'cart_events'

source = f"""
    CREATE TABLE cart_events_stream (
    id STRING,
    event_time INTEGER,
    event_type STRING,
    product_id STRING,
    category_id STRING,
    category_code STRING,
    brand STRING,
    price FLOAT,
    user_id FLOAT,
    user_session STRING

) WITH (
    
    'connector' = 'kafka',
    'topic' = '{TOPIC}',
    'properties.bootstrap.servers' = 'kafka-cluster-1:9092',
    'properties.group.id' = 'group1',
    
    'key.format' = 'raw',
    'key.fields' = 'id',
    
    'value.format' = 'avro-confluent',
    'value.avro-confluent.url' = 'http://schema-registry:8881'
);
    """

sink = """
CREATE TABLE cart_events (
    id STRING,
    event_time INTEGER,
    event_type STRING,
    product_id STRING,
    category_id STRING,
    category_code STRING,
    brand STRING,
    price FLOAT,
    user_id FLOAT,
    user_session STRING

) WITH (
   'connector' = 'jdbc',
   'url' = 'jdbc:postgresql://postgres-db:5432/events_db',
   'username' = 'user',
   'password' = 'password',
   'table-name' = 'cart_events'
);
"""

insert = """
    INSERT INTO cart_events
    SELECT * FROM cart_events_stream;
"""

table_env.execute_sql(source)
table_env.execute_sql(sink)
table_env.execute_sql(insert)
