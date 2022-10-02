Subtitles to CSV
================

Convert a subtitle file (SRT) to a basic tab delimited file (CSV), or optionally a HTML table. This process adds in the duration as a column. It can save you from tediously recording timecodes of points in a video, if you happen to be doing that manually.

## Use Case
I use subtitling software to create audio description for videos. I write the narration as subtitles in-between the gaps in the dialouge. I then take the SRT subtitle file and uses this script to generate a cue list which has the cue number, start and end times, duration and the actual text for the narrator.

It's very similar to the [Netflix audio description format](https://partnerhelp.netflixstudios.com/hc/en-us/articles/360001577767-Template-Audio-Description-Script), although it includes an extra column ("duration").

You can also use it to annotate videos if all you need at the end of the day is the timecode, and the text you want to associate with it.


## Example

Once you have annotated your video you save a SRT file formatted like this:

```
48
00:08:04,296 --> 00:08:10,526
The Doctor motions to Ian and Barbara, who get up. They slide open the cabin door and leave the ship.

49
00:08:23,975 --> 00:08:28,326
He gives her a warm, compassionate smile as she sits back down at the table
```

Use the python3 script on the command-line to convert the file to a tabular format, like this:

```
$python3 str2csv.py subtitles.srt csv > subtitles.csv
```

or

```
$python3 str2csv.py subtitles.srt html > subtitles.html
```

This will create a CSV or HTML file formatted like this:

|Serial|TimecodeIn|TimecodeOut|Duration|TRANSLATION|
|---|-----|---|--------|---------|
|48|00:08:04,296|00:08:10,526|00:06.23|The Doctor motions to Ian and Barbara, who get up. They slide open the cabin door and leave the ship.|
|49|00:08:23,975|00:08:28,326|00:04.35|He gives her a warm, compassionate smile as she sits back down at the table|

When opening the CSV file in your spreadsheet software, you may need to tell it that it is *tab delimited* to open correctly.


## About

This is a reasonably quick and dirty script I wrote to solve a problem. It is quite a lateral use of subtitling software and SRT files. It probably is not terribly robust, but hopefully it is of some use to someone.



