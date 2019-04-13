class Method:

    def __init__(self):
        self.method_id = ""
        self.method_name = ""
        self.class_name = ""
        self.class_path = ""

    def __str__(self):
        print("METHOD:")
        print("\t\t\t name: " + self.method_name)
        print("\t\t\t classe: " + self.class_name)
        print("\t\t\t path: " + self.class_path)
        return ''


# Ver a necessidade de utilizar a modelo de Describe tb.. acho que não precisa.
# class Describe:
#     def __init__(self):
#         self.description = ""
#         self.line = None


class It:
    def __init__(self):
        self.project = ""
        self.file = ""
        self.description = ""
        self.line = None
        self.executed_methods = []

    def __str__(self):
        return self.description

