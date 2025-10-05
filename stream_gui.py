import streamlit as st
import serial
import threading
import time
import random
import queue
from serial.tools import list_ports

# Set page configuration
st.set_page_config(
    page_title="ESP32 Bus Controller System",
    page_icon="🔌",
    layout="wide"
)

# Initialize session state variables
if 'serial_conn' not in st.session_state:
    st.session_state.serial_conn = None
if 'is_running' not in st.session_state:
    st.session_state.is_running = False
if 'current_led_status' not in st.session_state:
    st.session_state.current_led_status = "red"
if 'data_queue' not in st.session_state:
    st.session_state.data_queue = queue.Queue()
if 'last_received_data' not in st.session_state:
    st.session_state.last_received_data = "No data received"
if 'connection_status' not in st.session_state:
    st.session_state.connection_status = "Disconnected"
if 'available_ports' not in st.session_state:
    st.session_state.available_ports = []

# Initialize component data
component_defaults = {
    'cpu_data': "00000000",
    'memory_data': "00000000", 
    'io_data': "00000000",
    'address_bus': "00000000",
    'data_bus': "00000000",
    'control_bus': "00000000"
}

for key, value in component_defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

def get_available_ports():
    """Get list of available serial ports"""
    ports = list_ports.comports()
    return [port.device for port in ports]

def connect_esp32(com_port):
    try:
        if st.session_state.serial_conn and st.session_state.serial_conn.is_open:
            st.session_state.serial_conn.close()
            
        st.session_state.serial_conn = serial.Serial(
            com_port, 
            115200, 
            timeout=1,
            write_timeout=1
        )
        time.sleep(2)  # Wait for connection to establish
        
        # Clear any existing data in the buffer
        st.session_state.serial_conn.reset_input_buffer()
        st.session_state.serial_conn.reset_output_buffer()
        
        st.session_state.connection_status = f"Connected to ESP32 on {com_port}"
        return True, st.session_state.connection_status
    except Exception as e:
        error_msg = f"Connection failed: {str(e)}"
        st.session_state.connection_status = error_msg
        return False, error_msg

def process_data():
    # Simulate CPU operation
    st.session_state.cpu_data = f"{random.randint(0, 255):08b}"
    st.session_state.address_bus = f"{random.randint(0, 15):04b}{random.randint(0, 15):04b}"
    st.session_state.control_bus = "RD" + f"{random.randint(0, 3):02b}" + "WR" + f"{random.randint(0, 3):02b}"
    
    # Simulate memory operation
    st.session_state.memory_data = f"{random.randint(0, 255):08b}"
    st.session_state.data_bus = st.session_state.memory_data
    
    # Simulate I/O operation
    st.session_state.io_data = f"{random.randint(0, 255):08b}"
    st.session_state.data_bus = st.session_state.io_data

def read_serial():
    if (st.session_state.serial_conn and 
        st.session_state.serial_conn.is_open and 
        st.session_state.serial_conn.in_waiting > 0):
        try:
            line = st.session_state.serial_conn.readline().decode('utf-8').strip()
            if "LED_STATUS:" in line:
                status = line.split(":")[1]
                st.session_state.current_led_status = status
            elif "DATA:" in line:
                data = line.split(":")[1]
                st.session_state.last_received_data = data
            elif "ACK:" in line:
                data = line.split(":")[1]
                st.session_state.last_received_data = f"ACK: {data}"
            elif "SYSTEM:" in line:
                st.session_state.connection_status = f"ESP32: {line.split(':')[1]}"
        except UnicodeDecodeError:
            pass
        except Exception as e:
            st.session_state.connection_status = f"Read error: {str(e)}"

def send_data_to_esp32():
    if st.session_state.serial_conn and st.session_state.serial_conn.is_open:
        data = f"{random.randint(0, 255):08b}"
        try:
            st.session_state.serial_conn.write(f"DATA:{data}\n".encode())
            return f"Sent: {data}"
        except Exception as e:
            return f"Failed to send data: {str(e)}"
    return "Not connected to ESP32"

def start_system(com_port):
    success, message = connect_esp32(com_port)
    if success:
        st.session_state.is_running = True
        # Start a thread to periodically read from serial
        threading.Thread(target=serial_read_loop, daemon=True).start()
    return message

def stop_system():
    st.session_state.is_running = False
    if st.session_state.serial_conn and st.session_state.serial_conn.is_open:
        st.session_state.serial_conn.close()
    st.session_state.serial_conn = None
    st.session_state.connection_status = "Disconnected"
    return "System stopped"

def serial_read_loop():
    while st.session_state.is_running:
        try:
            read_serial()
            time.sleep(0.1)
        except:
            time.sleep(1)

# Streamlit UI
st.title("🚌 ESP32 Bus Controller System")
st.markdown("Simulating data movement via buses between CPU, memory, and I/O devices")

# Get available ports
st.session_state.available_ports = get_available_ports()

# Connection section
col1, col2 = st.columns(2)
with col1:
    if st.session_state.available_ports:
        com_port = st.selectbox("COM Port", st.session_state.available_ports, index=0)
    else:
        com_port = st.text_input("COM Port", value="COM8")
        st.warning("No serial ports detected. Please enter manually.")
    
    status = st.info(st.session_state.connection_status)
    
    col1a, col1b = st.columns(2)
    with col1a:
        if st.button("🟢 Start System", type="primary"):
            result = start_system(com_port)
            status.info(result)
    with col1b:
        if st.button("🔴 Stop System"):
            result = stop_system()
            status.info(result)

with col2:
    send_status = st.empty()
    if st.button("📤 Send Data to ESP32"):
        result = send_data_to_esp32()
        send_status.success(result)
    
    st.markdown("---")
    st.subheader("ESP32 Status")
    led_col1, led_col2 = st.columns(2)
    with led_col1:
        status_color = "🟢" if st.session_state.current_led_status == "green" else "🔴"
        st.metric("LED Status", f"{status_color} {st.session_state.current_led_status.upper()}")
    with led_col2:
        st.metric("Last Received Data", st.session_state.last_received_data)

# Process data and update display
process_data()
read_serial()

# Display the bus system visualization
st.markdown("---")
st.subheader("Bus Controller System Simulation")

# Create three columns for CPU, Memory, and I/O
col3, col4, col5 = st.columns(3)

with col3:
    st.markdown("### 🧠 CPU")
    st.code(st.session_state.cpu_data, language=None)
    st.markdown("""
    <div style='background-color: #ffcccc; padding: 10px; border-radius: 5px;'>
    <b>Central Processing Unit</b><br>
    Executes instructions and processes data
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("### 💾 Memory")
    st.code(st.session_state.memory_data, language=None)
    st.markdown("""
    <div style='background-color: #ccffcc; padding: 10px; border-radius: 5px;'>
    <b>Memory Unit</b><br>
    Stores data and instructions for processing
    </div>
    """, unsafe_allow_html=True)

with col5:
    st.markdown("### 🔌 I/O Device")
    st.code(st.session_state.io_data, language=None)
    st.markdown("""
    <div style='background-color: #ccccff; padding: 10px; border-radius: 5px;'>
    <b>Input/Output Device</b><br>
    Communicates with external devices
    </div>
    """, unsafe_allow_html=True)

# Display bus system
st.markdown("---")
st.subheader("Bus System")

bus_col1, bus_col2, bus_col3 = st.columns(3)

with bus_col1:
    st.markdown("### 📍 Address Bus")
    st.info(st.session_state.address_bus)
    st.markdown("Carries memory addresses for read/write operations")

with bus_col2:
    st.markdown("### 📊 Data Bus")
    st.success(st.session_state.data_bus)
    st.markdown("Carries data between components")

with bus_col3:
    st.markdown("### ⚙️ Control Bus")
    st.warning(st.session_state.control_bus)
    st.markdown("Carries control signals between components")

# Data flow animation
st.markdown("---")
st.subheader("Data Flow Animation")

# Create a simple animation showing data moving between components
flow_col1, flow_col2, flow_col3, flow_col4, flow_col5 = st.columns(5)

with flow_col1:
    st.markdown("**CPU**")
    st.markdown("⬇️")

with flow_col2:
    st.markdown("**Address Bus**")
    st.markdown("➡️")

with flow_col3:
    st.markdown("**Memory**")
    st.markdown("⬇️")

with flow_col4:
    st.markdown("**Data Bus**")
    st.markdown("➡️")

with flow_col5:
    st.markdown("**I/O Device**")
    st.markdown("🎯")

# Add a refresh button to update the display
if st.button("🔄 Refresh Display", type="secondary"):
    process_data()
    read_serial()
    st.rerun()

# Auto-refresh the page every 2 seconds
time.sleep(2)
st.rerun()