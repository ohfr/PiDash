import can
import subprocess
import socketio
from aiohttp import web
import asyncio

WIDEBAND = 0x368
SPEED = 0x370
RPM_MAP = 0x360
COOLANT_AIR_TEMP = 0x3E0

sio = socketio.AsyncServer(async_mode='aiohttp', cors_allowed_origins='*')
app = web.Application()
sio.attach(app)
notifier = None

def convert(bytes: list, type):
    if bytes[0] == None and bytes[1] == None:
        return 0
    if bytes[0] == None:
        bytes[0] = 0
    if bytes[1] == None:
        bytes[1] = 0
    num = int.from_bytes(bytes, 'big')
    if type == 'kelvin':
        num *= .1
        return  (num - 273.15) * 9/5 + 32
    if type == 'lambda':
        num *= .001
        num *= 14.71
        return num
    if type == 'KPA':
        num*= .1
        if num <= 100:
            return -(num*.01)
        return num//6.895
    if type == 'KMH':
        num *= 10
        return num // 1.609
    
async def send(msg):
    if msg.arbitration_id == COOLANT_AIR_TEMP:
        print('coolant: {}'.format(convert(msg.data[:2], 'kelvin')))
        print('air temp: {}'.format(convert(msg.data[2:4], 'kelvin')))
        await sio.emit('dashEvent', { 'coolant': convert(msg.data[:2], 'kelvin'), 'airTemp': convert(msg.data[2:4], 'kelvin') })
    elif msg.arbitration_id == RPM_MAP:
        await sio.emit('dashEvent', { 'rpm': int.from_bytes(msg.data[:2], 'big'), 'boost': convert(msg.data[2:4], 'KPA') })
        print('RPMS: {}'.format(int.from_bytes(msg.data[:2], 'big')))
        print('MAP (Boost): {}'.format(convert(msg.data[2:4], 'KPA')))
    elif msg.arbitration_id == WIDEBAND:
        await sio.emit('dashEvent', { 'afr': convert(msg.data[:2], 'lambda') })
        print('AFR: {}'.format(convert(msg.data[:2], 'lambda')))
    elif msg.arbitration_id == SPEED:
        await sio.emit('dashEvent', { 'speed': convert(msg.data[:2], 'KMH')})
        print('SPEED: {}'.format(convert(msg.data[:2], 'KMH')))

async def background_task():
    try:
        print('started task')
        with can.Bus(channel='can0', bustype='socketcan') as bus:
            loop = asyncio.get_running_loop()
            global notifier
            reader = can.AsyncBufferedReader()
            notifier = can.Notifier(bus, [reader], loop=loop)
            while True:
                msg = await reader.get_message()
                await send(msg)
    except KeyboardInterrupt:
        notifier.stop()
        print('Stopped task')

@sio.event
async def connect(sid, environ):
    print('client connected')
    await sio.emit('my_response', {'data': 'Connected', 'count': 0}, room=sid)


@sio.event
def disconnect(sid):
    print('Client disconnected')



async def init_app():
    # start the can bus
    subprocess.run(['sudo', '/sbin/ip', 'link', 'set', 'can0', 'up', 'type', 'can', 'bitrate', '1000000'])

    sio.start_background_task(background_task)
    return app

if __name__ == '__main__':
    asyncio.run(web.run_app(init_app(), port=5000))