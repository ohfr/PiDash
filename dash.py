import can
import time

def main():
    with can.Bus(channel='can0', bustype='socketcan_native') as bus:
    # coolant temp, rpm, vehicle speed, wideband, MAP, air temp
        bus.set_filters([{ 'can_id': 0x05, 'can_mask': 0x05, 'extended': False }, { 'can_id': 0x0C, 'can_mask': 0x0C, 'extended': False }, { 'can_id': 0x0D, 'can_mask': 0x0D, 'extended': False }, { 'can_id': 0x26, 'can_mask': 0x26, 'extended': False }, { 'can_id': 0x0B, 'can_mask': 0x0B, 'extended': False }, { 'can_id': 0x0F, 'can_mask': 0x0F, 'extended': False }])

        def prettyPrint(msg):
            print('msg _id: {}, msg data: {}'.format(msg.arbitration_id, msg.data))
            if msg.arbitration_id == 0x05:
                print('coolant: ' + int.from_bytes(msg.data[:2], 'big'))
            if msg.arbitration_id == 0x0F:
                print('air temp: ' + int.from_bytes(msg.data[1:3], 'big'))

        notifier = can.Notifier(bus, [prettyPrint])

        time.sleep(1.0)

if __name__ == '__main__':
    main()