from confluent_kafka import Producer
import os
import base64
from PIL import Image
import io
import logging

# Logging configuration
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Kafka configuration
conf = {
    'bootstrap.servers': '3.83.11.185:9092',  # Kafka broker address
    'client.id': 'image-producer',
    'message.max.bytes': 10485760,             # Maksimum ukuran pesan 10 MB
    'queue.buffering.max.messages': 100000    # Buffering maksimum untuk antrean pesan
}
producer = Producer(conf)

# Directory containing images
image_directory = '/home/ubuntu/datasets/dataset/train'

# Kafka topic
topic = 'image-stream'

def image_to_base64(image_path, max_size=1048576):
    """Convert image to base64 to be sent through Kafka"""
    try:
        with open(image_path, 'rb') as image_file:
            image_data = image_file.read()

            # Compress image if it exceeds max size
            if len(image_data) > max_size:
                image = Image.open(io.BytesIO(image_data))
                buffer = io.BytesIO()
                image.save(buffer, format='JPEG', quality=85)  # Compress the image
                image_data = buffer.getvalue()

            return base64.b64encode(image_data).decode('utf-8')
    except Exception as e:
        logging.error(f"Failed to process image {image_path}: {e}")
        return None


def on_delivery(err, msg):
    """Callback function to handle message delivery status"""
    if err is not None:
        logging.error(f"Message delivery failed: {err}")
    else:
        logging.info(f"Message delivered to {msg.topic()} [{msg.partition()}]")


# Produce images to Kafka topic
for subdir, dirs, files in os.walk(image_directory):
    for file in files:
        if file.endswith(('png', 'jpg', 'jpeg')):
            image_path = os.path.join(subdir, file)
            base64_image = image_to_base64(image_path)
            if base64_image:
                try:
                    producer.produce(topic, base64_image, callback=on_delivery)
                except Exception as e:
                    logging.error(f"Failed to produce message for {file}: {e}")

producer.flush()  # Ensure all messages are sent
logging.info("All images sent to Kafka topic.")
