from system.window_manager import WindowManager


wm = WindowManager()


print("=" * 40)
print("     AYESHA Window Detector Test")
print("=" * 40)



print("\nActive Window:")
print(
    wm.get_active_window()
)



print("\nAll Windows:")

windows = wm.get_all_windows()

for w in windows:

    if w.strip():

        print("-", w)



print("\nYouTube Open:")

if wm.is_youtube_open():

    print("True - YouTube detected")

else:

    print("False - YouTube not found")