import tkinter as tk
from pymodbus.client.sync import ModbusTcpClient
import OpenOPC
import pywintypes

pywintypes.datetime = pywintypes.TimeType


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.grid(padx=15, pady=15)

        self.opc_client = OpenOPC.client()
        self.modbus_client = ModbusTcpClient('192.168.56.128', 502)
        self.scan = False

        # ABB
        self.label_abb_title = tk.Label(self, text="ABB Robot")
        # title_font = tk.font.Font(size=36)
        # self.label_abb_title['font'] = title_font
        self.label_abb_title.config(font=("TkDefaultFont", 24))
        self.button_scan_server_abb = tk.Button(self, text="Connect ABB via OPC DA", command=self.scan_abb,
                                                padx=10, pady=10)
        self.label_abb_server = tk.Label(self, text="ABB Server:", anchor="w", width='30')
        self.button_disconnect_abb = tk.Button(self, text="Disconnect", command=self.disconnect_abb,
                                               padx=10, pady=10)
        self.button_connect_abb = tk.Button(self, text="Connect", command=self.connect_abb,
                                            padx=10, pady=10)
        self.label_status_abb = tk.Label(self, text="Server status: Disconnected")
        self.canvas_status_abb = tk.Canvas(self, width=30, height=30)
        self.lamp_status_abb = self.canvas_status_abb.create_oval(5, 5, 25, 25, fill='red')
        self.label_can_abb = tk.Label(self, text="CAN")
        self.canvas_can_abb = tk.Canvas(self, width=30, height=30)
        self.lamp_can_abb = self.canvas_can_abb.create_oval(5, 5, 25, 25, fill='white')
        self.label_brick_abb = tk.Label(self, text="BRICK")
        self.canvas_brick_abb = tk.Canvas(self, width=30, height=30)
        self.lamp_brick_abb = self.canvas_brick_abb.create_oval(5, 5, 25, 25, fill='white')
        self.label_conveyor_abb = tk.Label(self, text="CONVEYOR")
        self.canvas_conveyor_abb = tk.Canvas(self, width=30, height=30)
        self.lamp_conveyor_abb = self.canvas_conveyor_abb.create_oval(5, 5, 25, 25, fill='white')

        # UR
        self.label_ur_title = tk.Label(self, text="UR Robot")
        self.label_ur_title.config(font=("TkDefaultFont", 24))
        self.button_scan_and_connect_server_ur = tk.Button(self, text="Scan & connect UR via MODBUS TCP/IP",
                                                           command=self.scan_and_connect_ur, padx=10, pady=10)
        self.label_ur_server = tk.Label(self, text="UR Server:")
        self.button_disconnect_ur = tk.Button(self, text="Disconnect", command=self.disconnect_ur, padx=10, pady=10)
        self.label_status_ur = tk.Label(self, text="Server status: Disconnected")
        self.canvas_status_ur = tk.Canvas(self, width=30, height=30)
        self.lamp_status_ur = self.canvas_status_ur.create_oval(5, 5, 25, 25, fill='red')
        self.label_can_ur = tk.Label(self, text="CAN")
        self.canvas_can_ur = tk.Canvas(self, width=30, height=30)
        self.lamp_can_ur = self.canvas_can_ur.create_oval(5, 5, 25, 25, fill='white')
        self.label_brick_ur = tk.Label(self, text="BRICK")
        self.canvas_brick_ur = tk.Canvas(self, width=30, height=30)
        self.lamp_brick_ur = self.canvas_brick_ur.create_oval(5, 5, 25, 25, fill='white')

        self.button_scan_variables = tk.Button(self, text="Scan variables", command=lambda: self.set_scan(True),
                                               padx=10, pady=10)
        self.button_start_ur = tk.Button(self, text="Start UR Robot", command=self.start_ur, padx=10, pady=10)
        self.button_stop_ur = tk.Button(self, text="Stop UR Robot", command=self.stop_ur, padx=10, pady=10)
        self.button_stop_variables = tk.Button(self, text="Stop scanning", command=lambda: self.set_scan(False),
                                               padx=10, pady=10)
        self.quit = tk.Button(self, text="QUIT", fg="red",
                              command=self.master.destroy, padx=10, pady=10)

        # ABB
        self.label_abb_title.grid(sticky="W", row=0, column=0, padx=(15, 0), pady=5)
        self.button_scan_server_abb.grid(sticky="W", row=1, column=0, padx=5, pady=10)
        self.label_abb_server.grid(sticky="W", row=1, column=2, padx=5, pady=0, columnspan=2)
        self.button_disconnect_abb.grid(sticky="E", row=1, column=10, padx=5, pady=10)
        self.button_connect_abb.grid(sticky="W", row=2, column=0, padx=5, pady=5)
        self.label_status_abb.grid(sticky="W", row=2, column=2, padx=5, pady=0)
        self.canvas_status_abb.grid(sticky="W", row=2, column=3)
        self.label_can_abb.grid(row=3, column=0, padx=0, pady=(20, 0))
        self.canvas_can_abb.grid(row=4, column=0)
        self.label_brick_abb.grid(row=3, column=1, padx=0, pady=(20, 0))
        self.canvas_brick_abb.grid(row=4, column=1)
        self.label_conveyor_abb.grid(row=3, column=2, padx=0, pady=(20, 0))
        self.canvas_conveyor_abb.grid(row=4, column=2)

        # UR
        self.label_ur_title.grid(sticky="W", row=5, column=0, padx=15, pady=(30, 5))
        self.button_scan_and_connect_server_ur.grid(sticky="W", row=6, column=0, padx=5, pady=10, columnspan=2)
        self.label_ur_server.grid(sticky="W", row=6, column=2, padx=5, pady=0, columnspan=2)
        self.button_disconnect_ur.grid(sticky="E", row=6, column=10, padx=5, pady=10)
        self.label_status_ur.grid(sticky="W", row=7, column=2, padx=5, pady=0)
        self.canvas_status_ur.grid(sticky="W", row=7, column=3)
        self.label_can_ur.grid(row=8, column=0, padx=0, pady=(20, 0))
        self.canvas_can_ur.grid(row=9, column=0, padx=0, pady=(0, 20))
        self.label_brick_ur.grid(row=8, column=1, padx=0, pady=(20, 0))
        self.canvas_brick_ur.grid(row=9, column=1, padx=0, pady=(0, 20))

        self.button_scan_variables.grid(sticky="W", row=10, column=0, padx=5, pady=10)
        self.button_start_ur.grid(sticky="W", row=10, column=1, padx=5, pady=10)
        self.button_stop_ur.grid(sticky="W", row=10, column=8, padx=5, pady=10)
        self.button_stop_variables.grid(sticky="W", row=10, column=9, padx=5, pady=10)
        self.quit.grid(sticky="E", row=10, column=10, padx=5, pady=10)

    def scan_abb(self):
        self.label_abb_server["text"] = "ABB Server: " + self.opc_client.servers()[0]

    def connect_abb(self):
        self.opc_client.connect('ABB.IRC5.OPC.Server.DA')
        self.controller = self.opc_client.list()
        print(self.controller[0])
        self.label_status_abb["text"] = "Server Status: Connected"
        self.canvas_status_abb.itemconfig(self.lamp_status_abb, fill='green')

    def disconnect_abb(self):
        self.opc_client.close()
        self.label_status_abb["text"] = "Server Status: Disconnected"
        self.canvas_status_abb.itemconfig(self.lamp_status_abb, fill='red')

    def scan_and_connect_ur(self):
        if self.modbus_client.connect():
            self.label_ur_server["text"] = "UR Server: " + self.modbus_client.host + " Port: " + \
                                           str(self.modbus_client.port)
            self.label_status_ur["text"] = "Server Status: Connected"
            self.canvas_status_ur.itemconfig(self.lamp_status_ur, fill='green')

    def disconnect_ur(self):
        self.modbus_client.close()
        self.label_status_ur["text"] = "Server Status: Disconnected"
        self.canvas_status_ur.itemconfig(self.lamp_status_ur, fill='red')

    def set_scan(self, value):
        self.scan = value
        if self.scan:
            self.scan_variables()

    def scan_variables(self, old_sal_lata=None, old_sal_brick=None, old_conveyor_fwd=None, old_register_128=None):

        if self.scan:
            sal_lata = self.opc_client.read(self.controller[0] + '.IOSYSTEM.IOSIGNALS.sal_Lata')[0]
            sal_brick = self.opc_client.read(self.controller[0] + '.IOSYSTEM.IOSIGNALS.sal_Brick')[0]
            conveyor_fwd = self.opc_client.read(self.controller[0] + '.IOSYSTEM.IOSIGNALS.CONVEYOR_FWD')[0]

            if old_sal_lata != sal_lata or old_sal_brick != sal_brick or old_conveyor_fwd != conveyor_fwd:
                if sal_lata == 0:
                    self.modbus_client.write_register(128, 0)
                    self.canvas_can_abb.itemconfig(self.lamp_can_abb, fill='white')
                else:
                    self.canvas_can_abb.itemconfig(self.lamp_can_abb, fill='yellow')

                if sal_brick == 0:
                    self.canvas_brick_abb.itemconfig(self.lamp_brick_abb, fill='white')
                else:
                    self.canvas_brick_abb.itemconfig(self.lamp_brick_abb, fill='yellow')

                if conveyor_fwd == 0:
                    self.canvas_conveyor_abb.itemconfig(self.lamp_conveyor_abb, fill='white')
                else:
                    self.canvas_conveyor_abb.itemconfig(self.lamp_conveyor_abb, fill='yellow')
                # print('ciao')

            register_128 = self.modbus_client.read_input_registers(128).registers[0]
            # print(self.modbus_client.read_input_registers(128).registers[0])

            if old_register_128 != register_128:
                if register_128 == 0:
                    self.canvas_can_ur.itemconfig(self.lamp_can_ur, fill='white')
                else:
                    self.opc_client.write((self.controller[0] + '.IOSYSTEM.IOSIGNALS.sal_Lata', 1.0))
                    self.canvas_can_ur.itemconfig(self.lamp_can_ur, fill='yellow')
                    # print('ciao2')

            # print('oaic')
            root.after(100, self.scan_variables, sal_lata, sal_brick, conveyor_fwd, register_128)

    def start_ur(self):
        self.modbus_client.write_register(129, 1)
        self.modbus_client.write_register(128, 0)

    def stop_ur(self):
        self.modbus_client.write_register(129, 0)

    def stop_scan_variables(self):
        self.scan = False


root = tk.Tk()

app = Application(master=root)
app.mainloop()
