import Leap, sys
import serial
import time
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture, InteractionBox

def night():
    if time.localtime().tm_hour >= 23:
        return True
    else:
        return False

class LightListener(Leap.Listener):

    def on_init(self, controller):
        print "Initialized"
        self.ser = serial.Serial('/dev/ttyACM0', 9600)
        self.color_cycle =["G255;000;000X", "G000;255;000X", "G000;000;255X", "G255;215;000X", "G000;191;255X"]
        time.sleep(1) #wait for the arduino to be ready
   
        if controller.config.set("Gesture.Circle.MinRadius", 30.0) :
            controller.config.save()
        
    def on_connect(self, controller):
        print "Connected"
        # Enable gestures
        #controller.enable_gesture(Leap.Gesture.TYPE_CIRCLE);
        controller.enable_gesture(Leap.Gesture.TYPE_KEY_TAP);
        controller.enable_gesture(Leap.Gesture.TYPE_SCREEN_TAP);
        controller.enable_gesture(Leap.Gesture.TYPE_SWIPE);


    def on_disconnect(self, controller):
        # Note: not dispatched when running in a debugger.
        print "Disconnected"

    def on_exit(self, controller):
        print "Exited"

    def on_frame(self, controller):
        
        #Check if it's after 11pm
        if night():
            ser.write("000;000;000X")
            sys.exit()

        # Get the most recent frame and report some basic information
        frame = controller.frame()
        ib = frame.interaction_box
#        print frame. current_frames_per_second
        #detect circle or swipe gestures
        for gest in frame.gestures():
            
            if gest.type == Leap.Gesture.TYPE_KEY_TAP:
                tap = KeyTapGesture(gest)
                if tap.state == Leap.Gesture.STATE_STOP:
                    gest_finger = tap.pointable
                    hand = gest_finger.hand
                    fingers = hand.fingers
                    fingers = [fingers[x] for x in range(0, len(fingers))]
                    fingers.sort(key=lambda x: x.tip_position[0])
                    for (i, f) in enumerate(fingers):
                        if f.id == gest_finger.id:
                            print "finger #{0} was tapped".format(i)
                            self.ser.write(self.color_cycle[i])

                                
            
            elif gest.type == Leap.Gesture.TYPE_CIRCLE:
                circle = CircleGesture(gest)
                if circle.state == Leap.Gesture.STATE_STOP:
                    if circle.pointable.direction.angle_to(circle.normal) <= Leap.PI/2:
                        #it's clockwise
                        self.ser.write("C")
                    else:
                        self.ser.write("O")
                        #it's counterclockwise
                    #make call to trigger 
                    print "Circle!"
            a = """
            elif gest.type == Leap.Gesture.TYPE_SWIPE:
                swipe = SwipeGesture(gest)
                if swipe.state == Leap.Gesture.STATE_START:
                    print "you're swiping!"
                if swipe.state == Leap.Gesture.STATE_STOP:
                    print "you're done swiping!"
            """

        #check palm position
        if not frame.hands.is_empty:
            if len(frame.hands) == 1:
                palm = frame.hands[0].stabilized_palm_position
                #palm = frame.hands[0].palm_position
                palm_norm = ib.normalize_point(palm)
                #print ib.width
                #print ib.depth
                #print ib.height
                #print palm_norm
                #print palm

                x, y, z = palm_norm[0], palm_norm[2], palm_norm[1]
                #print palm[0]
                #print x
                #print "===="
                #print palm[2]
                #print y
                #print "======"
                #print palm[1]
                #print z 
                #print "========="
                r, g, b = x * 255, y * 255, z * 255
                #print "r: {0}  g:{1}  b:{2}".format(r,g,b)
                #print "x: {0}  y:{1}  z:{2}".format(x,y,z)
                
                #print "{0:03d};{1:03d};{2:03d}X".format(int(r), int(g), int(b))
                self.ser.write("{0:03d};{1:03d};{2:03d}X".format(int(r), int(g), int(b)))
def main():
    # Create a sample listener and controller
    listener = LightListener()
    controller = Leap.Controller()

    # Have the sample listener receive events from the controller
    controller.add_listener(listener)

    # Keep this process running until Enter is pressed
    #print "Press Enter to quit..."
 
    #sys.stdin.readline()
    while True:
      #  pass
      time.sleep(1)
    # Remove the sample listener when done
    controller.remove_listener(listener)


if __name__ == "__main__":
    main()
