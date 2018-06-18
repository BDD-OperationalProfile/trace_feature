

class Method:

    def __init__(self):
        self.method_name = ""
        self.class_name = ""
        self.class_path = ""


    def __str__(self):
        return "\t" + self.method_name + " (" + self.class_name + "):  " + self.class_path  