import urx
from time import sleep

prod = True
robot = urx.Robot("192.168.0.77")
robot.set_tcp((0, 0, 0.1, 0, 0, 0))
robot.set_payload(2, (0, 0, 0.1))
sleep(0.2)  # delay for elaborate setup commands
#home position of the robot
init_pose = [1.430511474609375e-06, -1.570815225640768, -3.0040740966796875e-05, -1.5708261928954066, -2.462068666631012e-05, -8.885060445606996e-06]
# definition of acceleration and velocity
a = 2.0  # acceleration
v = 0.5  # velocity

try:
    if prod:
        # Start coreography
        target_pose = [1.230511474609375e-06, -1.290815225640768, 2.1865895406544496e-05, -1.2708023510374964, 2.2126602172851562e-05, -2.0282826558888246e-05]  # test coords
        robot.movej(target_pose, a, v, wait=False)
        sleep(10)
        target_pose = [0.44907236099243164, -1.3290975850871583, 0.5394447485553187, -0.9637988370708008, 0.3632233142852783, 1.0841753482818604]  # test coords
        robot.movej(target_pose, a, v, wait=False)
        sleep(10)
        target_pose = [0.40950632095336914, -1.8714930019774378, -0.4720034599304199, -1.8088137112059535, -0.24520761171449834, -0.9267142454730433]  # test coords
        robot.movej(target_pose, a, v, wait=False)
        sleep(10)
        target_pose = [-0.20734817186464483, -2.023131032983297, -0.017201900482177734, -1.8087898693480433, 1.1775991916656494, -0.9267142454730433]  # test coords
        robot.movej(target_pose, a, v, wait=False)
        sleep(10)
        robot.movej(init_pose, a, v, wait=False)

        # Wait till the robot is done
        #robot.wait()

        joint_positions_j = robot.getj()
        print("Joint Coords:", joint_positions_j)
        t = robot.get_pose()
        print("Transformation from base to tcp is: ", t)
    else:
        joint_positions_j = robot.getj()
        print("Joint Coords:", joint_positions_j)
        t = robot.get_pose()
        print("Transformation from base to tcp is: ", t)

finally:
    # close the connection
    robot.close()

