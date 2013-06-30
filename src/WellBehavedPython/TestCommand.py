class TestCommand:

    def __init__(self, function):
        self.function = function

    def run(self):
        print("TestCommand.run()")
        self.function()
