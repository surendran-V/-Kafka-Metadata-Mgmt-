from flask import Flask, jsonify, request
from uuid import uuid4
from datetime import datetime

app = Flask(__name__)


import json
import atexit


data_file_path = "data_storage.json"

def load_data_from_file():
    global data_storage
    try:
        with open(data_file_path, "r") as file:
            data_storage = json.load(file)
    except FileNotFoundError:
        # If the file doesn't exist, initialize data_storage with an empty structure
        initialize_data_storage()
    except json.JSONDecodeError:
        # If the file exists but contains invalid JSON, initialize data_storage
        initialize_data_storage()

def initialize_data_storage():
    global data_storage
    data_storage = {
        "RegisterBrokerRecords": {
            "records": [],
            "timestamp": ""
        },
        "TopicRecords": {
            "records": [],
            "timestamp": ""
        },
        "PartitionRecords": {
            "records": [],
            "timestamp": ""
        },
        "ProducerIdsRecords": {
            "records": [],
            "timestamp": ""
        },
        "BrokerRegistrationChangeRecords": {
            "records": [],
            "timestamp": ""
        }
    }
    save_data_to_file()


def save_data_to_file():
    try:
        with open(data_file_path, "w") as file:
            global data_storage
            print(data_storage)
            json.dump(data_storage,file)
    except Exception as e:
        print(f"Error saving data to file: {e}")



load_data_from_file()


@app.route('/register-broker', methods=['POST'])
def create_register_broker_record():
    new_record = request.json
    new_record['internalUUID'] = str(uuid4)
    new_record['epoch'] = 0
    new_record['brokerStatus'] = "ALIVE"
    new_record['last_offset'] = datetime.utcnow().isoformat()
    data_storage['RegisterBrokerRecords']['records'].append(new_record)
    save_data_to_file() 
    return jsonify({'message': 'Record created successfully'}), 201

@app.route('/register-broker', methods=['GET'])
def get_register_broker_records():
    return jsonify(data_storage['RegisterBrokerRecords']['records']), 200

@app.route('/register-broker/<string:record_id>', methods=['GET'])
def get_register_broker_record(record_id):
    for record in data_storage['RegisterBrokerRecords']['records']:
        if record['brokerId'] == record_id:
            return jsonify(record), 200
    return jsonify({'message': 'Record not found'}), 404
    
    
    
@app.route('/register-broker/<int:record_id>', methods=['DELETE'])
def delete_register_broker_record(record_id):
    for index, record in enumerate(data_storage['RegisterBrokerRecords']['records']):
        if record['brokerId'] == record_id:
            record['brokerStatus'] = "CLOSED"
            del data_storage['RegisterBrokerRecords']['records'][index]
            save_data_to_file() 
            return jsonify({'message': 'Record deleted successfully'}), 200
    return jsonify({'message': 'Record not found'}), 404


@app.route('/register-broker-change', methods=['POST'])
def register_broker_change():
    updated_broker_data = request.json
    broker_id = updated_broker_data.get('brokerId')
    
    for record in data_storage['RegisterBrokerRecords']['records']:
        if record.get('brokerId') == broker_id:
            for key, value in updated_broker_data.items():
                if key != 'brokerId':
                    record[key] = value
            record['last_offset'] = datetime.utcnow().isoformat()
            record['epoch'] += 1
            save_data_to_file() 
            return jsonify({'message': 'Broker information updated successfully'}), 200
            


@app.route('/metadata-fetch-by-id/<int:broker_id>', methods=['GET'])
def metadata_fetch_by_id(broker_id):
    # Look for the broker ID in your data storage
    for record in data_storage['RegisterBrokerRecords']['records']:
        if record.get('brokerId') == broker_id:
            # If found, return the timestamp or relevant information
            return jsonify({'last_updated': record.get('last_offset')})
    
    # If the broker ID is not found
    return jsonify({'message': 'Broker ID not found'}), 404
    
    
@app.route('/register-producer', methods=['POST'])
def register_producer():
    new_producer = request.json
    required_fields = ['brokerId', 'brokerEpoch', 'producerId']

    if all(field in new_producer for field in required_fields):
        producer_record = {
            'brokerId': new_producer['brokerId'],
            'brokerEpoch': new_producer['brokerEpoch'],
            'producerId': new_producer['producerId'],
            'last_offset': datetime.utcnow().isoformat()
        }

        data_storage['ProducerIdsRecords']['records'].append(producer_record)
        save_data_to_file()

        return jsonify({'message': 'Producer registered successfully'}), 201
    else:
        return jsonify({'message': 'Missing fields in request'}), 400
    
@app.route('/create-topic', methods=['POST'])
def create_topic():
    new_topic = request.json
    required_fields = ['name']

    if 'name' in new_topic:
        topic_record = {
            'topicUUID': str(uuid4()),  # Generating a UUID for the topic
            'name': new_topic['name'],
            'last_offset': datetime.utcnow().isoformat()
        }

        data_storage['TopicRecords']['records'].append(topic_record)
        save_data_to_file()

        return jsonify({'message': 'Topic created successfully', 'topicUUID': topic_record['topicUUID']}), 201
    else:
        return jsonify({'message': 'Missing topic name in request'}), 400


@app.route('/get-topic/<string:topic_name>', methods=['GET'])
def get_topic_by_name(topic_name):
    matching_topics = [
        topic for topic in data_storage['TopicRecords']['records']
        if topic['name'] == topic_name
    ]

    if matching_topics:
        return jsonify(matching_topics), 200
    else:
        return jsonify({'message': 'Topic not found'}), 404

@app.route('/create-partition', methods=['POST'])
def create_partition():
    new_partition = request.json
    required_fields = ['partitionId', 'topicUUID', 'replicas', 'ISR', 'leader']

    if all(field in new_partition for field in required_fields):
        partition_record = {
            'partitionId': new_partition['partitionId'],
            'topicUUID': new_partition['topicUUID'],
            'replicas': new_partition['replicas'],
            'ISR': new_partition['ISR'],
            'removingReplicas': [],
            'addingReplicas': [],
            'leader': new_partition['leader'],
            'partitionEpoch': 0,
            'last_offset': datetime.utcnow().isoformat()
        }

        data_storage['PartitionRecords']['records'].append(partition_record)
        save_data_to_file()

        return jsonify({'message': 'Partition created successfully'}), 201
    else:
        return jsonify({'message': 'Missing fields in request'}), 400



if __name__ == "__main__":
    app.run(debug=True,port = 6000)


