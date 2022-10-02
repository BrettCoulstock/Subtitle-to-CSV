import sys
import datetime
from datetime import *
import argparse

def get_duration(a,b):

	start = datetime.strptime(a, "%H:%M:%S,%f")
	end = datetime.strptime(b, "%H:%M:%S,%f")

	duration = end - start

	duration = str(duration)[2:]

	# Truncate if too long
	if len(duration) > 8:
		duration = duration[0:8]

	return(duration)


def internalise(lines):

	""" Convert an SRT file into an internal data structure """

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


def render_csv(cues):

	""" Render the internal data structure into tab delimited CSV data """

	sep = "\t"

	# Print header
	print(sep.join(["Serial","TimecodeIn","TimecodeOut","Duration","TRANSLATION"]))

	count = 1
	for i in cues:
		print(sep.join([str(count),i["TimecodeIn"],i["TimecodeOut"],i["Duration"],i["Translation"]]))
		count += 1


def render_html(cues):

	""" Render the internal data structure into a html file as a table """

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

	# Process command line options

	# ... create
	parser = argparse.ArgumentParser(description="Convert a subtitle file (SRT) to either a basic tab delimited file (CSV) or a table in a HTML file.")

	# ... add arguments
	parser.add_argument("file_name", help="The name of the SRT subtitle file to convert")
	parser.add_argument("output_format", help="Output format. Valid values are 'html' and 'csv'.", choices=['html','csv'], default="csv")

	# ... parse
	args = parser.parse_args()

	try:
		file1 = open(args.file_name, 'r')
		lines = file1.readlines()
		file1.close()
	except:
		print("Unable to open file")
		exit()

	# Turn SRT file into internal state
	# An array of hashes (ie. structs)
	# Fields: TimecodeIn, TimecodeOut, Duration, Translation (ie, the voiceover)
	# Fieldnames based on Netflix Audio Description template + duration

	cues = internalise(lines)

	if args.output_format == 'html':
		render_html(cues)
	else:
		render_csv(cues)

if __name__ == '__main__':
	main()
