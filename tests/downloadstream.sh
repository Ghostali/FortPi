# required: ffmpeg (e.g. from homebrew), terminal-notifier from https://github.com/alloy/terminal-notifier 
# you can schedule this with launchd to run e.g. weekly

# Specify in seconds how long the script should record (default here is 1 hour).
seconds=15

# Date format for the recording file name
DATE=`date "+%d-%m-%y_%H-%M"`

# start ffmpeg recording
ffmpeg -re -i http://192.168.0.29:5000/imgstream_feed -c copy -bsf:a aac_adtstoasc recording_$DATE.mp4 &

# notification that recording has started
if [ "$(pgrep -P $$ 'ffmpeg')" ]
then
	/Applications/terminal-notifier.app/Contents/MacOS/terminal-notifier -title 'ffmpeg' -message "is recording now" -sender 'com.apple.Terminal'
else
	/Applications/terminal-notifier.app/Contents/MacOS/terminal-notifier -title 'ffmpeg' -message "is not recording!" -sound Funk -sender 'com.apple.Terminal'
	exit 42
fi

# check every 30 seconds for $seconds to make sure ffmpeg is still running
START=`date +%s`
while [ $(( $(date +%s) - $seconds )) -lt $START ]; do
	if [ -z "$(pgrep -P $$ 'ffmpeg')" ]
    	then
       		/Applications/terminal-notifier.app/Contents/MacOS/terminal-notifier -title 'ffmpeg' -message "is no longer running" -sound Funk -sender 'com.apple.Terminal'
  	fi
	sleep 30
done

# notification when time is up
/Applications/terminal-notifier.app/Contents/MacOS/terminal-notifier -title 'ffmpeg' -message "recording finished" -sound default -sender 'com.apple.Terminal'

# stop ffmpeg (using this because stopping ffmpeg via -t for duration turned out to be extremely unreliable)
kill $(pgrep -P $$ 'ffmpeg')