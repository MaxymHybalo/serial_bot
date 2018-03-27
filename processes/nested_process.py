

class NestedProcessor:

    def __init__(self, instruction):
        self.nested = instruction
        self.process = 'nested'

    def handle(self):
        from processors import InstructionProcessor
        queue = InstructionProcessor(self.nested)
        queue.process()
