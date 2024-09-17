import os
from confluent_kafka.admin import (AdminClient, NewTopic, 
                                   ConfigResource)

class kafka_admin:
    def __init__(self):
        config = {
            # User-specific properties that you must set
            'bootstrap.servers': f'localhost:{os.environ.get("Plaintext_Ports")}',
        }

        # Create Admin client
        self.admin = AdminClient(config)
        self.max_msg_k = 50


    def topic_exists(self,topic):
        metadata = self.admin.list_topics(topic)
        for t in iter(metadata.topics.values()):
            if  t.topic == topic:
                return True
        return False

    def check_create_topic(self, topic_name):
        if not self.topic_exists(topic_name):
            return self._create_topic(topic_name)
        return True

    # create new topic and return results dictionary
    def _create_topic(self, topic):
        new_topic = NewTopic(topic, num_partitions=6, replication_factor=3) 
        result_dict = self.admin.create_topics([new_topic])
        for topic, future in result_dict.items():
            try:
                future.result()  # The result itself is None
                print("Topic {} created".format(topic))
                return True
            except Exception as e:
                print("Failed to create topic {}: {}".format(topic, e))
                return False



Kafa_Admin = kafka_admin()