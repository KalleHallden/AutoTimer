Tracking the desktop applications in real time and time spent on each application.

Check out this for more https://youtu.be/ZBLYcvPl1MA 

Dependencies:
- selenium

Supported OS's: 
- macOS
- Windows
- Linux

Windows Depencies:
- pywin32
- python-dateutil
- uiautomation 

Browser support:
- Safari
- Chrome

Configure as macOS LaunchAgent:
- Configure and move the example .plist file to either ~/Library/LaunchAgent or /Library/LaunchAgent
- Move autotimer.py and activity.py to directory specified in plist program arguments
- Open terminal and enter 'launchctl load ~/Library/LaunchAgent/com.example.AutoTime.plist'