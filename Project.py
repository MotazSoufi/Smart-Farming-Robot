import cv2
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import ttk
from time import sleep
from gpiozero import Motor, InputDevice
import subprocess

coil1 = Motor(forward=27, backward=4, pwm=False)
coil2 = Motor(forward=17, backward=22, pwm=False)

motorRight = Motor(forward=26, backward=19)
motorLeft = Motor(forward=13, backward=6)

soilSensor = InputDevice(5)

forwardSeq = ['FF', 'BF', 'BB', 'FB']
reverseSeq = list(forwardSeq)
reverseSeq.reverse()


def forward(delay, steps):
    for i in range(steps):
        for step in forwardSeq:
            set_step(step)
            sleep(delay)


def backward(delay, steps):
    for i in range(steps):
        for step in reverseSeq:
            set_step(step)
            sleep(delay)


def set_step(step):
    if step == 'S':
        coil1.stop()
        coil2.stop()
    else:
        if step[0] == 'F':
            coil1.forward()
        else:
            coil1.backward()
        if step[1] == 'F':
            coil2.forward()
        else:
            coil2.backward()


def motorF():
    print("Motor Forward")
    motorRight.forward(0.3)
    motorLeft.forward(0.3)


def motorB():
    print("Motor Backward")
    motorRight.backward(0.3)
    motorLeft.backward(0.3)


def motorR():
    print("Motor Right")
    motorRight.backward(0.3)
    motorLeft.forward(0.9)


def motorL():
    print("Motor Left")
    motorRight.forward(0.9)
    motorLeft.backward(0.3)


def motorStop():
    print("Motor Stopped")
    motorRight.forward(0)
    motorLeft.forward(0)


def pump():
    print("Water Pump On")
    subprocess.run(["python", "pump.py"])


def soil():
    print("reading soil moisture...")
    set_step('S')
    backward(int(5) / 1000.0, int(200))
    sleep(2)
    moisture = soilSensor.value
    if moisture == 1:
        label1.config(text="Soil Moisture: Soil Dry")
    else:
        print("Soil wet")

    forward(int(5) / 1000.0, int(200))


window = tk.Tk()

cap = cv2.VideoCapture(0)


def camera():
    _, frame = cap.read()
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame = cv2.flip(frame, 0)
    image = Image.fromarray(frame)
    photo = ImageTk.PhotoImage(image)
    label.config(image=photo)
    label.image = photo
    window.after(30, camera)


label = tk.Label(window)
label.grid(row=0, column=0, columnspan=3)

camera()

button1 = tk.Button(window, text="up", command=motorF)
button1.grid(row=1, column=1)

button2 = tk.Button(window, text="down", command=motorB)
button2.grid(row=3, column=1)

button3 = tk.Button(window, text="right", command=motorR)
button3.grid(row=2, column=2)

button4 = tk.Button(window, text="left", command=motorL)
button4.grid(row=2, column=0)

button5 = tk.Button(window, text="stop", command=motorStop)
button5.grid(row=2, column=1)

button6 = tk.Button(window, text="WATER", command=pump)
button6.grid(row=3, column=2)

button7 = tk.Button(window, text="SOIL", command=soil)
button7.grid(row=3, column=0)

label1 = tk.Label(window, text="Soil Moisture: ")
label1.grid(row=4, column=1, columnspan=3)

window.mainloop()