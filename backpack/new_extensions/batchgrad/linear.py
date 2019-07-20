from backpack.core.derivatives.linear import (LinearDerivatives,
                                              LinearConcatDerivatives)

from backpack.new_extensions.batchgrad.base import BatchGradBase


class BatchGradLinear(BatchGradBase):
    def __init__(self):
        super().__init__(
            derivatives=LinearDerivatives(),
            params=["bias", "weight"]
        )


class BatchGradLinearConcat(BatchGradBase):
    def __init__(self):
        super().__init__(
            derivatives=LinearConcatDerivatives(),
            params=["weight"]
        )
