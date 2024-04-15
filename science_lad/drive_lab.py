#Declare libraries
import rclpy
from .submodules.lx16a import *
#from lx16a import *
from math import *
from std_msgs.msg import *
from numpy import*
from rclpy.node import Node
import serial

class DriveScienceListener(Node):
    
    def __init__(self):
        # Init the node
        super().__init__('listener_drive_lab')
        self.subscriber_elevator = self.create_subscription(Int8,"science/elevator",self.callbackelevator,10)
        self.subscriber_elevator
        self.subscriber_servo1 = self.create_subscription(Int8,"science/servos1", self.callbackservo1,10)
        self.subscriber_servo1
        self.subscriber_servo2 = self.create_subscription(Int8,"science/servos2", self.callbackservo2,10)
        self.subscriber_servo2
        try:
            LX16A.initialize("/dev/ttyUSB1")
        except Exception as e:
            print(e)

        try: 
            self.ser = serial.Serial('/dev/ttyUSB0', 115200, timeout= 1)
        except Exception as e:
            print(e)

        self.servo1 = LX16A(1)
        #self.servo3 = LX16A(3)
        self.servo1.servoMode()
        #self.servo3.servoMode()

        self.servo1_data = None
        self.servo2_data = None
        self.elevator_data = None

        self.timer = self.create_timer(0.05, self.main)

    def callbackservo1(self,data):
        self.servo1_data = int(data.data)

    def callbackservo2(self,data):
        self.servo2_data = int(data.data)
    
    def callbackelevator(self,data):
        self.elevator_data = int(data.data)


    def main(self):
        print("entre")

        if(self.servo1_data == -1):
            self.servo1.moveTimeWrite(0)
        elif(self.servo1_data == 0):
            self.servo1.moveTimeWrite(95)
        elif(self.servo1_data == 1):
            self.servo1.moveTimeWrite(185)

        #if(self.servo2_data == -1):
            #self.servo3.moveTimeWrite(0)
        #elif(self.servo2_data == 0):
            #self.servo3.moveTimeWrite(95)
        #elif(self.servo2_data == 1):
            #self.servo3.moveTimeWrite(185)

        #self.servo1.moveTimeWrite(int(self.servo1_data))
        #self.servo3.moveTimeWrite(int(self.servo2_data))

        if(self.elevator_data == 1):
            self.ser.write(('1\n').encode())
        elif(self.elevator_data == -1):
            self.ser.write(('-1\n').encode())
        self.elevator_data == 0
        #else:
            #self.ser.write(('2\n').encode())


        


def main(args=None):
    rclpy.init(args=args)
    listener=DriveScienceListener()
    rclpy.spin(listener)
    listener.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()