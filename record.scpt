set theCurrentDate to current date
set dateTime to short date string of theCurrentDate & space & time string of theCurrentDate
set P to offset of "/" in dateTime
set dateTime to text 1 through (P - 1) of dateTime & "-" & text (P + 1) through -1 of dateTime
set P to offset of "/" in dateTime
set dateTime to text 1 through (P - 1) of dateTime & "-" & text (P + 1) through -1 of dateTime
set theFilePath to "/Users/iamfire297/Desktop/PythonDev/SecurityBot/CAM " & dateTime & ".mov"

tell application "QuickTime Player"
     set newMovieRecording to new movie recording
     tell newMovieRecording
           start
           delay 6
           pause
           save newMovieRecording in POSIX file theFilePath
           stop
           close newMovieRecording
     end tell
end tell