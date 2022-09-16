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


def render_csv(cues):

	sep = "\t"

	# Print header
	print(sep.join(["Serial","TimecodeIn","TimecodeOut","Duration","TRANSLATION"]))

	count = 1
	for i in cues:
		print(sep.join([str(count),i["TimecodeIn"],i["TimecodeOut"],i["Duration"],i["Translation"]]))
		count += 1

def internalise(lines):

	cues = []

	GET_TEXT = 1
	WAITING = 2
	cue = 0	
	current_state = WAITING
	start_time = ""
	end_time = ""
	text = ""
	duration = 0
	text_line = 0

	current_cue = {}

	for line in lines:
		line = line.strip()

		if "-->" in line:
			cue += 1
			start_time = line[0:12]
			end_time = line[17:]
			duration = get_duration(start_time,end_time)
			current_state = GET_TEXT
			text_line = 0

			current_cue["TimecodeIn"] = start_time
			current_cue["TimecodeOut"] = end_time
			current_cue["Duration"] = duration

			continue

		if line == "":
			current_cue["Translation"] = text
			cues.append(current_cue)
			current_cue = {}
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
		current_cue["Translation"] = text
		cues.append(current_cue)

	return cues

def render_html(cues):

	print("""
<html>
<table>
<tr>
<th>Serial</th>
<th>TimecodeIn</th>
<th>TimecodeOut</th>
<th>Duration</th>
<th>Translation</th>
</tr>
	""")

	count = 1
	for i in cues:

		print("<tr>")
		print("<td>" + str(count) + "</td>")
		print("<td>" + i["TimecodeIn"] + "</td>")
		print("<td>" + i["TimecodeOut"] + "</td>")
		print("<td>" + i["Duration"] + "</td>")
		print("<td>" + i["Translation"] + "</td>")
		print("</tr>")

		count += 1

	print("</table></html>")



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

	# Turn SRT file into internal state
	# An array of hashes (ie. structs)
	# Fields: TimecodeIn, TimecodeOut, Duration, Translation (ie, the voiceover)

	cues = internalise(lines)

	render_csv(cues)

if __name__ == '__main__':
	main()
