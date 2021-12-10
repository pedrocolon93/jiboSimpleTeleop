from Tkconstants import END
from Tkinter import LEFT, Button, TOP, Label, Frame, BOTTOM, Tk, Text

try:
    import rospy
    from jibo_msgs.msg import JiboAction, JiboVec3, JiboAsrCommand
    from std_msgs.msg import Header, Int8, Bool, String  # standard ROS msg header
except:
    print("Could not load ros stuff!!!")
import time
import os
# os.environ['ROS_MASTER_URI'] = 'http://matlaberp7.media.mit.edu:11311'
# os.environ['ROS_MASTER_IP'] = 'matlaberp7.media.mit.edu'
ROSCORE_TO_JIBO_TOPIC = '/jibo'


class RobotSender:

    def __init__(self):
        self.robot_commander = None
        self.robot_asr_commander = None

    def start_robot_publisher(self):
        """
        Starts up the robot publisher node
        """

        rospy.init_node('Jibo_Mhri_Teleop', anonymous=True)
        print('Robot Pub Node started')

        msgType = JiboAction
        msgTopic = ROSCORE_TO_JIBO_TOPIC

        self.robot_commander = rospy.Publisher(msgTopic, msgType, queue_size=10)
        self.robot_asr_commander = rospy.Publisher('jibo_asr_command', JiboAsrCommand, queue_size=1)
        rate = rospy.Rate(10)  # spin at 10 Hz
        rate.sleep()  # sleep to wait for subscribers

    def send_robot_motion_cmd(self, command):
        """
        send a Motion Command to Jibo
        """

        msg = JiboAction()
        # add header
        msg.header = Header()
        msg.header.stamp = rospy.Time.now()

        msg.do_motion = True
        msg.do_tts = False
        msg.do_lookat = False

        msg.motion = command

        self.robot_commander.publish(msg)
        rospy.loginfo(msg)

    def send_robot_tts_cmd(self, text, *args):
        """
        send a Motion Command to Jibo
        """

        msg = JiboAction()
        # add header
        msg.header = Header()
        msg.header.stamp = rospy.Time.now()

        msg.do_motion = False
        msg.do_tts = True
        msg.do_lookat = False

        msg.tts_text = text

        self.robot_commander.publish(msg)
        rospy.loginfo(msg)

    def send_robot_lookat_cmd(self, x, y, z):
        """
        send a Motion Command to Jibo
        """

        msg = JiboAction()
        # add header
        msg.header = Header()
        msg.header.stamp = rospy.Time.now()

        msg.do_motion = False
        msg.do_tts = False
        msg.do_lookat = True

        position = JiboVec3(x, y, z)

        msg.lookat = position

        self.robot_commander.publish(msg)
        rospy.loginfo(msg)

    def send_robot_audio_cmd(self, audio_command):
        """
        send a Motion Command to Jibo
        """

        msg = JiboAction()
        # add header
        msg.header = Header()
        msg.header.stamp = rospy.Time.now()

        msg.do_motion = False
        msg.do_tts = False
        msg.do_lookat = False
        msg.do_sound_playback = True

        msg.audio_filename = audio_command

        self.robot_commander.publish(msg)
        rospy.loginfo(msg)

    def send_robot_audio_motion_cmd(self, a, m):
        """
        send LED ring color Command to Jibo
        """

        msg = JiboAction()
        # add header
        msg.header = Header()
        msg.header.stamp = rospy.Time.now()

        msg.do_sound_playback = True
        msg.do_motion = True

        msg.audio_filename = a
        msg.motion = m

        self.robot_commander.publish(msg)
        rospy.loginfo(msg)

    def send_robot_led_cmd(self, r, g, b):
        """
        send LED ring color Command to Jibo
        """

        msg = JiboAction()
        # add header
        msg.header = Header()
        msg.header.stamp = rospy.Time.now()

        msg.do_led = True

        color = JiboVec3(r, g, b)
        msg.led_color = color

        self.robot_commander.publish(msg)
        rospy.loginfo(msg)

    def send_robot_volume_cmd(self, v):
        """
        send LED ring color Command to Jibo
        """

        msg = JiboAction()
        # add header
        msg.header = Header()
        msg.header.stamp = rospy.Time.now()

        msg.do_volume = True

        msg.volume = v

        self.robot_commander.publish(msg)
        rospy.loginfo(msg)

    def send_robot_asr_cmd(self, cmd, heyjibo=False, continuous=False, rule=""):
        """
        send ASR Command to Jibo
        """

        msg = JiboAsrCommand()
        # add header
        msg.header = Header()
        msg.header.stamp = rospy.Time.now()

        msg.heyjibo = heyjibo
        msg.continuous = continuous

        msg.rule = rule
        msg.command = cmd

        self.robot_asr_commander.publish(msg)
        rospy.loginfo(msg)

    def send_robot_anim_transition_cmd(self, tran):
        msg = JiboAction()
        # add header
        msg.header = Header()
        msg.header.stamp = rospy.Time.now()

        msg.do_anim_transition = True
        msg.anim_transition = tran
        self.robot_commander.publish(msg)
        rospy.loginfo(msg)





if __name__ == '__main__':
    rs = RobotSender()
    rs.start_robot_publisher()

    root = Tk()
    frame = Frame(root)
    frame.pack()

    lookAtFrame = Frame(frame)
    lookAtFrame.pack()

    labelbutton = Button(lookAtFrame, text="Look At:")
    labelbutton.pack(side=TOP)


    def lookLeft():
        print('Gonna look at...left')

        rs.send_robot_lookat_cmd(0.3,0.2,0.3)


    def lookRight():
        rs.send_robot_lookat_cmd(0, 1, 0.4)


    def lookMiddle():
        rs.send_robot_lookat_cmd(0.3, 0.7, 0.4)


    leftButton = Button(lookAtFrame, text="Left", command=lookLeft)
    leftButton.pack(side=LEFT)

    middlebutton = Button(lookAtFrame, text="Middle", command=lookMiddle)
    middlebutton.pack(side=LEFT)

    rightbutton = Button(lookAtFrame, text="Right", command=lookRight)
    rightbutton.pack(side=LEFT)

    speakFrame = Frame(frame)
    speakFrame.pack()

    T = Text(speakFrame, height=1, width=30)
    T.pack(side=LEFT)
    def speak():
        data = T.get(1.0,END).strip()
        print('Gonna speak...', data)
        rs.send_robot_tts_cmd(data)

    speakButton = Button(speakFrame, text="Speak", command=speak)
    speakButton.pack(side=LEFT)

    lookAtCustomFrame = Frame(frame)
    lookAtCustomFrame.pack()

    X = Text(lookAtCustomFrame, height=1, width=5)
    X.insert(1.0,"0")
    X.pack(side=LEFT)
    Y = Text(lookAtCustomFrame, height=1, width=5)
    Y.insert(1.0,"0")

    Y.pack(side=LEFT)
    Z = Text(lookAtCustomFrame, height=1, width=5)
    Z.insert(1.0,"0")
    Z.pack(side=LEFT)
    def lookAtCustom():
        print('Gonna look at...', X.get(1.0,END),Y.get(1.0,END),Z.get(1.0,END))
        rs.send_robot_lookat_cmd(float(X.get(1.0,END)),float(Y.get(1.0,END)),float(Z.get(1.0,END)))
    lookAtCustomButton = Button(lookAtCustomFrame, text="Look At", command=lookAtCustom)
    lookAtCustomButton.pack(side=LEFT)

    root.mainloop()