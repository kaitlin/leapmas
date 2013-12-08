import Leap, sys
import serial
import time
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture, InteractionBox



class LightListener(Leap.Listener):

    def on_init(self, controller):
        print "Initialized"
        #self.ser = serial.Serial('/dev/ttyACM0', 9600)
        self.color_cycle =["G255;000;000X", "G000;255;000X", "G000;000;255X", "G255;255;000X"]
        time.sleep(1) #wait for the arduino to be ready
        self.interaction_box = InteractionBox()
        print self.interaction_box.width
        print self.interaction_box.height
        print self.interaction_box.depth

    def on_connect(self, controller):
        print "Connected"
        # Enable gestures
        controller.enable_gesture(Leap.Gesture.TYPE_CIRCLE);
        controller.enable_gesture(Leap.Gesture.TYPE_KEY_TAP);
        controller.enable_gesture(Leap.Gesture.TYPE_SCREEN_TAP);
        controller.enable_gesture(Leap.Gesture.TYPE_SWIPE);

    def on_disconnect(self, controller):
        # Note: not dispatched when running in a debugger.
        print "Disconnected"

    def on_exit(self, controller):
        print "Exited"

    def on_frame(self, controller):
        # Get the most recent frame and report some basic information
        frame = controller.frame()
#        print frame. current_frames_per_second
        #detect circle or swipe gestures
        for gest in frame.gestures():
            
            if gest.type == Leap.Gesture.TYPE_KEY_TAP:
                tap = KeyTapGesture(gest)
                if tap.state == Leap.Gesture.STATE_STOP:

                    if not frame.hands.is_empty:
                        hand = frame.hands[0]
                        fingers = hand.fingers
                        if not fingers.is_empty:
                            for (i, f) in enumerate(fingers):
                                if f == tap.pointable:
                                    self.ser.write(self.color_cycle[i])
                                    print "TAP!!!"
                                    #refactor this to get hand from gesture, then order pointables by x position to get order of fingers

                                
            
            a="""if gest.type == Leap.Gesture.TYPE_CIRCLE:
                circle = CircleGesture(gest)
                if circle.state == Leap.Gesture.STATE_START:
                    print "circle started"
                if circle.state == Leap.Gesture.STATE_STOP:
                    print "circle ended"
                    #make call to trigger 

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
                palm_norm = self.interaction_box.normalize_point(palm)
                x, y, z = palm_norm[0], palm_norm[1], palm_norm[2]
                print "x: {0}  y:{1}  z:{2}".format(x,y,z)

                #self.ser.write("{0};{1};{2}X".format(x, y, z))
def main():
    # Create a sample listener and controller
    listener = LightListener()
    controller = Leap.Controller()

    # Have the sample listener receive events from the controller
    controller.add_listener(listener)

    # Keep this process running until Enter is pressed
    print "Press Enter to quit..."
    sys.stdin.readline()

    # Remove the sample listener when done
    controller.remove_listener(listener)


if __name__ == "__main__":
    main()
