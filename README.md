Please use this repository to maintain your work for the team project.

Also please fill the following details:

- Team name: Operation Bravo
- Students (SCS username - Name):
	- tiie2231@scs.ubbcluj.ro - Tamas Florin
	- svie2228@scs.ubbcluj.ro - Stanila Vlad
	- taie2233@scs.ubbcluj.ro - Tili Adrian
	- umie2239@scs.ubbcluj.ro - Ungur Maria

## Project idea:
Meeting room monitoring system(provide information on the number persons in the room).

This application demonstrates how to use a camera in order to detect the number of persons in a room. 
The application is provided as a web page where the user is provided with the information.
The web page communicates with a machine learning server via REST and outputs the received prediction.

## PIServer
The PI server is used in order to retrieve screenshots from a particular meeting room.
The images are used by the machine learning model in order to make a prediction regarding
the number of persons in the room.

## Machine Learning model server
The machine learning server retrieves images from the PIServer and predicts the number
of persons from that image.
The server communicates with the client via REST calls.

## Client
The client is provided as a web page created using React and provides a table 
containing each room and the number if persons for that particular room.

## Pre-requisites

- Android Things compatible board
- Android Studio 2.2+
- 1 Android Things compatible camera

## Schematics

![Schematics for Raspberry Pi 3](schematics.jpg)

## Build and install

On Android Studio, click on the "Run" button.

If you prefer to run on the command line, type

```bash
./gradlew installDebug
adb shell am start ro.ubbcluj.cs.tamasf.roomspy/.MainActivity
```

If you have everything set up correctly, the web page will reveive information from the server.

=============

Due: last laboratory.
	Either May 16th or May 23rd, depending on your laboratory frequency.
	Please note that we are obeying the faculty student group assignments.
Details:
- A team of 4 or 5 students to tackle a real-world problem.
- Choose an existing project proposed by the lab instructor.
- Define a new one, together with the lab instructor.
Expected outcome:
- The source code should be hosted in this github classroom repository.
- A webpage presenting the project results, similar to:
	https://androidthings.withgoogle.com/#!/samples/doorbell
- A short video presenting the results.

