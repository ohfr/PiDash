import can
import time

def main():
    while True:
        with can.Bus(channel='can0', bustype='socketcan_native') as bus:
            WIDEBAND = 0x368
            SPEED = 0x370
            RPM_MAP = 0x360
            COOLANT_AIR_TEMP = 0x3E0
        # coolant temp/air temp, rpm/MAP, vehicle speed, wideband, 
            bus.set_filters([{ 'can_id': 0x3E0, 'can_mask': 0x3E1, 'extended': False }, { 'can_id': 0x360, 'can_mask': 0x360, 'extended': False }, { 'can_id': 0x370, 'can_mask': 0x371, 'extended': False }, { 'can_id': 0x368, 'can_mask': 0x368, 'extended': False }])

            def convert(bytes, type):
                num = int.from_bytes(bytes, 'big')
                if type == 'kelvin':
                    num *= .1
                    return (num - 273.15) * 9/5 + 32
                if type == 'lambda':
                    num *= .001
                    return num
                if type == 'KPA':
                    num*= 10
                    return num//6.895
                if type == 'KMH':
                    num *= 10
                    return num // 1.609
                

            def prettyPrint(msg):
                if msg.arbitration_id == COOLANT_AIR_TEMP:
                    print('coolant: {}'.format(convert(msg.data[:2], 'kelvin')))
                    print('air temp: {}'.format(convert(msg.data[2:4], 'kelvin')))
                elif msg.arbitration_id == RPM_MAP:
                    print('RPMS: {}'.format(int.from_bytes(msg.data[:2], 'big')))
                    print('MAP (Boost): {}'.format(convert(msg.data[2:4], 'KPA')))
                elif msg.arbitration_id == WIDEBAND:
                    print('AFR: {}'.format(convert(msg.data[:2], 'lambda')))
                elif msg.arbitration_id == SPEED:
                    print('SPEED: {}'.format(convert(msg.data[:2], 'KMH')))

            notifier = can.Notifier(bus, [prettyPrint])

            time.sleep(1.0)

if __name__ == '__main__':
    main()
