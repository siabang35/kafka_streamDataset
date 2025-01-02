from confluent_kafka import Consumer
import base64
from io import BytesIO
import matplotlib.pyplot as plt
from PIL import Image
import logging

# Logging configuration
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Kafka configuration
conf = {
    'bootstrap.servers': '3.83.11.185:9092',  # Kafka broker address
    'group.id': 'image-consumer-group',
    'auto.offset.reset': 'earliest'            # Start consuming from the earliest message
}
consumer = Consumer(conf)

# Kafka topic
topic = 'image-stream'

# Subscribe to the topic
consumer.subscribe([topic])

def display_image_from_base64(base64_str):
    """Convert base64 string to image and display it using matplotlib"""
    try:
        image_data = base64.b64decode(base64_str)
        image = Image.open(BytesIO(image_data))
        plt.imshow(image)
        plt.axis('off')  # Hide axis
        plt.show()
    except Exception as e:
        logging.error(f"Failed to decode or display image: {e}")


# Consume and visualize images
try:
    batch_size = 5
    batch_images = []

    while True:
        msg = consumer.poll(timeout=1.0)  # Adjust timeout as needed
        if msg is None:
            continue
        if msg.error():
            logging.error(f"Consumer error: {msg.error()}")
            continue

        # Message containing base64 image data
        base64_image = msg.value().decode('utf-8')
        batch_images.append(base64_image)

        if len(batch_images) >= batch_size:
            for image_base64 in batch_images:
                display_image_from_base64(image_base64)
            batch_images.clear()

except KeyboardInterrupt:
    logging.info("Consumer stopped")

finally:
    consumer.close()
