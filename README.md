# Bus-and-I-O-Controller-System-

A Computer Architecture Simulation Project using ESP32 and Streamlit GUI

⟩ Overview
This project demonstrates the working of a Bus and I/O Controller System, transforming the theoretical concept of CPU–Memory–I/O communication into an interactive real-time simulation.

Using an ESP32 microcontroller as the CPU and a Streamlit-based Python GUI, the project visualizes how the Address Bus, Data Bus, and Control Bus operate together to transfer data within a computer system.

⟩ Objectives
- To simulate and visualize the working of a system bus in a computer architecture.  
- To understand the interaction between CPU, Memory, and I/O devices.  - To demonstrate real-time data transfer using serial communication between ESP32 and a PC GUI.  

⟩ System Architecture
The system follows a client-server model:
- Server (ESP32): Executes low-level bus logic and responds to commands.  
- Client (Python GUI):Sends commands to ESP32, receives responses, and updates the graphical display.
- Communication: Serial connection (via `pyserial`) at baud rate 115200.

⟩ Components Used
» Hardware
- ESP32 Microcontroller Board  
- USB Cable for Serial Communication  

» Software
- Arduino IDE – for programming ESP32  
- Python 3 – for GUI development  
- Libraries:  
  - `streamlit` (for interactive GUI)  
  - `pyserial` (for serial communication)  
  - `threading` (for real-time data updates)

⟩ Working Principle
1. GUI Setup:
The Streamlit app provides interactive controls for data read/write operations and visualizes bus states.  

2. Serial Communication:
The GUI sends commands (e.g., `DATA:10110101`) to the ESP32 and listens for responses.  

3. ESP32 Processing: 
The microcontroller simulates bus activity and sends updated bus data back to the GUI.  

4. Real-Time Visualization: 
The GUI displays Address, Data, and Control bus activity dynamically, representing actual CPU–Memory–I/O interactions.

⟩ Features
» Real-time visualization of Address, Data, and Control buses  
» Interactive GUI for bus operations  
» Serial communication between PC and ESP32  
» Educational model for Computer Architecture understanding  

⟩ How to Run
1. Flash ESP32:
   - Open the ESP32 code in Arduino IDE  
   - Select the correct COM port  
   - Upload the code to the ESP32  

2. Run GUI:
   ```bash
   pip install streamlit pyserial
   streamlit run bus_controller.py

3. Connect ESP32:
- Ensure the ESP32 is connected via USB
- The GUI will auto-detect the COM port and begin communication

⟩ Theoretical Concepts
» Address Bus: Unidirectional bus carrying memory addresses.
» Data Bus: Bidirectional bus carrying actual data.
» Control Bus: Carries control signals to manage operations (e.g., Read/Write).



