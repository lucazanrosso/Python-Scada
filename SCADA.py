import tkinter as tk
from pymodbus.client.sync import ModbusTcpClient
import OpenOPC
import pywintypes

pywintypes.datetime = pywintypes.TimeType

root = tk.Tk()
root.title("SCADA Interface")

def scan_abb():
    label_abb_server["text"] = "ABB Server: " + opc_client.servers()[0]


def connect_abb():
    opc_client.connect(opc_client.servers()[0], entry_abb_address.get())
    print(opc_client.list())
    global opc_server_name
    opc_server_name = opc_client.list()
    label_status_abb["text"] = "Status: Connected"
    canvas_status_abb.itemconfig(lamp_status_abb, fill='green')


def disconnect_abb():
    opc_client.close()
    label_status_abb["text"] = "Status: Disconnected"
    canvas_status_abb.itemconfig(lamp_status_abb, fill='red')


def scan_and_connect_ur():
    global modbus_client
    modbus_client = ModbusTcpClient(entry_ur_address.get(), 502)
    if modbus_client.connect():
        label_ur_server["text"] = "UR Server: " + modbus_client.host + " Port: " + \
                                  str(modbus_client.port)
        label_status_ur["text"] = "Status: Connected"
        canvas_status_ur.itemconfig(lamp_status_ur, fill='green')


def disconnect_ur():
    modbus_client.close()
    label_status_ur["text"] = "Status: Disconnected"
    canvas_status_ur.itemconfig(lamp_status_ur, fill='red')


def set_scan(value):
    global scan
    scan = value
    if scan:
        canvas_scanning.itemconfig(lamp_scanning, fill='green')
        scan_variables()
    else:
        canvas_scanning.itemconfig(lamp_scanning, fill='red')


def scan_variables():
    global opc_server_name

    if scan:
        conveyor_fwd = opc_client.read(opc_server_name[0] + '.IOSYSTEM.IOSIGNALS.CONVEYOR_FWD')[0]
        conveyor_bwd = opc_client.read(opc_server_name[0] + '.IOSYSTEM.IOSIGNALS.CONVEYOR_BWD')[0]
        conveyor_obj_sur = opc_client.read(opc_server_name[0] + '.IOSYSTEM.IOSIGNALS.CONVEYOR_OBJ_SUR')[0]

        if conveyor_obj_sur == 1:
            modbus_client.write_register(130, 1)
        else:
            modbus_client.write_register(130, 0)

        if conveyor_fwd == 1:
            canvas_conveyor_fwd.itemconfig(lamp_conveyor_fwd, fill="green")
        else:
            canvas_conveyor_fwd.itemconfig(lamp_conveyor_fwd, fill="red")

        if conveyor_bwd == 1:
            canvas_conveyor_bwd.itemconfig(lamp_conveyor_bwd, fill="green")
        else:
            canvas_conveyor_bwd.itemconfig(lamp_conveyor_bwd, fill="red")

        can_ready = modbus_client.read_input_registers(131, 1).registers[0]
        brick_ready = modbus_client.read_input_registers(132, 1).registers[0]
        obj_verified = modbus_client.read_input_registers(133, 1).registers[0]

        if obj_verified == 1:
            opc_client.write((opc_server_name[0] + '.IOSYSTEM.IOSIGNALS.objeto_Verificado', 1))
            modbus_client.write_register(133, 0)

        if can_ready == 1:
            opc_client.write((opc_server_name[0] + '.IOSYSTEM.IOSIGNALS.sal_Lata', 1))
            modbus_client.write_register(131, 0)
            canvas_can.itemconfig(lamp_can, fill="green")
            total_cans = int(entry_total_can.get()) + 1
            entry_total_can.delete(0, tk.END)
            entry_total_can.insert(0, total_cans)
        else:
            canvas_can.itemconfig(lamp_can, fill="white")

        if brick_ready == 1:
            opc_client.write((opc_server_name[0] + '.IOSYSTEM.IOSIGNALS.sal_Brick', 1))
            modbus_client.write_register(132, 0)
            canvas_brick.itemconfig(lamp_brick, fill="green")
            total_bricks = int(entry_total_brick.get()) + 1
            entry_total_brick.delete(0, tk.END)
            entry_total_brick.insert(0, total_bricks)
        else:
            canvas_brick.itemconfig(lamp_brick, fill="white")

        root.after(200, scan_variables)


def start_ur():
    modbus_client.write_register(128, 1)
    canvas_process.itemconfig(lamp_process, fill='green')


def stop_ur():
    modbus_client.write_register(128, 0)
    canvas_process.itemconfig(lamp_process, fill='red')


def can():
    print(opc_client.write((opc_server_name[0] + '.IOSYSTEM.IOSIGNALS.sal_Lata', 1)))


def brick():
    print(opc_client.write((opc_server_name[0] + '.IOSYSTEM.IOSIGNALS.sal_Brick', 1)))


def obj_sensor_sur():
    modbus_client.write_register(130, 1)


def obj_available():
    print(opc_client.write((opc_server_name[0] + '.IOSYSTEM.IOSIGNALS.sal_obj_nuevo', 1)))


opc_client = OpenOPC.client()
opc_server_name = opc_client.list()
modbus_client = ModbusTcpClient('127.0.0.1', 502)
scan = False

# ABB
label_connections = tk.Label(root, text="Connections")
label_connections.config(font=("TkDefaultFont", 14))
label_abb_title = tk.Label(root, text="IRB 140 (OPC DA)")
label_abb_title.config(font=("TkDefaultFont", 12))
label_abb_address = tk.Label(root, text="IP Address")
entry_abb_address = tk.Entry(root)
entry_abb_address.insert(0, "127.0.0.1")
button_scan_server_abb = tk.Button(root, text="Scan OPC servers", command=scan_abb, width=15, padx=5, pady=5)
label_abb_server = tk.Label(root, text="ABB Server:")
button_connect_abb = tk.Button(root, text="Connect", command=connect_abb, width=15, padx=5, pady=5)
label_status_abb = tk.Label(root, text="Status: Disconnected")
button_disconnect_abb = tk.Button(root, text="Disconnect", command=disconnect_abb, width=15, padx=5, pady=5)
canvas_status_abb = tk.Canvas(root, width=30, height=30)
lamp_status_abb = canvas_status_abb.create_oval(5, 5, 25, 25, fill='red')

# UR
label_ur_title = tk.Label(root, text="UR3 (MODBUS TCP IP)")
label_ur_title.config(font=("TkDefaultFont", 12))
label_ur_address = tk.Label(root, text="IP Address")
entry_ur_address = tk.Entry(root)
entry_ur_address.insert(0, "192.168.56.128")
button_scan_and_connect_server_ur = tk.Button(root, text="Connect", command=scan_and_connect_ur, width=15, padx=5,
                                              pady=5)
label_ur_server = tk.Label(root, text="UR Server:")
button_disconnect_ur = tk.Button(root, text="Disconnect", command=disconnect_ur, width=15, padx=5, pady=5)
label_status_ur = tk.Label(root, text="Status: Disconnected")
canvas_status_ur = tk.Canvas(root, width=30, height=30)
lamp_status_ur = canvas_status_ur.create_oval(5, 5, 25, 25, fill='red')

# PLC
label_plc_title = tk.Label(root, text="PLC")
checkbox_plc_simulated = tk.Checkbutton(root, text="Simulated")
checkbox_plc_simulated.select()
label_plc_title.config(font=("TkDefaultFont", 12))
label_plc_address = tk.Label(root, text="IP Address")
entry_plc_address = tk.Entry(root)
entry_plc_address.insert(0, "192.168.0.108")
button_plc_connect = tk.Button(root, text="Connect", width=15, padx=5, pady=5)
button_plc_disconnect = tk.Button(root, text="Disconnect", width=15, padx=5, pady=5)

# SIGNALS
label_signals_title = tk.Label(root, text="Signals")
label_signals_title.config(font=("TkDefaultFont", 14))
button_start_scanning = tk.Button(root, text="Scan signals", command=lambda: set_scan(True), width=15, padx=5, pady=5)
canvas_scanning = tk.Canvas(root, width=30, height=30)
lamp_scanning = canvas_scanning.create_oval(5, 5, 25, 25, fill='red')
button_stop_scanning = tk.Button(root, text="Stop scanning", command=lambda: set_scan(False), width=15, padx=5, pady=5)
button_start_process = tk.Button(root, text="Start process", command=start_ur, width=15, padx=5, pady=5)
canvas_process = tk.Canvas(root, width=30, height=30)
lamp_process = canvas_process.create_oval(5, 5, 25, 25, fill='red')
button_stop_process = tk.Button(root, text="Stop process", command=stop_ur, width=15, padx=5, pady=5)

label_input = tk.Label(root, text="INPUT")
label_input.config(font=("TkDefaultFont", 12))
button_can = tk.Button(root, text="Can", command=can, width=15, padx=5, pady=5)
button_brick = tk.Button(root, text="Brick", command=brick, width=15, padx=5, pady=5)
button_obj_available = tk.Button(root, text="Obj available", command=obj_available, width=15, padx=5, pady=5)
button_obj_sensor_sur = tk.Button(root, text="Obj sensor sur", command=obj_sensor_sur, width=15, padx=5, pady=5)
label_output = tk.Label(root, text="OUTPUT")
label_output.config(font=("TkDefaultFont", 12))
label_can = tk.Label(root, text="Can")
canvas_can = tk.Canvas(root, width=30, height=30)
lamp_can = canvas_can.create_oval(5, 5, 25, 25, fill='white')
entry_total_can = tk.Entry(root, width=5)
entry_total_can.insert(0, 0)
label_brick = tk.Label(root, text="Brick")
canvas_brick = tk.Canvas(root, width=30, height=30)
lamp_brick = canvas_brick.create_oval(5, 5, 25, 25, fill='white')
entry_total_brick = tk.Entry(root, width=5)
entry_total_brick.insert(0, 0)
label_conveyor_fwd = tk.Label(root, text="Conveyor FWD")
canvas_conveyor_fwd = tk.Canvas(root, width=30, height=30)
lamp_conveyor_fwd = canvas_conveyor_fwd.create_oval(5, 5, 25, 25, fill='red')
label_conveyor_bwd = tk.Label(root, text="Conveyor BWD")
canvas_conveyor_bwd = tk.Canvas(root, width=30, height=30)
lamp_conveyor_bwd = canvas_conveyor_bwd.create_oval(5, 5, 25, 25, fill='red')


# ABB
label_connections.grid(sticky="W", row=2, column=2, padx=5, pady=5)
label_abb_title.grid(sticky="W", row=3, column=2, padx=5, pady=5, columnspan=3)
label_abb_address.grid(sticky="E", row=4, column=2, padx=5, pady=5)
entry_abb_address.grid(sticky="W", row=4, column=3, padx=5, pady=5, columnspan=2)
button_scan_server_abb.grid(sticky="W", row=5, column=2, padx=5, pady=5)
label_abb_server.grid(sticky="W", row=5, column=3, padx=5, pady=5, columnspan=2)
button_connect_abb.grid(sticky="W", row=6, column=2, padx=5, pady=5)
label_status_abb.grid(sticky="W", row=6, column=3, padx=5, pady=5)
canvas_status_abb.grid(sticky="W", row=6, column=4, padx=(5, 30))
button_disconnect_abb.grid(sticky="W", row=7, column=2, padx=5, pady=5)

# UR
label_ur_title.grid(sticky="W", row=9, column=2, padx=5, pady=5, columnspan=3)
label_ur_address.grid(sticky="E", row=10, column=2, padx=5, pady=5)
entry_ur_address.grid(sticky="W", row=10, column=3, padx=5, pady=5)
button_scan_and_connect_server_ur.grid(sticky="W", row=11, column=2, padx=5, pady=5, columnspan=2)
label_ur_server.grid(sticky="W", row=11, column=3, padx=5, pady=5, columnspan=2)
button_disconnect_ur.grid(sticky="W", row=12, column=2, padx=5, pady=5)
label_status_ur.grid(sticky="W", row=12, column=3, padx=5, pady=5)
canvas_status_ur.grid(sticky="W", row=12, column=4)

# PLC
label_plc_title.grid(sticky="W", row=14, column=2, padx=5, pady=5)
checkbox_plc_simulated.grid(sticky="W", row=14, column=3, padx=5, pady=5)
label_plc_address.grid(sticky="E", row=15, column=2, padx=5, pady=5)
entry_plc_address.grid(sticky="W", row=15, column=3, padx=5, pady=5)
button_plc_connect.grid(sticky="W", row=16, column=2, padx=5, pady=5)
button_plc_disconnect.grid(sticky="W", row=17, column=2, padx=5, pady=5)

# SIGNALS
label_signals_title.grid(sticky="W", row=2, column=7, padx=5, pady=5)
button_start_scanning.grid(sticky="W", row=4, column=7, padx=5, pady=5)
canvas_scanning.grid(sticky="W", row=4, column=8, padx=5, pady=5)
button_stop_scanning.grid(sticky="W", row=5, column=7, padx=5, pady=5)
button_start_process.grid(sticky="W", row=6, column=7, padx=5, pady=5)
canvas_process.grid(sticky="W", row=6, column=8, padx=5, pady=5)
button_stop_process.grid(sticky="W", row=7, column=7, padx=5, pady=5)

label_input.grid(sticky="W", row=9, column=7, padx=5, pady=(40, 5))
button_can.grid(sticky="W", row=10, column=7, padx=5, pady=5)
button_brick.grid(sticky="W", row=10, column=8, padx=5, pady=5, columnspan=2)
button_obj_sensor_sur.grid(sticky="W", row=11, column=7, padx=5, pady=5)
button_obj_available.grid(sticky="W", row=11, column=8, padx=5, pady=5, columnspan=2)

label_output.grid(sticky="W", row=13, column=7, padx=5, pady=5)
label_can.grid(sticky="W", row=14, column=7, padx=5, pady=5)
canvas_can.grid(sticky="W", row=14, column=8, padx=5, pady=5)
entry_total_can.grid(sticky="W", row=14, column=9, padx=5, pady=5)
label_brick.grid(sticky="W", row=15, column=7, padx=5, pady=5)
canvas_brick.grid(sticky="W", row=15, column=8, padx=5, pady=5)
entry_total_brick.grid(sticky="W", row=15, column=9, padx=5, pady=5)
label_conveyor_fwd.grid(sticky="W", row=16, column=7, padx=5, pady=5)
canvas_conveyor_fwd.grid(sticky="W", row=16, column=8, padx=5, pady=5)
label_conveyor_bwd.grid(sticky="W", row=17, column=7, padx=5, pady=5)
canvas_conveyor_bwd.grid(sticky="W", row=17, column=8, padx=5, pady=5)

root.mainloop()
