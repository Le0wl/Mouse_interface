import rtde_receive
import rtde_control
import numpy as np
import time

class UR:
    def __init__(self, descriptive_device_name, ip):
        self.ip = ip
        self.dev_name = descriptive_device_name

        self.home_pos_joint_space_deg = [0, -90, 0, -90, 0, 0]

    def connect(self):
        try:
            self.recv = rtde_receive.RTDEReceiveInterface(self.ip)
            self.ctrl = rtde_control.RTDEControlInterface(self.ip)
            print(self.dev_name, "successfully connected")
        except: 
            print(self.dev_name, "cannot be connected")

    def disconnect(self):
        try:
            self.recv.disconnect()
            self.ctrl.disconnect()
            print(self.dev_name, "successfully disconnected")
        except: 
            print(self.dev_name, "cannot be disconnected")

    def move_joint_absolute(self, joint_in_deg, vel = 0.1, acc = 0.1):
        joint_in_rad = np.radians(joint_in_deg)
        self.ctrl.moveJ(joint_in_rad, vel, acc)

    def move_joint_relative(self, joint_in_deg, joint_relative_to_in_deg = None, vel = 0.1, acc = 0.1):
        joint_in_rad = np.radians(joint_in_deg)

        if joint_relative_to_in_deg is None:
            target_joint_in_rad = joint_in_rad + np.copy(self.recv.getActualQ())
        else:
            target_joint_in_rad = joint_in_rad + np.radians(joint_relative_to_in_deg)

        self.ctrl.moveJ(target_joint_in_rad, vel, acc)
        
    def move_pose_absolute(self, pose, vel = 0.05, acc = 0.1):
        self.ctrl.moveL(pose, vel, acc)


    def move_pose_relative(self, pose, pose_relative_to = None, vel = 0.05, acc = 0.1):

        if pose_relative_to is None:
            target_pose = np.asarray(pose) + np.copy(self.recv.getActualTCPPose())
        else:
            target_pose = np.asarray(pose) + np.asarray(pose_relative_to)

        self.ctrl.moveL(target_pose, vel, acc)

    def teach_mode(self, key):
        pose_record = []

        print("Press 's' to start teach mode")
        
        while key.keyPress != "s":
            pass

        print("Starting teach mode!")
        print("Press 'q' to end teach mode")
        print("Press 'a' to add a waypoint")
        print("Press 'r' to remove the previous waypoint")

        self.ctrl.teachMode()

        pose_record.append(self.recv.getActualTCPPose())
        print("Added starting way point")
        while key.keyPress != "q":

            if key.keyPress == "a":
                pose_record.append(self.recv.getActualTCPPose())
                
                while key.keyPress == "a":
                    pass
                print("Added way point number", len(pose_record))

            if key.keyPress == "r":
                pose_record.pop()
                
                while key.keyPress == "a":
                    pass
                print("Removed way point. Now has", len(pose_record), "way points")

        self.ctrl.endTeachMode()
        print("Teach mode finished")

        return pose_record
    

    def playback(self, pose_record, time_record, vel_to_start = 0.1, acc_to_start = 0.11):

        self.ctrl.moveJ_IK(pose_record[0], vel_to_start, acc_to_start)
        
        pose_record.pop(0)
        time_record.pop(0)

        for p, t in zip(pose_record, time_record):
            t_start = self.ctrl.initPeriod()

            joint_p = self.ctrl.getInverseKinematics(p)

            self.ctrl.servoJ(joint_p, 0, 0, t, 0.1, 300)
    
            self.ctrl.waitPeriod(t_start)

        self.ctrl.servoStop()

    def playback2(self, pose_record, vel_to_start = 0.1, acc_to_start = 0.11, vel = 0.1, acc = 0.1):
        
        for i, p in enumerate(pose_record):
            if i == 0:
                self.ctrl.moveJ_IK(p, vel_to_start, acc_to_start)
            else:
                self.ctrl.moveJ_IK(p, vel, acc)