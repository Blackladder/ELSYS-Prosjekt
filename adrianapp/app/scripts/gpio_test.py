from gpiozero import Button

print("Waiting for button press!")

button = Button(27)
button.wait_for_press()
print("The button was pressed!")
