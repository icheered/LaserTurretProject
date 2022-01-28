import _thread
import time

class test:
    def __init__(self):
        self.i = 15

    def printFunc(self):
        print("Something:" + i)

def threadFunction(description, count):
  print(description)
 
  i = 0
 
  while i < count:
 
    print(description + ": " + str(i) )
    i=i+1
    time.sleep(1)

 


_thread.start_new_thread(threadFunction, ("Thread 1", 5))
_thread.start_new_thread(threadFunction, ("Thread 2", 5))
_thread.start_new_thread(threadFunction, ("Thread 3", 5))