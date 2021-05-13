import OpenOPC
import pywintypes

pywintypes.datetime = pywintypes.TimeType

opc = OpenOPC.client()
servers = opc.servers()
print(servers)
# print(opc.info())

opc.connect(servers[0])

servername = opc.list()
print(servername)

value = opc[servername[0] + '.IOSYSTEM.IOSIGNALS.sal_Lata']
print(value)

print(opc.write((servername[0] + '.IOSYSTEM.IOSIGNALS.sal_Lata', 1.0)))

opc.close()

#tags = ['DESKTOP-KHMIAC0_Controlador_P2_2021.IOSYSTEM.IOSIGNALS.sal_Lata', 'DESKTOP-KHMIAC0_Controlador_P2_2021.IOSYSTEM.IOSIGNALS.CONVEYOR_FWD']
#opc.read(tags, group='test')
#print(opc.write(opc.read(group='test')))

#print(opc.write(opc.read(group='test')))
#value2, quality, time = opc.read('DESKTOP-KHMIAC0_Controlador_P2_2021.IOSYSTEM.IOSIGNALS.sal_Lata')
#print(value2)
#value = opc['DESKTOP-KHMIAC0_Controlador_P2_2021.IOSYSTEM.IOSIGNALS.sal_Lata']
#print(value)

#opc['DESKTOP-KHMIAC0_Controlador_P2_2021.IOSYSTEM.IOSIGNALS.sal_Lata'] = opc['DESKTOP-KHMIAC0_Controlador_P2_2021.IOSYSTEM.IOSIGNALS.sal_Lata'] + 1

#properties = opc.properties('DESKTOP-KHMIAC0_Controlador_P2_2021.IOSYSTEM.IOSIGNALS.sal_Lata')
#print(properties)

#print(opc.groups())
