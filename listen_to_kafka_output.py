from kafka import KafkaConsumer
consumer = KafkaConsumer('output', bootstrap_servers=['localhost:9092'])
for msg in consumer:
    print(msg, '\n')