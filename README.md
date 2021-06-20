# AutoTimer

---
### Here's original writing by original author: [Kalle Hallden](https://github.com/KalleHallden)
Auto timer is used to track the desktop applications in real time and time spent on each application.

Check out this for more https://youtu.be/ZBLYcvPl1MA

#### Dependencies:

- selenium

#### Windows Depencies

- pywin32
- python-dateutil
- uiautomation

---
### Here's what I added
#### Environment

- Windows 10
- IDE: PyCharm
- Python 3.6

#### Windows Dependencies

- pywin32
- python-dateutil
- uiautomation

#### Dependencies I deleted

- AppKit
- Foundation

---
### Explanation
1. I deleted the macOS part because I found that downloading AppKit package is a trouble thing in Windows OS. 

2. I updated the python version from 2.7 to 3.6, and I deleted the old env dir and add a new one, which is named venv.

3. There are still have some bugs. For example, When I open a page in Chrome, the program fail to track it. And when I open a login page with a Form saved in Chrome, the cmd will print the Form's content.