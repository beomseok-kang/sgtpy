from math import isclose
import torch

def test_func(func1, func2, input):
    # assume func1 is the reference function
    output1 = func1(input) # numpy or float (likely)
    output2 = func2(input) # torch
    if isinstance(output1, float):
        assert isclose(output1, output2.item(), rel_tol=1e-6, abs_tol=1e-6), "Not close. output1: {}, output2: {}".format(output1, output2)
    else:
        output2 = output2.numpy()
        assert output1.shape == output2.shape, "Shapes are different. output1: {}, output2: {}".format(output1.shape, output2.shape)
        dim = output1.dim
        assert dim == 1, "Dimension is greater than 1. output1: {}, output2: {}".format(output1.dim, output2.dim)
        for i in range(len(output1)):
            assert isclose(output1[i], output2[i], rel_tol=1e-6, abs_tol=1e-6), "Not close.\noutput1: {},\noutput2: {}".format(output1, output2)
    return True

# test numpy to torch
# assumes func is a torch function, hence takes in torch tensor.
# Then, outputs the resulting function in numpy array.
def tnt(func, np_arr):
    ten = torch.from_numpy(np_arr) # tensor
    output = func(ten)
    if output.dim() == 0:
        return output.item()
    else:
        return output.numpy()
