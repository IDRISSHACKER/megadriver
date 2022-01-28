import os

class Utils:
    def __init__(self):
        super(Utils, self).__init__()
    
    def verfifyTrueCafeData(self):
        path = os.path.join("C:","/","trueCafeData")
        if os.path.exists(path):
            return (path, True)
        else:
            return (path, False)
