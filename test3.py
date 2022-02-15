from win10toast import ToastNotifier
import time
import bidict


a = bidict()

toaster = ToastNotifier()

# header = input("What You Want Me To Remember\n")
# text = input("Releated Message\n")
# time_min = float(input("In how many minutes?\n"))

header = "What You Want Me To Remember\n"
text = "Releated Message\n"
time_min = 10

# time_min = time_min * 60
print("Setting up reminder..")
time.sleep(2)
print("all set!")
time.sleep(time_min)
toaster.show_toast(f"{header}", f"{text}", duration=10, threaded=True, icon_path=r'C:/Users/admin/Desktop/20211103_xiaogui/test.ico')
while toaster.notification_active():
    time.sleep(0.005)
