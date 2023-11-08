import urx
from time import sleep

rob = urx.Robot("192.168.0.77")
rob.set_tcp((0, 0, 0.1, 0, 0, 0))
rob.set_payload(2, (0, 0, 0.1))
sleep(0.2)  # leave some time for the robot to process the setup commands

# Define values for 'a' and 'v'
a = 1.0  # acceleration
v = 0.1  # velocity

rob.movej((1, 2, 3, 4, 5, 6), a, v)
rob.movel((x, y, z, rx, ry, rz), a, v)
print('Current tool pose is: ',  rob.getl())

try:
    rob.movel((0, 0, 0, 0, 0, 0), a, v, relative=True)  # move relative to the current pose
except urx.RobotException as ex:
    print("Robot could not execute move (emergency stop for example), do something", ex)

rob.translate((0.1, 0, 0), a, v)  # move the tool and keep the orientation
rob.stopj(a)

rob.movel(x, y, z, rx, ry, rz, wait=False)
while True:
    sleep(0.1)  # sleep first since the robot may not have processed the command yet
    if rob.is_program_running():
        break

rob.movel(x, y, z, rx, ry, rz, wait=False)
while rob.getForce() < 50:
    sleep(0.01)
    if not rob.is_program_running():
        break
rob.stopl()
