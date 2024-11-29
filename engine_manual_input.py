import json
import paho.mqtt.client as mqtt

# MQTT Broker details
BROKER = "test.mosquitto.org"
PORT = 1883
INPUT_TOPIC = "BRE/calculateWinterSupplementInput/<MQTT topic ID>"  # Replace with the actual MQTT topic ID
OUTPUT_TOPIC = "BRE/calculateWinterSupplementOutput/<MQTT topic ID>"  # Replace with the actual MQTT topic ID

def calculate_supplement(data):
    """
    Calculate the Winter Supplement based on input data.
    """
    id_ = data["id"]
    family_composition = data["familyComposition"]
    number_of_children = data["numberOfChildren"]
    family_in_pay = data["familyUnitInPayForDecember"]

    # Base eligibility
    is_eligible = family_in_pay

    # Initialize amounts
    base_amount = 0.0
    children_amount = 0.0
    supplement_amount = 0.0

    if is_eligible:
        # Calculate base amount
        if number_of_children > 0:
            base_amount = 120.0
        elif family_composition == "single":
            base_amount = 60.0
        elif family_composition == "couple":
            base_amount = 120.0

        # Additional amount for children
        children_amount = number_of_children * 20.0

        # Total amount
        supplement_amount = base_amount + children_amount

    # Output result
    return {
        "id": id_,
        "isEligible": is_eligible,
        "baseAmount": base_amount,
        "childrenAmount": children_amount,
        "supplementAmount": supplement_amount,
    }

# MQTT Callbacks
def on_connect(client, userdata, flags, rc):
    """
    Callback triggered when the MQTT client connects to the broker.
    """
    print(f"Connected to broker with result code {rc}")
    if rc == 0:
        # Subscribe to the input topic to receive messages
        client.subscribe(INPUT_TOPIC)
        print(f"Subscribed to topic: {INPUT_TOPIC}")

        # Send input data manually due to issues with the Winter Supplement web app
        # This is a workaround to ensure the system can be tested with predefined input
        input_data = {
            "id": "test123",
            "familyComposition": "single",
            "numberOfChildren": 1,
            "familyUnitInPayForDecember": True
        }
        # Publish the input data to the input topic to simulate app functionality
        client.publish(INPUT_TOPIC, json.dumps(input_data))

    else:
        print(f"Failed to connect with result code {rc}")

def on_message(client, userdata, msg):
    """
    Callback triggered when a message is received on a subscribed topic.
    """
    print(f"Message received on {msg.topic}: {msg.payload.decode()}")
    try:
        # Decode the JSON payload from the message
        input_data = json.loads(msg.payload.decode())
        print(f"Input data: {input_data}")  # Log input data for debugging

        # Calculate supplement based on input data
        output_data = calculate_supplement(input_data)

        # Log output data for debugging
        print(f"Output data: {output_data}")

        # Publish the calculated result to the output topic
        client.publish(OUTPUT_TOPIC, json.dumps(output_data))
        print(f"Published to {OUTPUT_TOPIC}: {output_data}")
        print()
    except Exception as e:
        # Log any errors encountered during processing
        print(f"Error processing message: {e}")

# Main entry point
if __name__ == "__main__":
    # Start MQTT client
    client = mqtt.Client(client_id=None, clean_session=True)
    
    client.on_connect = on_connect
    client.on_message = on_message

    # Connect to the MQTT broker
    try:
        client.connect(BROKER, PORT, 60)
        print(f"Connecting to broker {BROKER} on port {PORT}")
        
        # Start the network loop in a separate thread
        client.loop_start()

        # Keep the program running indefinitely, unless interrupted
        print("Waiting for messages...")
        try:
            while True:
                pass  # Prevent program termination
        except KeyboardInterrupt:
            # Handle graceful shutdown on manual interruption
            print("Disconnected")
            client.loop_stop()  # Stop the loop gracefully

    except Exception as e:
        # Handle connection errors
        print(f"Failed to connect to broker: {e}")
