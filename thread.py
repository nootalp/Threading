import msvcrt
import time
import threading
import keyboard
from abc import ABC, abstractmethod


class Provident(ABC):
    @abstractmethod
    def occur(self):
        pass

    class BranchOne:
        def __init__(self, stop_event):
            self.stop = stop_event

        def line_one(self):
            while not self.stop.is_set():
                print("\nThread 1 running...\n")

                key_press = keyboard.is_pressed(hotkey='q')
                if key_press:
                    self.stop.set()
                    print("\nKey pressed, stopping threads...\n")
                    break
            print("\nThread 1 stopped.\n")

    class BranchTwo:
        def __init__(self, stop_event):
            self.stop = stop_event

        def line_two(self):
            while not self.stop.is_set():
                key_press = keyboard.is_pressed(hotkey='l')
                if key_press:
                    self.stop.set()
                    print("\nKey pressed, stopping thread...\n")
                    break
                print("\nThread 2 running...\n")

            print("\nThread 2 stopped.\n")


class Support(Provident):
    def __init__(self):
        self.stop_event = threading.Event()
        self.branch_one = Provident.BranchOne(self.stop_event)
        self.branch_two = Provident.BranchTwo(self.stop_event)
        self.running = False

    def pause_loop(self):
        if not self.running:
            self.running = True
            print("Script resumed.")
        elif self.running:
            self.running = False
            print("Paused.")

    def occur(self):
        pass


class SupportOne(Support):
    def occur(self):
        self.branch_one.line_one()


class SupportTwo(Support):
    def occur(self):
        self.branch_two.line_two()
        self.stop_event.set()


if __name__ == '__main__':
    actions = [SupportOne(), SupportTwo()]
    threads = [threading.Thread(target=action.occur) for action in actions]

    i = Support()

    keyboard.add_hotkey('insert', i.pause_loop)
    print("Press `insert` to start...")
    while True:
        if keyboard.is_pressed(hotkey='insert'):
            time.sleep(0.5)
            break

    if i.running:
        for thread in threads:
            thread.start()

    for thread in threads:
        thread.join()

    print("\nAll threads stopped.\n[***] Exiting...\n")
    time.sleep(1)

# Limpeza do buffer de entrada.
while msvcrt.kbhit():
    msvcrt.getch()
