# Script to manually control a MeArm with an XBOX controller
# Needs servoblaster running and xboxdrv installed
import xbox
from servos import Servo
import time
import pickle
import os.path

TIMESTEP = 0.04  # seconds
PERCENT_INCREASE = 10 # % of max range
PICKLED_POSITIONS = "saved_positions.p"


def main():
    with open("/dev/servoblaster", "w") as sb_fd:
        servos = {
            "base": Servo(sb_fd, 0, (3, 99), (0, 180)),
            "forward": Servo(sb_fd, 1, (3, 45), (0, 180)),
            "upward": Servo(sb_fd, 3, (5, 90), (0, 180)),
            "claw": Servo(sb_fd, 4, (1, 15), (0, 180)),
        }
        
        if os.path.isfile(PICKLED_POSITIONS):
            SAVED_POSITIONS = pickle.load(open(PICKLED_POSITIONS))
        else:
            SAVED_POSITIONS = {
                "X": {k: p.position for k, p in servos.items()},
                "Y": {k: p.position for k, p in servos.items()},
                "A": {k: p.position for k, p in servos.items()},
                "B": {k: p.position for k, p in servos.items()},
            }

        joy = xbox.Joystick()

        last_event = time.time()
        print "MeARM XBOX manual controller. Feel the POWAH!\n"
        print "Press back to exit"
        while not joy.Back():
            if (last_event + TIMESTEP) > time.time():
                continue
            if not joy.connected():
                continue
            
            command_issued = False
            save_position = False
            print_position = False
            
            if joy.dpadUp():
                print "dpad up pressed"
                save_position = True
                SAVED_POSITIONS["Y"] = {k: p.position for k, p in servos.items()}
            if joy.dpadDown():
                print "dpad down pressed"
                save_position = True
                SAVED_POSITIONS["A"] = {k: p.position for k, p in servos.items()}
            if joy.dpadLeft():
                print "dpad left pressed"
                save_position = True
                SAVED_POSITIONS["X"] = {k: p.position for k, p in servos.items()}
            if joy.dpadRight():
                print "dpad right pressed"
                save_position = True
                SAVED_POSITIONS["B"] = {k: p.position for k, p in servos.items()}
            if joy.Y():
                print_position = True
                for name, servo in servos.items():
                    servo.position = SAVED_POSITIONS["Y"][name]
            if joy.A():
                print_position = True
                for name, servo in servos.items():
                    servo.position = SAVED_POSITIONS["A"][name]
            if joy.X():
                print_position = True
                for name, servo in servos.items():
                    servo.position = SAVED_POSITIONS["X"][name]
            if joy.B():
                print_position = True
                for name, servo in servos.items():
                    servo.position = SAVED_POSITIONS["B"][name]
            if joy.leftTrigger():
                print "left trigger pressed"
                command_issued = True
                print_position = True
                servos["claw"].percent_position = 0.0
            if joy.rightTrigger():
                print "right trigger pressed"
                command_issued = True
                print_position = True
                servos["claw"].percent_position = 100.0
            if joy.leftY():
                print "left analog (Y)"
                command_issued = True
                print_position = True
                servos["forward"].percent_position += PERCENT_INCREASE * joy.leftY()
            if joy.leftX():
                print "left analog (X)"
                command_issued = True
                print_position = True
                servos["base"].percent_position -= PERCENT_INCREASE * joy.leftX()
            if joy.rightY():
                print "right analog (Y)"
                command_issued = True
                print_position = True
                servos["upward"].percent_position += PERCENT_INCREASE * joy.rightY()
            if joy.Start():
                print "start button"
                command_issued = True
                print_position = True
                for servo in servos.values():
                    servo.reset()

            if command_issued:
                last_event = time.time() + TIMESTEP
            if print_position:
                print "Current position is:"
                for name, servo in servos.items():  
                    print "\t", name, servo.position
            if save_position:
                pickle.dump(SAVED_POSITIONS, open(PICKLED_POSITIONS, "w"))

        joy.close()


if __name__ == '__main__':
    main()
