import re
from dateutil.parser import *

text='''
Hi All,

PFA the list of shortlisted candidates for the online test of AXIS Bank.

-----
Google Hackathon
Date:25-12-2016
Time:10AM
Venue:New Sac Conference Room
-----

-----
Spirit
Date:29-12-2016
Time:6PM
Venue:Football Field
-----

i) CSE 4th Yr Lab : MnC+ CSE+ ME+ EP +BT + CST
ii) Main CC : CL+ CE + EEE/ECE

Please Note:

i) All of you need to bring earphones
ii) Those who have test in CSE 4th Yr Lab need to bring laptop and LAN cable.

Regards,

CCD
'''

pattern = '^-----$\n^(.*)$\n^Date:(.*)$\n^Time:(.*)$\n^Venue:(.*)$\n^-----$'
matches = re.findall(pattern, text, re.I|re.M)
print matches
print len(matches)
# print parse(date[0])
