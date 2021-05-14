# PyCollab


Python Blackboard Collaborate script to download recording based on Blackboard Learn Course ID, or Blackboard Learn Course UUID, Moodle plugin session ID, Moodle LTI Tool.
and get:
<ul>
<li>Recording Report in a CSV file (Recording_ID, Storage Size, Duration, Creation Date, Duration) on /reports folder
</li>
<li>Downloads local folder that will receive the MP4 video <i>if the recording have chats, those will be downloaded too.</i> Recording  and Chat csv files will be on /downloads folder
</li>
<li>Command line attributes depending on the scenario: Learn Course,Blackboard Learn Course UUID, Moodle plugin session ID, Moodle LTI Tool.
</li>

<li><b>This script is NOT supported on Behind the Blackboard.</b></li>
</ul>




## 1. Python Instalation 
You need to have installed from Python 3.7 to Python 3.8.6 

Will depent on Computer operation system how Python is referenced on command line tool:
<br> 
 Mac OS: 
 <ul> 
 <li>(HomeBrew)  brew install python3</li>
 <li>normally python3 is the alias to run python scripts when install python 3.7+</li>
</ul> 
Windows OS: 
<ul> 
 <li>Python 3.9+ still do not support PEP 157 package instalation, so must be installed Python 3.8.6 (x86_64 or x86 installer depending on your computer processor)</li>
 <li>Normally python is the alias to run python scripts when install python from version 3.7 to Python 3.8.6</li>
</ul>
<br>
<br>

## 2. Install script requirements

MacOS:

```
pip install -r requerimientos.txt
```

Windows:


```
python -m pip install -r requerimientos.txt
```

## 3. Add Blackboard Collaborate and Learn Credentials
<ul>
<li>Scenario 1:  Learn to Collaborate search for recordings</li>
<li>Scenario 2: Moodle to Collaborate search for recordings</li>
<li>Scenario 3: Collab Admin Institutional Reports</li>
</ul>

<br>
if you have the scenario 1 you need to insert both Learn and Collaborate credentials 
<br>
If you have the scenario 2 or scenario 3, yo only need to insert Collaborate credentials, but DO NOT REMOVE the key:value association of Learn credentials section from the Config.py file.
<br>

```
edit content of Config.py file
```


### Note: Backboard Credentials / Integration on Learn

In order to get the Learn credentials, go to <i>developer.blackboard.com</i> and register from there to grab the Learn credentials for their application, it is also imperative to remind them that they are creating an application based on your code, so they need to register as a developer.Then on your Blackboard Learn environment, as admin role user, go to Rest API Integration a create an integration using data provided from developer.blackboard.com before.<br>
<p>Check <a href="https://github.com/zerausolrac/PyCollab/blob/master/LearnPyCollab.pdf">Learn Integration</a></p>

### Note: Backboard Credentials for Collaborate

Now, for Collaborate production they CAN and MUST create a ticket on behind the blackboard requesting their credentials.

## 4. Modify external file depending on scenario
```
edit learn_courses.txt file
edit learn_uuids.txt file
edit moodle_lti_id.txt file
edit moodle_plugin_sessions.txt file

for Scenario 3
downlaod the Collaborate Admin Institutional Attendance Report and put on the root directoriy
downlaod Collaborate Admin Institutional Recordings Report and put on the root directoriy
```


## 5. Run the script

<ul>
<li>Collab.py -h</li>
<li>CollabMoodle.py -h</li>
<li>CollabReport.py -h</li>
<li>CollabMinutes.py -h</li>
<li>CollabRecordings.py -h</li>
<li>CollabRecordingsDownload.py -h</li>
</ul>
<br>

## Scenario 1
### Search recording from Blackboard Learn to Collaborate  

<li>if you have the Blackboard Learn course id(s) as input data on the file learn_courses.txt, where -w is a value of weeks back for as starting point of searching for recordings:
<B>Note:</B> <i>if the recording have chats, those will be downloaded too.</i>
</li>

```
python3 Collab.py -f learn_courses.txt -w 10   
```
<li>
if you have the Blackboard Learn UUID(s) as input data on the file learn_uuids.txt, where -w is a value of weeks back for as starting point of searching for recordings:
<B>Note:</B> <i>if the recording have chats, those will be downloaded too.</i>
</li>

```
python3 Collab.py -e learn_uuids.txt -w 10   
```

<b>Report Learn-Collaborate</b>
<li>
If you need to know about recording storage size, duration and  recording ID before download any recording you can create a report, where -f is point to learn_courses.txt file that have Blackboard Learn courses ID listed by row, and -w is a value of weeks back for as starting point of searching for recordings.
<b>Note:</b>If the recording has public_access disabled, the recording won't be readed by script and will 403 report will be generated with list recording_id.

</li>

```
python3 CollabReport.py -f learn_courses.txt -w 10
```


## Scenario 2
### Search recording from Moodle to Collaborate  

<p>If you have the Moodle with Plugin Integration</p>

<li>
Add one per row,the sessionuid column values from mdl_collaborate table from Moodle database on the file moodle_plugin_sessions.txt.
</li>
<li>
-w is a value of weeks back for as starting point of searching for recordings
</li>
<li>
If the recording have chats, those will be downloaded too.</i>
</li>

<p>Then run the command:</p>

```
python3 CollabMoodle.py -s moodle_plugin_sessions.txt -w 10   
```


<p>If you have the Moodle with LTI Integration</p>

<li>
Add one per row, the id column values from mdl_lit table from Moodle database on the file moodle_lti_id.txt, check that course column value from from mdl_lit table match with id value from mdl_course table.
</li>
<li>
 -w is a value of weeks back for as starting point of searching for recordings
 <li>
If the recording have chats, those will be downloaded too.</i>
</li>

<p>Then run the command:</p>

```
python3 CollabMoodle.py -l moodle_lti_id.txt -w 10   
```


## Scenario 3
### Collaborate Admin Institutional Reports 

<b>Report Minutes on Callaborate from AttendeeReport</b>
<li>
if you need to identify the amount of minutes spend in Collaborate session,first  you need to download the Collaborate Admin Institutional Attendance Report according to your zone (ca:Canada, us: USA), then use the script CollabMinutes.py with the parameter -f that point to the file previously downloaded.
</li>

```
python3 CollabMinutes.py -f AttendeeReport.csv   
```

<br>
<br>

<b>Report RecordingId from Collaborate RecordingsReport</b>
<li>
if you need to get information about recordingId, storage size, first you need to download the Collaborate Admin Institutional Recording Report according to your zone (ca:Canada, us: USA), then use the script CollabRecordings.py with the parameter -f that point to the file previously downloaded. 
<b>Note:</b>If the recording has public_access disabled, the recording won't be readed by script and will 403 report will be generated with list recording_id.
</li>

```
python3 CollabRecordings.py -f RecordingsReport.csv   
```
<br>
<br>

<b>Download RecordingId from Collaborate RecordingsReport</b>
<li>
if you need to download recordings, first you need to download the Collaborate Admin Institutional Recording Report according to your zone (ca:Canada, us: USA), then use the script CollabRecordingsDownload.py with the parameter -f that point to the file previously downloaded. 
<b>Note:</b>If the recording has public_access disabled, the recording won't be readed by script and will 403 report will be generated with list recording_id.
</li>

```
python3 CollabRecordingsDownload.py -f RecordingsReport.csv   
```
<br>
<br>



## Delete recordings
### Considerations

<b>About deletion process</b>
<ul>
<li>
Use this feature at your own risk
</li>
<li>
 It is soft-deletion, this means, deletion process will remove recording after 30 days from deletion day
</li>
<li>
 When deleted from API, It is not taken in count for total calculation of storage for Collaborate Entitlements
</li>
<li>
On reporting only takes in count Blackboard Learn-Collab in Blackboard Data, there is no way to caculate Collab Scheduler total storage using API
</li>
<li>
It is not possible to recover a deleted recording using Collaborate’s API, for that cases will need to create a Blackboard Support ticket  for it</li>

</ul>

```
python3 CollabDeleteRecordings.py -f recordingsid_list.txt   
```

Where <b>recordingids_list.txt </b> is a text-plain o-column-list with all recordingsId that will be deleted from Blackboard Collaborate instance.






<pre>
  ____    _                  _      _                                  _ 
 |  _ \  | |                | |    | |                                | |
 | |_) | | |   __ _    ___  | | __ | |__     ___     __ _   _ __    __| |
 |  _ <  | |  / _` |  / __| | |/ / | '_ \   / _ \   / _` | | '__|  / _` |
 | |_) | | | | (_| | | (__  |   <  | |_) | | (_) | | (_| | | |    | (_| |
 |____/  |_|  \__,_|  \___| |_|\_\ |_.__/   \___/   \__,_| |_|     \__,_|
                                                                             
</pre>

# Tutorials

<a href="https://www.youtube.com/watch?v=UxKZvBw_-NU" target="new">Downloading - English</a>
<br>
<br>
<a href="https://www.youtube.com/watch?v=0ov-HZJeAE0&feature=youtu.be" target="new"> Downloading - Español</a>