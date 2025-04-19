import platform
import time
import os
import zipfile
import threading
import subprocess

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

    def download_model(self):
        dropbox_url = "https://www.dropbox.com/scl/fi/sb8pa3w7gwvb1er1wd7le/phish_gpt2.zip?rlkey=zg6nc2ng1qhezvu4wu16qez25&st=vrdayq26&dl=1"
        zip_path = "phish_gpt2.zip"

        try:
            print("*** Downloading Phish_GPT2 Model with aria2c... ***")
      
            command = [
                "aria2c", 
                "-x", "16",  
                "-s", "16",  
                dropbox_url, 
                "-d", ".",    
                "-o", zip_path  
            ]
   
            subprocess.run(command, check=True)
            
            print("*** Zip Downloaded. Extracting... ***")
            time.sleep(1)

            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(".")

            os.remove(zip_path)
            print("*** Extraction Completed, Launching ToolKit... ***")

        except Exception as e:
            print(f" *** Failed to Download/Extract Model Folder: {str(e)} ***")
            exit(1)

    def check_and_download_model(self):
        if not os.path.exists("phish_gpt2"):
            print("*** Model Folder 'phish_gpt2' Not Found. Downloading Zip... ***")

            download_thread = threading.Thread(target=self.download_model)
            download_thread.start()
            download_thread.join()

        else:
            print("*** Phish_GPT2 Folder Exists, Launching ToolKit... ***")

    def start_up(self):
        print("\033[92m" + self._banner + "\033[0m") 
        print("*** Detecting Host Operating System: " + self.os_system + " ***")
        time.sleep(2)

        self.check_and_download_model()

        time.sleep(2)
        from mvc import MVC
        mvc = MVC(self.os_system)
        mvc.mainloop()

if __name__ == "__main__":
    main = Main()
    main.start_up()
