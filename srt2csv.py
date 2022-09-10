import sys
import datetime
from datetime import *

def get_duration(a,b):

	start = datetime.strptime(a, "%H:%M:%S,%f")
	end = datetime.strptime(b, "%H:%M:%S,%f")

	duration = end - start

	duration = str(duration)[2:]
	if len(duration) > 8:
		duration = duration[0:8]

	return(duration)


def main():

	n = len(sys.argv)
	if n < 2:
		print("Not enough arguments")
		exit()

	file_name = sys.argv[1]

	try:
		file1 = open(file_name, 'r')
		lines = file1.readlines()
		file1.close()
	except:
		print("Unable to open file")
		exit()

	GET_TEXT = 1
	WAITING = 2
	sep = "\t"
	cue = 0	
	current_state = WAITING
	start_time = ""
	end_time = ""
	text = ""
	duration = 0
	text_line = 0

	print(sep.join(["Serial","TimecodeIn","TimecodeOut","Duration","TRANSLATION"]))

	for line in lines:
		line = line.strip()

		if "-->" in line:
			cue += 1
			start_time = line[0:12]
			end_time = line[17:]
			duration = get_duration(start_time,end_time)
			current_state = GET_TEXT
			text_line = 0
			continue

		if line == "":
			print(str(cue) + sep + start_time + sep + end_time + sep + duration + sep +  text)
			text = ""
			current_state = WAITING
			continue

		if current_state == GET_TEXT:
			if text_line == 0:
				text += line
				text_line += 1
			else:
				text += " " + line

	if current_state == GET_TEXT:
		print(str(cue) + sep + start_time + sep + end_time + sep + duration + sep +  text)

if __name__ == '__main__':
	main()
