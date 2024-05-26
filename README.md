# Kafka-Metadata-Mgmt

## YAKRaft: Revolutionizing Kafka Metadata Management through KRaft Protocol Implementation

YAKRaft is a project aimed at revolutionizing Kafka metadata management through the implementation of the KRaft protocol. It leverages the principles of the Raft consensus algorithm to ensure fault tolerance, reliability, and consistency in managing Kafka metadata.

## Overview

This project consists of several components:

1. **Data Preprocessing**: A set of Python scripts (`data_preprocessing.py`) for preprocessing raw data before feeding it into Kafka.

2. **Kafka Metadata Management**: A Flask application (`app.py`) for managing Kafka metadata, including broker registration, topic creation, partition management, and producer registration.

3. **Raft Consensus Algorithm**: Implementation of the Raft consensus algorithm in Python to maintain consistency and fault tolerance among multiple Kafka metadata management nodes.

## Project Files

### 1. `data_preprocessing.py`

This Python script preprocesses raw data before feeding it into Kafka. It includes functions for data cleaning, transformation, and validation.

### 2. `app.py`

This Flask application provides RESTful APIs for managing Kafka metadata. It includes endpoints for registering brokers, creating topics, managing partitions, and registering producers. It stores metadata in JSON format and ensures data consistency using the KRaft protocol.

### 3. `bd_final.py`

This Python script implements a simplified version of the Raft consensus algorithm. It includes classes for `RaftNode` and `LogEntry`, simulating the behavior of nodes in a distributed system. The algorithm ensures fault tolerance and consistency in managing Kafka metadata across multiple nodes.

## Usage

1. **Data Preprocessing**: Run `data_preprocessing.py` to preprocess raw data before feeding it into Kafka.

2. **Kafka Metadata Management**: Start the Flask application (`app.py`) to manage Kafka metadata. Use the provided RESTful APIs to register brokers, create topics, manage partitions, and register producers.

3. **Raft Consensus Algorithm**: Use `bd_final.py` to simulate the behavior of nodes in a distributed system. The algorithm ensures fault tolerance and consistency in managing Kafka metadata across multiple nodes.

## Contributors

- Surendran Venkataraman

## License

This project is licensed under the [MIT License](LICENSE).
