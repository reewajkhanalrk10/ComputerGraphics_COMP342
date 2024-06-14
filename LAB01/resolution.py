# pip install screeninfo
from screeninfo import get_monitors

def get_device_resolution():
    for monitor in get_monitors():
        return (monitor.width, monitor.height)

# Example usage
try:
    width, height = get_device_resolution()
    print(f"Device resolution: {width}x{height}")
except Exception as e:
    print(f"Error getting device resolution: {e}")
