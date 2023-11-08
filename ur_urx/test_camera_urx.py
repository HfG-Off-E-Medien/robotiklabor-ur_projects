import urx
from time import sleep
import cv2

prod = True
robot = urx.Robot("192.168.0.77")
robot.set_tcp((0, 0, 0.1, 0, 0, 0))
robot.set_payload(2, (0, 0, 0.1))
sleep(0.2)  # delay for elaborate setup commands

# define static movements
init_pose = [1.430511474609375e-06, -1.570815225640768, -3.0040740966796875e-05, -1.5708261928954066, -2.462068666631012e-05, -8.885060445606996e-06] 
left_pose = [1.230511474609375e-06, -1.290815225640768, 2.1865895406544496e-05, -1.2708023510374964, 2.2126602172851562e-05, -2.0282826558888246e-05]
right_pose = [0.40950632095336914, -1.8714930019774378, -0.4720034599304199, -1.8088137112059535, -0.24520761171449834, -0.9267142454730433]

# Initialize the webcam
cap = cv2.VideoCapture(0)

# Load a pre-trained face detection model (you may need to install OpenCV's haarcascades)
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# definition of acceleration and velocity
a = 1.0  # acceleration
v = 0.25  # velocity

try:
    if prod:
        # home position
        robot.movej(init_pose, a, v, wait=False)
        sleep(10)

        while True:
            ret, frame = cap.read()

            # Perform face detection on the frame
            faces = face_cascade.detectMultiScale(frame, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

            for (x, y, w, h) in faces:
                # Calculate the center of the detected face
                center_x = x + w // 2
                center_y = y + h // 2

                # Draw a rectangle around the detected face
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

                # Display center_x and center_y on the top left corner
                cv2.putText(frame, f"center_x: {center_x}, center_y: {center_y}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

                # Perform robot movements based on the face position (modify as needed)
                # For example, you can adjust the robot's target_pose based on the face's position
                # and control the robot's movement accordingly.

                if center_x < 500:
                    robot.movej(left_pose, a, v, wait=False)
                    sleep(3)
                elif center_x > 1000:
                    robot.movej(right_pose, a, v, wait=False)
                    sleep(3)
                else:
                    robot.movej(init_pose, a, v, wait=False)
                    sleep(3)

            # Display the frame with face detection
            cv2.imshow("Face Detection", frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

    else:
        joint_positions_j = robot.getj()
        print("Joint Coords:", joint_positions_j)
        t = robot.get_pose()
        print("Transformation from base to tcp is: ", t)
except Exception as e:
    print(f"An error occurred: {str(e)}")
finally:
    # close the connection
    robot.close()
