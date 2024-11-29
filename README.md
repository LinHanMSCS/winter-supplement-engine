# winter-supplement-engine

## 1. Overview
This project implements a business rules engine designed to determine eligibility and calculate the Winter Supplement benefits for clients of BC Government assistance programs. The Winter Supplement is a seasonal benefit that helps recipients cover additional expenses during the winter holiday season. The engine evaluates whether clients qualify for the supplement and calculates the appropriate benefit amount based on their assistance program and family composition.

The rules engine uses the following criteria to calculate the benefit:
- Single Person with No Dependent Children: $60 per calendar year.
- Childless Couple: $120 per calendar year.
- Single or Two-Parent Family with Dependent Children: $120 per calendar year, plus $20 for each dependent child.

The engine is designed to process client data, assess eligibility, and apply these rules to determine the total Winter Supplement amount. This system integrates with a Winter Supplement Calculator using MQTT to exchange data and trigger calculations, ensuring a seamless and efficient process for providing benefits.

## 2. Development Environment Setup

### 2.1 Prerequisites
Ensure you have the following installed:
- Python 3.x: Download and install from [python.org](https://www.python.org/downloads/).
- paho-mqtt library: To install the library, run:
    ```bash
    pip install paho-mqtt
    ```

### 2.2 Cloning the Repository
Clone the repository to your local machine:
```bash
git clone https://github.com/LinHanMSCS/winter-supplement-engine.git
cd winter-supplement-engine
```

## 3. Updating MQTT Topic ID

### 3.1 Login to Winter Supplement Calculator
Visit the Winter Supplement Calculator website: https://winter-supplement-app-d690e5-tools.apps.silver.devops.gov.bc.ca/

Use the following login credentials to access the calculator:
- User: user
- Password: r44UKbfSeIn9AZjI4Ed24xr6

### 3.2 Obtain MQTT Topic ID
After logging in the calculator will generate a unique MQTT Topic ID. Copy the generated MQTT Topic ID as you'll need it to configure the engine. Please note that refreshing the page will generate a new MQTT topic ID.

### 3.3 Update with the New MQTT Topic ID in engine.py
Open the engine.py file. Locate the following lines:
```python
INPUT_TOPIC = "BRE/calculateWinterSupplementInput/<MQTT topic ID>"  # Replace with the actual MQTT topic ID
OUTPUT_TOPIC = "BRE/calculateWinterSupplementOutput/<MQTT topic ID>"  # Replace with the actual MQTT topic ID
```
Replace <MQTT topic ID> with the actual MQTT topic ID you received from the Winter Supplement Calculator, we use 3c4c2d89-2769-40ea-ad83-23b11ea6ac47 as example.
```python
INPUT_TOPIC = "BRE/calculateWinterSupplementInput/3c4c2d89-2769-40ea-ad83-23b11ea6ac47"  # Replace with the actual MQTT topic ID
OUTPUT_TOPIC = "BRE/calculateWinterSupplementOutput/3c4c2d89-2769-40ea-ad83-23b11ea6ac47"  # Replace with the actual MQTT topic ID
```

## 4 Running the Engine

### 4.1 Running the Engine Script
Run the engine script using the following command: 
```bash
python3 engine.py
```

### 4.2 Connecting to the MQTT Broker
The engine will attempt to connect to the MQTT broker (test.mosquitto.org) and subscribe to the input topic. Once connected, it will wait for incoming messages containing the input data. The MQTT topic ID of the example below is 3c4c2d89-2769-40ea-ad83-23b11ea6ac47. You should see an output like the following when the engine successfully connects:
```css
Connecting to broker test.mosquitto.org on port 1883
Waiting for messages...
Connected to broker with result code 0
Subscribed to topic: BRE/calculateWinterSupplementInput/3c4c2d89-2769-40ea-ad83-23b11ea6ac47
```

### 4.3 Submit Data to the Winter Supplement Calculator
Go back to the Winter Supplement Calculator and fill in the necessary fields, such as the number of children, family composition, and whether the family unit is in pay for December. Click Submit to send the data to the engine.

### 4.4 Viewing the Results
The engine will process the input data and output the calculated result in the terminal. You should see output similar to the following:
```css
Message received on BRE/calculateWinterSupplementInput/3c4c2d89-2769-40ea-ad83-23b11ea6ac47: {"id": "34733e72-bb56-43a4-9a2f-bd96ecabc4f7", "numberOfChildren": 3, "familyComposition": "single", "familyUnitInPayForDecember": true}
Input data: {'id': '34733e72-bb56-43a4-9a2f-bd96ecabc4f7', 'numberOfChildren': 3, 'familyComposition': 'single', 'familyUnitInPayForDecember': True}
Output data: {'id': '34733e72-bb56-43a4-9a2f-bd96ecabc4f7', 'isEligible': True, 'baseAmount': 120.0, 'childrenAmount': 60.0, 'supplementAmount': 180.0}
Published to BRE/calculateWinterSupplementOutput/3c4c2d89-2769-40ea-ad83-23b11ea6ac47: {'id': '34733e72-bb56-43a4-9a2f-bd96ecabc4f7', 'isEligible': True, 'baseAmount': 120.0, 'childrenAmount': 60.0, 'supplementAmount': 180.0}
```
The calculated results from the engine are also displayed on the Winter Supplement Calculator web app.

You can submit different input values multiple times to verify the accuracy and reliability of the engine's calculations.

This allows you to confirm that the engine integrates seamlessly with the web app and provides accurate results.

## 5 Unit Tests

This project includes unit tests for the engine.py functionality. The tests are implemented using Python's unittest framework. To run the tests, follow the instructions below:
- Ensure that you have completed the Development Environment Setup as described earlier.
- Open a terminal and navigate to the root directory of the project.
- Run the unit tests using the following command:
    ```bash
    python3 -m unittest test_engine.py
    ```
If the tests pass, you will see an output like this:
```css
.....
----------------------------------------------------------------------
Ran 5 tests in 0.000s

OK
```

## 6 Running the Manual Input Engine

### 6.1 Description
The engine_manual_input.py script is designed for scenarios where you need to manually test the Winter Supplement calculations without relying on the Winter Supplement Calculator web application to send input data. While the script still uses MQTT services to publish results, the input data is provided directly within the script.

This allows for flexibility in testing and debugging calculations when the web application is unavailable or if you want to validate specific scenarios without external dependencies.

### 6.2 Configuring Input Data
To use the manual input engine, open the engine_manual_input.py file and locate the section where the input data is defined:
```python
input_data = {
    "id": "test123",
    "familyComposition": "single",
    "numberOfChildren": 1,
    "familyUnitInPayForDecember": True
}
```
Modify the input_data dictionary to simulate different scenarios:
- id: A unique identifier for the test case.
- numberOfChildren: The number of dependent children in the family.
- familyComposition: The family type, such as "single" or "couple".
- familyUnitInPayForDecember: A boolean indicating if the family unit is in pay for December.

### 6.3 Running the Engine Script
Once the input data is configured, run the script using the following command:
```bash
python3 engine_manual_input.py
```

### 6.4 Viewing the Results
The script processes the manual input data, calculates the Winter Supplement, and publishes the results to the MQTT output topic. The results are also displayed in the terminal. For example:
```css
Connecting to broker test.mosquitto.org on port 1883
Waiting for messages...
Connected to broker with result code 0
Subscribed to topic: BRE/calculateWinterSupplementInput/<MQTT topic ID>
Message received on BRE/calculateWinterSupplementInput/<MQTT topic ID>: {"id": "test123", "familyComposition": "single", "numberOfChildren": 1, "familyUnitInPayForDecember": true}
Input data: {'id': 'test123', 'familyComposition': 'single', 'numberOfChildren': 1, 'familyUnitInPayForDecember': True}
Output data: {'id': 'test123', 'isEligible': True, 'baseAmount': 120.0, 'childrenAmount': 20.0, 'supplementAmount': 140.0}
Published to BRE/calculateWinterSupplementOutput/<MQTT topic ID>: {'id': 'test123', 'isEligible': True, 'baseAmount': 120.0, 'childrenAmount': 20.0, 'supplementAmount': 140.0}
```