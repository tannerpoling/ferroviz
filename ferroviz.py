from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import BlockingOSCUDPServer
import RPi.GPIO as GPIO          
from time import sleep

##### VARIABLE SETUP
# range of values from midi knob
input_min = 0
input_max = 127
# range of values going out to electromagnets
output_min = 10
output_max = 75
# GPIO variables
in1 = 24
in2 = 23
en = 25
temp1=1

##### FUNCTION DEFS
def my_handler(address, *args):
    print("in my handler!")
    # print(f"all data: {args}")
    print(f"args[0]: {args[0]}")
    val = args[0]
    out = translate(val, input_min, input_max, output_min, output_max)
    p.ChangeDutyCycle(out)    

# Translate 'value' from 'left' range to 'right' range
def translate(value, leftMin, leftMax, rightMin, rightMax):
    # If value outside of range, apply ceiling
    if (value > leftMax): value = leftMax
    if (value < leftMin): value = leftMin
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin
    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)
    # Convert the 0-1 range into a value in the right range.
    return rightMin + (valueScaled * rightSpan)


##### GPIO SETUP
GPIO.setmode(GPIO.BCM)
GPIO.setup(in1,GPIO.OUT)
GPIO.setup(in2,GPIO.OUT)
GPIO.setup(en,GPIO.OUT)
GPIO.output(in1,GPIO.LOW)
GPIO.output(in2,GPIO.LOW)
p=GPIO.PWM(en,1000)
p.start(25)


##### START SCRIPT
dispatcher = Dispatcher()
# dispatcher.map("/something/*", print_handler)
dispatcher.set_default_handler(default_handler)
dispatcher.map("/knob1", my_handler)

ip = "169.254.44.162"
port = 1337

server = BlockingOSCUDPServer((ip, port), dispatcher)
server.serve_forever()  # Blocks forever