import platform
import time

class Main():
    _banner = ('''
                       _                _   ___  
  /\/\    __ _  _ __  (_) _ __   _   _ | | ( _ ) 
 /    \  / _` || '_ \ | || '_ \ | | | || | / _ \ 
/ /\/\ \| (_| || | | || || |_) || |_| || || (_) |
\/    \/ \__,_||_| |_||_|| .__/  \__,_||_| \___/ 
                         |_|                                                                                         
    ''')

    def __init__(self):
        self.os_system = platform.system()

    def start_up(self):
        print("\033[92m" + self._banner + "\033[0m") 
        print("*** Detecting Host Operating System: " + self.os_system + " ***")
        time.sleep(2)

        from mvc import MVC
        mvc = MVC(self.os_system)
        mvc.mainloop()
        

main = Main()
main.start_up()
