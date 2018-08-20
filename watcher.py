import time
import ntpath
import sys
from watchdog.observers import Observer
from watchdog.events import RegexMatchingEventHandler
class LogFilesModificationHandler(RegexMatchingEventHandler):
    def __init__(self):
        super().__init__(ignore_directories=True)
        self.files = {}
    def on_modified(self, event):
        time.sleep(0.5)
        file_name = ntpath.basename(event.src_path)
        if file_name != "kareem.log":
            return
        if  event.src_path not in self.files:
            self.files[event.src_path] = 0

        self.read_new_lines(event.src_path)
    def read_new_lines(self,path):
        try:
            file = open(path,'r')
            lines = file.readlines()
            number_of_lines = len(lines)
            if self.files[path]== 0:
                if number_of_lines>0:
                    self.files[path] = number_of_lines
                    print("{} file added with {} lines".format(path,number_of_lines))
            elif number_of_lines< self.files[path]:
                self.files[path] = number_of_lines
                print("file {} is re-written with {} new lines".format(path,number_of_lines))
            else:
                tail_length = 0 - (number_of_lines - self.files[path])
                self.files[path] = number_of_lines
                print("{} lines added for file {}".format(abs(tail_length),path))
                print(lines[-1:tail_length-1:-1])
        except Exception:
            raise Exception

if __name__ == '__main__':
    log_file_modification_handler = LogFilesModificationHandler()
    observer = Observer()
    path = sys.argv[1] if len(sys.argv) > 1 else '.'
    observer.schedule(log_file_modification_handler,path=path,recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        print("Done")
    observer.join()