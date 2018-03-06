# Script to manually control a MeArm with an XBOX controller
# Needs servoblaster running and xboxdrv installed
import xbox
from servos import Servo

TIMESTEP = 0.2  # seconds
PERCENT_INCREASE = 10 # % of max range

def main():
    with open("/dev/servoblaster", "w") as sb_fd:
        servos = {
            "base": Servo(sb_fd, 2, (3, 99), (0, 180)),
            "forward": Servo(sb_fd, 1, (3, 45), (0, 180)),
            "upward": Servo(sb_fd, 3, (5, 90), (0, 180)),
            "claw": Servo(sb_fd, 4, (1, 15), (0, 180)),
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
            
            if joy.leftTrigger():
                command_issued = True
                servos["claw"].percent_position += PERCENT_INCREASE * joy.leftTrigger()
            if joy.rightTrigger():
                command_issued = True
                servos["claw"].percent_position -= PERCENT_INCREASE * joy.leftTrigger()
            if joy.leftX():
                command_issued = True
                servos["forward"].percent_position += PERCENT_INCREASE * joy.leftX()
            if joy.leftY():
                command_issued = True
                servos["base"].percent_position -= PERCENT_INCREASE * joy.leftY()
            if joy.rightX():
                command_issued = True
                servos["upward"].percent_position += PERCENT_INCREASE * joy.rightX()

            if joy.Start():
                for servo in servos.values():
                    servo.reset()

            if command_issued:
                last_event = time.time() + TIMESTEP

if __name__ == '__main__':
    main()