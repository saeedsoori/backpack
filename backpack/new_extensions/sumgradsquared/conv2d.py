from backpack.utils.utils import einsum
from backpack.utils import conv as convUtils
from backpack.new_extensions.firstorder import FirstOrderExtension


class SGSConv2d(FirstOrderExtension):
    def __init__(self):
        super().__init__(params=["bias", "weight"])

    def bias(self, ext, module, grad_input, grad_output, backproped):
        return (grad_output[0].sum(3).sum(2)**2).sum(0)

    def weight(self, ext, module, grad_input, grad_output, backproped):
        X, dE_dY = convUtils.get_weight_gradient_factors(
            module.input0, grad_output[0], module)
        d1 = einsum('bml,bkl->bmk', (dE_dY, X))
        return (d1**2).sum(0).view_as(module.weight)


class SGSConv2dConcat(FirstOrderExtension):
    def __init__(self):
        super().__init__(params=["weight"])

    def weight(self, ext, module, grad_input, grad_output, backproped):
        X, dE_dY = convUtils.get_weight_gradient_factors(
            module.input0, grad_output[0], module)

        if module.has_bias():
            X = module.append_ones(X)

        d1 = einsum('bml,bkl->bmk', (dE_dY, X))
        return (d1**2).sum(0).view_as(module.weight)

