class Enhancer:

    def __init__(self, config, inventory):
        self.config = config
        self.inventory = inventory;

        print(self.config, self.inventory)
        self.proceed(int(self.config['options']['cycles']))


    def proceed(self, loops):
        for l in range(loops):
            self.stage(l)

    def stage(self, cycle):
        print(cycle)
