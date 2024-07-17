import torch
import torch.nn as nn

class SimpleGrad(nn.Module):

    def __init__(self, eos):
        super().__init__()
        self.eos = eos # eos = saftgammamie(component), assumes pure
        self.method_dict = {
            "density": self.eos.density
        }
    
    def forward(self, component, method):
        method_fn = self.method_dict[method]
        return method_fn(component)
