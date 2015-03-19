import os, sys, inspect, thread, time
src_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
arch_dir = '../lib'
sys.path.insert(0, os.path.abspath(os.path.join(src_dir, arch_dir)))

import Leap
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture
import time
import fluidsynth

# --------------------------------------------------------------------------
# --------------------------------------------------------------------------
fs = fluidsynth.Synth()
fs.start()

sfid = fs.sfload("YAMAHA DX7Piano.SF2")
fs.program_select(0, sfid, 0, 0)

scale = (60, 62, 64, 65, 67, 69, 71, 72)
play = [False, False,False, False, False]
# --------------------------------------------------------------------------
# --------------------------------------------------------------------------

class SampleListener(Leap.Listener):
	finger_names = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
	bone_names = ['Metacarpal', 'Proximal', 'Intermediate', 'Distal']
	state_names = ['STATE_INVALID', 'STATE_START', 'STATE_UPDATE', 'STATE_END']

	def on_init(self, controller):
		print "Initialized"

	def on_connect(self, controller):
		print "Connected"

		# Enable gestures
		controller.enable_gesture(Leap.Gesture.TYPE_KEY_TAP);

	def on_disconnect(self, controller):
		# Note: not dispatched when running in a debugger.
		print "Disconnected"

	def on_exit(self, controller):
		print "Exited"

	def on_frame(self, controller):
		# Get the most recent frame and report some basic information
		frame = controller.frame()

		# print "Frame id: %d, timestamp: %d, hands: %d, fingers: %d, tools: %d, gestures: %d" % (
		#       frame.id, frame.timestamp, len(frame.hands), len(frame.fingers), len(frame.tools), len(frame.gestures()))

		# Get hands
		for hand in frame.hands:

			handType = "Left hand" if hand.is_left else "Right hand"

			# print "  %s, id %d, position: %s" % (
			#     handType, hand.id, hand.palm_position)

			# Get fingers
			for finger in hand.fingers:

				# print "    %s finger, id: %d, length: %fmm, width: %fmm" % (
				#     self.finger_names[finger.type()],
				#     finger.id,
				#     finger.length,
				#     finger.width)

				# Get bones
				# for b in range(0, 4):
				#     bone = finger.bone(b)
				#     print "      Bone: %s, start: %s, end: %s, direction: %s" % (
				#         self.bone_names[bone.type],
				#         bone.prev_joint,
				#         bone.next_joint,
				#         bone.direction)

				bone = finger.bone(3)
				if bone.next_joint[1] < 90:
					print self.finger_names[finger.type()]
					if play[finger.type()] == False:
						play[finger.type()] = True
						fs.noteon(0, scale[finger.type()], 127)
				else:
					if play[finger.type()] == True:
						fs.noteoff(0, scale[finger.type()])
						play[finger.type()] = False


	def state_string(self, state):
		if state == Leap.Gesture.STATE_START:
			return "STATE_START"

		if state == Leap.Gesture.STATE_UPDATE:
			return "STATE_UPDATE"

		if state == Leap.Gesture.STATE_STOP:
			return "STATE_STOP"

		if state == Leap.Gesture.STATE_INVALID:
			return "STATE_INVALID"

def main():
	# Create a sample listener and controller
	listener = SampleListener()
	controller = Leap.Controller()

	# Have the sample listener receive events from the controller
	controller.add_listener(listener)

	# Keep this process running until Enter is pressed
	print "Press Enter to quit..."
	try:
		sys.stdin.readline()
	except KeyboardInterrupt:
		pass
	finally:
		# Remove the sample listener when done
		controller.remove_listener(listener)


if __name__ == "__main__":
	main()
