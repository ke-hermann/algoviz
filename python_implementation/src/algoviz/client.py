import socket
import pickle

import mockobjects


# Function to serialize and send an object to the server
def send_object_to_server(obj, server_host="127.0.0.1", server_port=9999):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_host, server_port))

    try:
        # Serialize the object
        serialized_data = pickle.dumps(obj)

        # Send the serialized object to the server
        client_socket.send(serialized_data)

        # Receive acknowledgment from the server
        acknowledgment = client_socket.recv(1024).decode("utf-8")
        print(f"[SERVER RESPONSE] {acknowledgment}")
    finally:
        client_socket.close()


# Example usage
if __name__ == "__main__":
    # Create a Python object to send
    example = mockobjects.mock_list()
    example_grid = mockobjects.mock_cooridnate_grid()
    example_ascii = mockobjects.mock_ascii_text()
    # Send the object to the server
    send_object_to_server(example_ascii)
