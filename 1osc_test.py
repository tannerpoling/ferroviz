from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import BlockingOSCUDPServer


def print_handler(address, *args):
    print(f"{address}: {args}")


def default_handler(address, *args):
    print(f"DEFAULT {address}: {args}")

def my_handler(address, *args):
    print("in my handler!")
    # print(f"all data: {args}")
    print(f"args[0]: {args[0]}")


dispatcher = Dispatcher()
# dispatcher.map("/something/*", print_handler)
dispatcher.set_default_handler(default_handler)
dispatcher.map("/knob1", my_handler)

ip = "169.254.44.162"
port = 1337

server = BlockingOSCUDPServer((ip, port), dispatcher)
server.serve_forever()  # Blocks forever