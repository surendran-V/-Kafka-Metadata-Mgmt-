class LogEntry:
    def __init__(self, term, command):
        self.term = term
        self.command = command

    def _repr_(self):
        return f"LogEntry(term={self.term}, command={self.command})"


class RaftNode:
    def __init__(self, node_id):
        self.node_id = node_id
        self.state = "follower"
        self.current_term = 0
        self.voted_for = None
        self.log = []
        self.commit_index = 0
        self.last_applied = 0

    def request_vote(self, candidate_id, term, last_log_index, last_log_term):
        if term > self.current_term:
            self.current_term = term
            self.state = "follower"
            self.voted_for = None

        if (
            term == self.current_term
            and (self.voted_for is None or self.voted_for == candidate_id)
            and last_log_index >= 0 and last_log_index < len(self.log)
            and (last_log_index == 0 or last_log_term >= self.log[last_log_index].term)
        ):
            self.voted_for = candidate_id
            return {"term": self.current_term, "vote_granted": True}
        else:
            return {"term": self.current_term, "vote_granted": False}

    def append_entries(self, leader_id, term, prev_log_index, prev_log_term, entries, leader_commit):
        if term < self.current_term:
            return {"term": self.current_term, "success": False}

        if term > self.current_term:
            self.current_term = term
            self.state = "follower"
            self.voted_for = None

        if prev_log_index > len(self.log) - 1 or (prev_log_index >= 0 and self.log[prev_log_index].term != prev_log_term):
            return {"term": self.current_term, "success": False}

        # Append new entries and update commit index
        self.log.extend(entries)
        self.commit_index = min(leader_commit, len(self.log) - 1)

        return {"term": self.current_term, "success": True}

    def send_message(self, message, receiver_node):
        # In a real implementation, this method would send a message to another node.
        # For simplicity, we'll directly call the receive_message function of the receiver node.
        receiver_node.receive_message(message)

    def receive_message(self, message):
        # In a real implementation, this method would process incoming messages from other nodes.
        # For simplicity, we'll just print the message in this example.
        print(f"Node {self.node_id} received message: {message}")

    def start_election(self):
        self.state = "candidate"
        self.current_term += 1
        self.voted_for = self.node_id

        return {"term": self.current_term, "vote_granted": 1}  # Vote for itself

    def become_leader(self):
        self.state = "leader"

        next_index = {node_id: len(self.log) for node_id in range(3) if node_id != self.node_id}
        match_index = {node_id: 0 for node_id in range(3) if node_id != self.node_id}

        return {"term": self.current_term, "success": True, "next_index": next_index, "match_index": match_index}

    def become_follower(self):
        self.state = "follower"

    def handle_timeout(self):
        if self.state == "follower" or self.state == "candidate":
            self.start_election()
        elif self.state == "leader":
            # Send heartbeats to maintain leadership
            pass

    def apply_log_entries(self):
        while self.last_applied < self.commit_index:
            self.last_applied += 1
            # Apply log entry to the state machine (not implemented in this example)

    def replicate_log_entries(self):
        if self.state == "leader":
            for follower_id in range(3):
                if follower_id != self.node_id:
                    # Simulate sending log entries to followers for replication
                    next_index = len(self.log)
                    entries_to_replicate = self.log[next_index:]
                    match_index = next_index - 1
                    success = self.send_append_entries(follower_id, next_index, entries_to_replicate, match_index)

                    if success:
                        # Update next_index and match_index for the follower
                        next_index += len(entries_to_replicate)
                        match_index = next_index - 1
                    else:
                        # Handle failure (e.g., decrease next_index)
                        pass
        else:
            print(f"Node {self.node_id}: Not the leader, cannot replicate log entries.")

    def send_append_entries(self, follower_id, next_index, entries, match_index):
        # Simulate sending AppendEntries RPC to a follower
        append_entries_message = {
            "term": self.current_term,
            "leader_id": self.node_id,
            "prev_log_index": next_index - 1,
            "prev_log_term": self.log[next_index - 1].term if next_index > 0 else -1,
            "entries": entries,
            "leader_commit": match_index,
        }

        # In a real implementation, you would send this message to the follower
        # and handle the response to determine if replication was successful.

        # For the sake of this example, assume success.
        return True

    def handle_client_request(self, request):
        if self.state == "leader":
            entry = LogEntry(term=self.current_term, command=request)
            self.log.append(entry)
            self.replicate_log_entries()
            return f"Node {self.node_id}: Client request executed by the leader."
        else:
            return f"Node {self.node_id}: Not the leader, cannot execute client request."

    def handle_new_leader(self):
        self.state = "follower"
        self.voted_for = None


# ... (previous code remains unchanged)

raft_nodes = [RaftNode(node_id=i) for i in range(3)]

# Simulate an election and check the results
for node in raft_nodes:
    if node.state == "follower":
        vote_response = node.request_vote(candidate_id=2, term=1, last_log_index=-1, last_log_term=0)
        print(f"Node {node.node_id}: {vote_response}")

# Expected output with range(3):
# Node 0: {'term': 1, 'vote_granted': False}
# Node 1: {'term': 1, 'vote_granted': False}
# Node 2: {'term': 1, 'vote_granted': False}

# Simulate an append entries RPC from a leader (node ID: 2)
leader_node = raft_nodes[1]
for node in raft_nodes:
    if node.node_id != leader_node.node_id:
        append_entries_response = node.append_entries(
            leader_id=leader_node.node_id,
            term=2,
            prev_log_index=-1,
            prev_log_term=0,
            entries=[],
            leader_commit=0,
        )
        print(f"Node {node.node_id}: {append_entries_response}")

# Expected output with range(3):
# Node 0: {'term': 2, 'success': False}
# Node 1: {'term': 2, 'success': False}
# Node 2: {'term': 2, 'success': False}

# Simulate a client request to one of the nodes
client_request_node = raft_nodes[0]
client_request_response = client_request_node.handle_client_request("example_command")
print(client_request_response)

# Expected output:
# Node 0: Not the leader, cannot execute client request.

# Check the state of the nodes after the client request
for node in raft_nodes:
    print(f"Node {node.node_id}: State - {node.state}, Term - {node.current_term}")
    print(f"Node {node.node_id}: Log - {node.log}")