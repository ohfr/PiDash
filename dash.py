import can
import time
from PyQt5 import QtWidgets
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys

WIDEBAND = 0x368
SPEED = 0x370
RPM_MAP = 0x360
COOLANT_AIR_TEMP = 0x3E0
class WorkerThread(QThread):
    update_coolant = pyqtSignal(int)
    update_airTemp = pyqtSignal(int)
    update_airFuel = pyqtSignal(int)
    update_speed = pyqtSignal(int)
    update_rpm = pyqtSignal(int)
    update_boost = pyqtSignal(int)
    def run(self):
        with can.Bus(channel='can0', bustype='socketcan') as bus:
            bus.set_filters([{ 'can_id': 0x3E0, 'can_mask': 0x3E1, 'extended': False }, { 'can_id': 0x360, 'can_mask': 0x360, 'extended': False }, { 'can_id': 0x370, 'can_mask': 0x371, 'extended': False }, { 'can_id': 0x368, 'can_mask': 0x368, 'extended': False }])
            while True:
                def convert(bytes, type):
                    num = int.from_bytes(bytes, 'big')
                    if type == 'kelvin':
                        num *= .1
                        return  (num - 273.15) * 9/5 + 32
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
                        self.update_coolant.emit(convert(msg.data[:2], 'kelvin'))
                        self.update_airTemp.emit(convert(msg.data[2:4], 'kelvin'))
                        print('coolant: {}'.format(convert(msg.data[:2], 'kelvin')))
                        print('air temp: {}'.format(convert(msg.data[2:4], 'kelvin')))
                    elif msg.arbitration_id == RPM_MAP:
                        self.update_rpm.emit(int.from_bytes(msg.data[:2], 'big'))
                        self.update_boost.emit(convert(msg.data[2:4], 'KPA'))
                        print('RPMS: {}'.format(int.from_bytes(msg.data[:2], 'big')))
                        print('MAP (Boost): {}'.format(convert(msg.data[2:4], 'KPA')))
                    elif msg.arbitration_id == WIDEBAND:
                        self.update_airFuel.emit(convert(msg.data[:2], 'lambda'))
                        print('AFR: {}'.format(convert(msg.data[:2], 'lambda')))
                    elif msg.arbitration_id == SPEED:
                        self.update_speed.emit(convert(msg.data[:2], 'KMH'))
                        print('SPEED: {}'.format(convert(msg.data[:2], 'KMH')))
                notifier = can.Notifier(bus, [prettyPrint])
                time.sleep(.5)

def main():
    app = QApplication(sys.argv)
    win = QMainWindow()
    win.setWindowTitle("PiDash")


    coolantTempLabel = QtWidgets.QLabel(win)
    airTempLabel = QtWidgets.QLabel(win)
    rpmLabel = QtWidgets.QLabel(win)
    boostLabel = QtWidgets.QLabel(win)
    airFuelLabel = QtWidgets.QLabel(win)
    speedLabel = QtWidgets.QLabel(win)
    
    app.setStyleSheet('.QLabel { font-size: 25pt }')

    coolantTempLabel.setText('Coolant: 0')
    airTempLabel.setText('Air Temp: 0')
    rpmLabel.setText('RPM: 0')
    boostLabel.setText('Boost: 0')
    airFuelLabel.setText('AFR: 0')
    speedLabel.setText('Speed: 0')

    coolantTempLabel.setFixedWidth(400)
    speedLabel.setFixedWidth(400)
    airTempLabel.setFixedWidth(400)
    rpmLabel.setFixedWidth(400)
    airFuelLabel.setFixedWidth(400)
    boostLabel.setFixedWidth(400)

    rpmLabel.move(50, 0)
    speedLabel.move(50, 50)
    airFuelLabel.move(50, 100)
    boostLabel.move(50, 150)
    coolantTempLabel.move(50, 200)
    airTempLabel.move(50, 250)

    win.showMaximized()
    worker = WorkerThread()
    worker.start()

    def updateCoolant(val):
        coolantTempLabel.adjustSize()
        coolantTempLabel.setText('Coolant Temp: {}'.format(val))
    
    def updateAir(val):
        airTempLabel.adjustSize()
        airTempLabel.setText('Air temp: {}'.format(val))

    def updateAFR(val):
        airFuelLabel.adjustSize()
        airFuelLabel.setText('AFR: {}'.format(val))

    def updateRpm(val):
        rpmLabel.adjustSize()
        rpmLabel.setText('RPM: {}'.format(val))


    def updateSpeed(val):
        speedLabel.adjustSize()
        speedLabel.setText('Speed: {}'.format(val))

    def updateBoost(val):
        boostLabel.adjustSize()
        boostLabel.setText('Boost: {}'.format(val))


    worker.update_airTemp.connect(updateAir)
    worker.update_coolant.connect(updateCoolant)
    worker.update_airFuel.connect(updateAFR)
    worker.update_rpm.connect(updateRpm)
    worker.update_speed.connect(updateSpeed)
    worker.update_boost.connet(updateBoost)
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
