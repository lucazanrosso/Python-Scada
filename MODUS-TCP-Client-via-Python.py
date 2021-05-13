from pymodbus.client.sync import ModbusTcpClient

client = ModbusTcpClient('192.168.56.128', 502)
print(client.connect())

print(client.read_input_registers(128, 1).registers[0])

client.write_registers(128, 1)

client.close()
