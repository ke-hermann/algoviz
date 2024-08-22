import sys
import time
import mockobjects

from imgui_bundle import hello_imgui, imgui, immapp, ImVec2
from custom_types import DataObject

import threading
import socket
import queue
import pickle

# Function to handle client connections
def handle_client(client_socket, client_address, message_queue):
    print(f"[INFO] Connected to {client_address}")
    while True:
        try:
            # Receive the data from the client
            data = client_socket.recv(4096)
            if not data:
                break
            
            # Deserialize the data to a Python object
            obj = pickle.loads(data)
            print(obj)
            
            # Put the object in the queue to be processed by the main thread
            message_queue.put((client_address, obj))
            
            # Send acknowledgment back to the client
            client_socket.send("Object received".encode('utf-8'))
        except ConnectionResetError:
            break
        except Exception as e:
            print(f"[ERROR] {e}")
            break
    print(f"[INFO] Connection closed by {client_address}")
    client_socket.close()


# Function to start the server
def start_server(host, port, message_queue):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(5)
    print(f"[INFO] Server listening on {host}:{port}")

    while True:
        client_socket, client_address = server.accept()
        client_handler = threading.Thread(
            target=handle_client,
            args=(client_socket, client_address, message_queue),
            daemon=True,  # Allows the server to exit even if threads are still running
        )
        client_handler.start()


# Function to run the server in a separate thread
def run_server_thread(host="0.0.0.0", port=9999):
    message_queue = queue.Queue()  # Queue for communication between threads
    server_thread = threading.Thread(
        target=start_server, args=(host, port, message_queue), daemon=True
    )
    server_thread.start()
    print("[INFO] Server running in a separate thread")
    return message_queue


class ObjectInspector:
    def __init__(self, obj: DataObject):
        self.obj = obj
        self.data = self.obj.data
        self.startup = True
        self.is_open = True

    def retrieve_object_info(self):
        if isinstance(self.data, list):
            return dict(enumerate(self.data))
        elif isinstance(self.data, dict):
            return self.data

    def display(self):
        if self.startup is True:
            imgui.set_next_window_pos(ImVec2(300, 300))
            imgui.set_next_window_size(ImVec2(400, 300))

        if self.is_open:
            _, self.is_open = imgui.begin("Object Inspector", True)

            imgui.begin_table("table1", 2)
            imgui.table_setup_column("Property")
            imgui.table_setup_column("Value")
            imgui.table_headers_row()

            info = self.retrieve_object_info()

            for k, v in info.items():
                imgui.table_next_column()
                imgui.text(str(k))
                imgui.table_next_column()
                imgui.text(str(v))

            imgui.end_table()
            imgui.end()
        self.startup = False


class Gui:
    def __init__(self, fps=144):
        imgui.create_context()
        # list of containers holding the data objects we're going to visualize
        self.data_objects = [mockobjects.mock_list()]
        self.selected_object = None
        # UI state
        self.startup = True
        self.inspectors = []
        # initial UI layout
        self.startup = True
        self.fps = 1 / fps
        # outbound connection so we can actually receive user data
        self.message_queue = run_server_thread()  # Start the server on a non-blocking thread

    def ui_loop(self):
        # UI Loop
        hello_imgui.apply_theme(hello_imgui.ImGuiTheme_.imgui_colors_dark)
        self.sidebar()
        self.visualisation()
        self.startup = False
        # here we keep a list of optional windows that might be opened
        for w in self.inspectors:
            w.display()

        # clean up and remove closed windows:
        self.inspectors = [p for p in self.inspectors if p.is_open]
        time.sleep(self.fps)

    def visualisation(self):
        if self.startup:
            imgui.set_next_window_size(ImVec2(600, 400))
            imgui.set_next_window_pos(ImVec2(250, 20))
        imgui.begin("Data Visualisation", True)

        if self.selected_object is None:
            pass
        elif self.selected_object.visualized is False:
            pass
        else:
            # to be implemented
            pass
        imgui.end()

    def sidebar(self):
        "Represents individual data objects that can be selected for visualisation"
        if self.startup:
            imgui.set_next_window_size(ImVec2(200, 600))
            imgui.set_next_window_pos(ImVec2(20, 20))
        imgui.begin("Select Elements", True)
        # iterate over the data elements and represent each as a clickable button
        if self.data_objects is not None:
            for element in self.data_objects:
                imgui.button(element.name, ImVec2(imgui.get_window_width() - 10, 20))

                if imgui.is_item_hovered():
                    imgui.set_tooltip(element.category)

                if imgui.is_item_clicked():
                    self.selected_object = element
                    self.inspectors.append(ObjectInspector(element))

        imgui.end()

    def menubar(self):
        if imgui.begin_main_menu_bar():
            if imgui.begin_menu("File", True):
                clicked_quit, selected_quit = imgui.menu_item(
                    "Quit", "Cmd+Q", False, True
                )
                if clicked_quit:
                    sys.exit(0)

                imgui.end_menu()
            imgui.end_main_menu_bar()


if __name__ == "__main__":
    gui = Gui()
    immapp.run(
        gui_function=gui.ui_loop,
        window_title="Algoviz!",
        window_size=(1000, 800),
    )
