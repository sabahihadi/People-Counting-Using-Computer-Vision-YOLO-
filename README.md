People Counter using YOLO11 and ByteTrack
Project Overview
This project implements a people counting system based on YOLO11 and ByteTrack. The system detects and tracks people in a fixed-camera video, monitors a predefined virtual fence, detects ENTER and EXIT events, and continuously estimates the current occupancy inside the virtual fence.
The project generates the following outputs:
•	Annotated output video
•	CSV event log
•	JSON event log
•	Performance report
________________________________________
Project Architecture
The overall processing pipeline is illustrated below:
                +----------------------+
                |     Input Video      |
                +----------------------+
                           |
                           v
                +----------------------+
                |   YOLO11s Detection  | YOLO11s is one of the best person detectors with good speed and accuracy.
                +----------------------+
                           |
                           v
                +----------------------+
                |  ByteTrack Tracking  | ByteTrack performs very well in maintaining track during occlusion in many MOT benchmarks.
                +----------------------+
                           |
                           v
                +----------------------+
                |   Virtual Fence      | Rectangle Drawing, Foot Point Check, Inside / Outside Detection
                +----------------------+
                           |
                           v
                +----------------------+
                |   Event Manager      | Record the status of each track, Prevent duplicate counting, Record ENTER and EXIT
                +----------------------+
                     |             |
                     |             |
                     v             v
          +----------------+   +----------------+
          | CSV / JSON Log |   | Output Video   |
          +----------------+   +----------------+
                           |
                           v
                +----------------------+
                | Performance Report   |
                +----------------------+
________________________________________
Overlap and Occlusion Handling
The input video is captured using a fixed camera from a side view with a relatively low viewing angle. Therefore, temporary occlusions between people are expected.
The system handles these situations using the following strategy:
•	ByteTrack maintains object identities across consecutive frames and reduces identity switching during short-term occlusions.
•	A Virtual Fence determines whether each tracked person’s foot point is inside or outside the monitored region.
•	The Event Manager applies temporal confirmation before generating ENTER or EXIT events, reducing false counting caused by temporary tracking instability or boundary fluctuations.
•	Track information is automatically cleaned after a configurable timeout to prevent inactive tracks from remaining in memory.
________________________________________
Project Structure
PeopleCounter/

├── main.py
│
├── input/
│   └── Hike Vision.mp4
│
├── src/
│   ├── config.py           #All configurable parameters of the project are stored here.
│   ├── detector.py         #Person detector using YOLO11s.
│   ├── tracker.py          #Multi-object tracker using YOLO11s and ByteTrack.
│   ├── fence.py            #Represents the virtual fence. FOOT POINT is used to determine inside/outside.
│   ├── event_manager.py    #Applies temporal confirmation before ENTER/EXIT, reducing false counting.
│   ├── logger.py           #Save events to both CSV and JSON.
│   └── performance.py      #Generate performance report.
│
├── yolo11s.pt
│
├── tracker_configs/
│   └── bytetrack_custom.yaml    #Custom ByteTrack configuration
│
├── outputs/
│   ├── output.mp4
│   ├── events.csv
│   ├── events.json
│   └── performance_report.txt
│
├── requirements.txt       #All required Python packages
└── README.md
________________________________________
How to Run
0. Extract the project to your desired directory.
1. Set the video path in src/config.py.
2. Open the project folder in Visual Studio Code.
3. From VS Code, open a new Git Bash terminal.
4. Create a virtual environment: 
```bash
python -m venv .venv
```
5. Activate the virtual environment:
```bash
source .venv/Scripts/activate
```
After activation, the terminal prompt should start with:
```text
(.venv)
```
6. Install the required packages:
```bash
pip install -r requirements.txt
```
7. Run the application
```bash
python main.py
```
Notes:
- The `.venv` directory is **not included** in this project.
- A new virtual environment must be created before running the project.
- All required Python packages are listed in `requirements.txt`.
________________________________________
Outputs
The following files are generated after processing:
File	        Description
output.mp4	Annotated output video
events.csv	Structured event log (CSV)
events.json	Structured event log (JSON)
performance_report.txt	Performance evaluation report
________________________________________
Experimental Hardware
The project was tested on the following hardware:
•	Operating System: Windows 10 Pro
•	CPU: Intel(R) Core(TM) i7-2670QM CPU @2.20GHz, 2201 Mhz, 4 Core(s), 8 Logical Processor(s)
•	RAM: 8.00 GB
•	GPU: CPU only
•	Python Version: 3.12.3
________________________________________
Performance Evaluation
The generated "performance_report.txt" includes:
•	Total processed frames:
•	Input video FPS:
•	Processing throughput (FPS): XXX FPS
•	Pipeline latency:
o	Average latency: XXX ms
o	Minimum latency: XXX ms
o	Maximum latency: XXX ms
o	Latency standard deviation: XXX ms
•	Total processing time: XXX sec
•	Number of ENTER events: XXX
•	Number of EXIT events: XXX
•	Maximum occupancy: XXX
•	Final occupancy: XXX
Pipeline latency is measured from frame acquisition to final output generation, including:
Frame acquisition, YOLO11 inference, ByteTrack tracking, Virtual fence evaluation, Event management, Visualization
________________________________________
Notes
•	The system assumes a fixed camera.
•	The monitored area is defined by a rectangular virtual fence.
•	ENTER and EXIT events are generated only after temporal confirmation to improve counting stability.
•	Output logs are generated in both CSV and JSON formats for further analysis.
________________________________________
Limitations
•	The system is designed for fixed-camera scenarios and assumes a static camera throughout the video.
•	Long-term occlusions or complete disappearance of a person may lead to track fragmentation or ID reassignment.
•	Detection performance may decrease for heavily occluded.
•	The virtual fence is manually configured and should be adjusted if the camera position or scene changes.
________________________________________
Future Improvements
Possible future extensions include:
•	Direction-aware counting
•	Person Re-Identification (Re-ID)
•	Multi-camera support
•	Real-time RTSP camera processing
•	Web-based monitoring dashboard
•	Stronger detectors and tracking algorithms
