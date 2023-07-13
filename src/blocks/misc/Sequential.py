from ..BaseBlock import BaseBlock

class Sequential(BaseBlock):
    def __init__(self, *blocks):
        BaseBlock.__init__(self)
        self.blocks = blocks
        self.name = 'Sequential: ' + str([type(b) for b in self.blocks])

    def run(self, samples):
        for block in self.blocks:
            samples = block.run(samples)
            block.emit(samples) # forward to other branches
        return samples
