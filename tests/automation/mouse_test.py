import time

from services.mouse import MouseService

mouse = MouseService()

print("Move your mouse...")
print("Waiting 5 seconds...")

time.sleep(5)

pos = mouse.position()

print("\nMouse Position:")
print(f"X = {pos.x}")
print(f"Y = {pos.y}")