import time
# Assumes I2C, a certain type of connection
import board
import busio

import qrcode
import py_resize

i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_bmp280.Adafruit_BMP280_I2C(i2c)

# QR Code format:
#  {
#   id: int
#   locked: bool
#   super: {
#     deviceId: int,
#     deviceType: "lock",
#     status: String,
#     group: [list of String],
#     location: String,
#   }
#  }
# }

def getState(sensor):
    data = {
        "locked": sensor.pin() == high,
        "super": {
            "deviceId": 1,
            "deviceType": "lock",
            "status": "ok", # ?
            "group": ["Trap House"],
            "location": "Tom's Room"
        }
    }
    return data

state = getState(sensor)
# TODO: add call to Nikhil's script to make sure qrCode has the right dimensions
# Then actually display on screen
qrCode = qrcode.make(state)


while True:
    time.sleep(30)
    if state != getState(sensor):
        # The lock status has changed, generate new QR Code
        state = getState(sensor)
        # TODO: add call to Nikhil's script to make sure qrCode has the right dimensions
        # Then actually display on screen
        qrCode = qrcode.make(state)
        qrCode.save(f'{state.super.deviceId}.bmp')
        py_resize.main(f'-f {state.super.deviceId}.bmp')


