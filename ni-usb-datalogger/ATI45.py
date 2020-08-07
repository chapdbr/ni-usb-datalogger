# Import libraries
import nidaqmx.stream_readers
import numpy as np
import time
import datetime
import subprocess
import os
import msvcrt
import math

# ATI mini45 SI-120 calibration matrix
###################################################################################################
calibration_ati45 = np.array([[0.15596, 0.05364, -0.29616, -22.76401, 0.71258, 22.77619],
						[0.17628, 25.86714, -0.34444, -13.07013, -0.42680, -13.39725],
						[29.42932, -1.68566, 29.50395, -0.09508, 29.75563, -1.01253],
						[0.00754, 0.22624, -0.47721, -0.11727, 0.47877, -0.12927],
						[0.53998, -0.02617, -0.25730, 0.19768, -0.29711, -0.19153],
						[0.00107, -0.33260, -0.00357, -0.34021, -0.01832, -0.33980]])
###################################################################################################

class sensor(object):
	"""ATI load cell class."""
	def __init__(self, name, calibration, r):
		"""Initialise class."""
		self.data = np.empty([6,]) # force & torque array
		self.name = name
		self.calibration = calibration
		self.r = r # length of the tether

	def tare(self):
		"""Tare with user input"""
		self.tare_input = np.empty([6,])
		print("Press ENTER to tare")
		while input() != '':
			pass
		self.my_multi_channel_ai_reader.read_one_sample(self.tare_input, timeout=10)
		print("Tared")

	def tare_quick(self):
		"""Instant tare."""
		self.my_multi_channel_ai_reader.read_one_sample(self.tare_input, timeout=10)
		print("Tared")

	def init_stream(self):
		"""Init nidaqmx stream."""
		self.task = nidaqmx.Task()
		self.task.ai_channels.add_ai_voltage_chan("Dev1/ai0:5","analog_input",nidaqmx.constants.TerminalConfiguration.RSE)
		#print(self.channel1.ai_term_cfgs) # debug
		self.my_stream = nidaqmx._task_modules.in_stream.InStream(self.task)
		self.my_multi_channel_ai_reader = nidaqmx.stream_readers.AnalogMultiChannelReader(self.my_stream)

	def init_time(self):
		"""Init time."""
		self.last_time = time.time()
		self.start_time = self.last_time

	def read_data(self):
		"""Read and log sensor data."""
		# Read data from nidaqmx stream
		self.my_multi_channel_ai_reader.read_one_sample(self.data, timeout=10)
		self.data_tared = np.array(self.data - self.tare_input)
		self.data_tared = np.reshape(self.data_tared,(6, 1))
		self.data_tared_cal = np.matmul(self.calibration,self.data_tared)
		# Calculate time
		self.now = time.time()
		self.elapsed_time = str(self.now - self.start_time)
		# Define forces
		self.fx = self.data_tared_cal[0, 0]
		self.fy = self.data_tared_cal[1, 0]
		self.fz = self.data_tared_cal[2, 0]
		self.fr = math.sqrt(self.fx**2+self.fy**2+self.fz**2)
		# Calculate position
		self.theta = math.atan2(self.fy, self.fx)
		self.phi = math.acos(self.fz/self.fr)
		self.x = self.r*math.cos(self.theta)*math.sin(self.phi)
		self.y = self.r*math.sin(self.theta)*math.sin(self.phi)
		self.z = self.r*math.cos(self.phi)
		# Log data
		self.log.write(str(self.elapsed_time)+','+
					   str(self.fx) + ',' +
					   str(self.fy) + ',' +
					   str(self.fz) + ',' +
					   str(self.fr) + ',' +
					   str(self.x) + ',' +
					   str(self.y) + ',' +
					   str(self.z)+'\n')
		return self.data_tared_cal

	def init_savefile(self):
		"""Create savefile."""
		self.filename = self.name + "_savefile_" + datetime.datetime.now().strftime("%Y-%B-%d_%I-%M-%p") + ".txt"
		#self.filename = self.name + ".txt"
		self.log = open(self.filename, 'w+',1)
		self.log.write('elapsed_time (s)' + ',' +
					   'fx (N)' + ',' +
					   'fy (N)' + ',' +
					   'fz (N)' + ',' +
					   'fr (N)' + ',' +
					   'x (m)' + ',' +
					   'y (m)' + ',' +
					   'z (m)' + '\n')

	def close(self):
		"""Close nidaqmx stream."""
		self.task.close()
		self.log.close()

def uinput_plot_forces():
	"""Ask user to plot forces."""
	print("Do you want to plot the forces? <y/n>: ")
	repeat = True
	while repeat:
		uinput = input()
		if uinput == 'y':
			dir_path = os.path.dirname(os.path.realpath(__file__)) # Dir path on Windows
			repeat = False
			plotting_forces = True
			print('Starting the plotting process...')
			p1 = subprocess.Popen(['python', 'plot_forces.py', 'ati45.filename'])
		elif uinput == 'n':
			repeat = False
			plotting_forces = False
			p1 = False
		else:
			print("Please press the right key.")
	return plotting_forces, p1

def uinput_plot_pos():
	"""Ask user to plot position."""
	print("Do you want to plot the position? <y/n>: ")
	repeat = True
	while repeat:
		uinput = input()
		if uinput == 'y':
			dir_path = os.path.dirname(os.path.realpath(__file__)) # Dir path on Windows
			repeat = False
			plotting_pos = True
			print('Starting the plotting process...')
			p2 = subprocess.Popen(['python', 'plot_position.py', 'ati45.filename'])
		elif uinput == 'n':
			repeat = False
			plotting_pos = False
			p2 = False
		else:
			print("Please press the right key.")
	return plotting_pos, p2

def read_n_log_data():
	"""Read and log data until ESC key is pressed."""
	print('Reading and logging data')
	print('Press T to tare and ESC key to exit...')
	while True:
		ati45.read_data()
		time.sleep(0.01) # 100 Hz
		if msvcrt.kbhit():
			key = ord(msvcrt.getch())
			if key == 27: # escape key
				break
			elif key == 116: # t key
				ati45.tare_quick()
if __name__ == '__main__':
	# Create sensor class and init
	ati45 = sensor('ATI45', calibration_ati45, 10)
	ati45.init_savefile()
	ati45.init_stream()
	ati45.tare()
	ati45.init_time()
	ati45.read_data()

	# Ask for plots
	(plotting_forces, p1) = uinput_plot_forces()
	(plotting_pos, p2) = uinput_plot_pos()

	# Read and log data
	read_n_log_data()

	# Terminate subprocesses
	if plotting_forces:
		p1.kill()
		p1.terminate()
	if plotting_pos:
		p2.kill()
		p2.terminate()
	ati45.close() # end task