import OpenOPC
import pywintypes

pywintypes.datetime = pywintypes.TimeType

opc = OpenOPC.client()
print(opc.servers())

opc.connect('ABB.IRC5.OPC.Server.DA')
print(opc.list())

# opc.read('DESKTOP-OJGEJRP_Controlador1.IOSYSTEM.IOSIGNALS.sal_Lata')
value = opc['DESKTOP-OJGEJRP_Controlador1.IOSYSTEM.IOSIGNALS.sal_Lata']
print(value)

opc.write(('DESKTOP-OJGEJRP_Controlador1.IOSYSTEM.IOSIGNALS.sal_Lata', 1.0))

value = opc['DESKTOP-OJGEJRP_Controlador1.IOSYSTEM.IOSIGNALS.sal_Lata']
print(value)

opc.close()
