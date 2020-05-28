# Aricon
Aricon is a simple GUI for ffmpeg written with python and Qt.

# Requirements:
* Python version 3.0 or higher
* PyQt

# It can:
* Burn subtitle file (.sub) to videos. (The input video file should have no sub tracks)
* Compress videos
* Convert videos to audio tracks
* Change the resulotion of videos
* Mute videos 
* Rotate videos

* More features coming soon!

# How to use:
### To Burn subtitle file: 
* Go to Subtitle Tools > Burn a sub file into the video > Select your files > After conversion is complete, Open your file.
### To Convert video file to audio file:
* Go to Video Tools > Convert to audio > Select your files > After conversion is complete, Open your file.
### To Mute the Video:
* Go to Video Tools > Mute the video > Select your files > After conversion is complete, Open your file.
### To Compress the Video (Not fully functional, but it works!):
* Go to Video Tools > Compress the video > Select your files > After conversion is complete, Open your file.
### To Change the video's resulotion:
* Go to Video Tools > Change resolution > Select your files and enter the resolution in this format : WidthxHeight > After conversion is complete, Open your file.
### To View history file:
* Go to File > History > You can view your history file and clear it or refresh it.

### I used persepolis download manager's papirus icon pack, here's their project link: 
* https://github.com/persepolisdm/persepolis
* Papirus project link: https://github.com/PapirusDevelopmentTeam/papirus-icon-theme

### Special Thanks to @nelforza for the idea, You can see the original GUI written with zenity and bash script here: 
* https://github.com/nelforza/aricon

### Again Thanks to @fliptopbox for the ffmpeg progress file
* https://github.com/fliptopbox/nuke/blob/master/python/misc/ffmpeg-progress.py
