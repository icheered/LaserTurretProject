class t:
    def __init__(self, id: int):
        self.id = id
    
    def testfunc(self):
        raise NotImplementedError

class b(t):
    def __init__(self, what):
        print(f"What: {what}")



id = 1
initialized = b(what="test")
initialized.testfunc()
