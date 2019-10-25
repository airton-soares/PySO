from functions.function_type import FunctionType
from functions.rastrigin import Rastrigin
from functions.sphere import Sphere


def build_function(typ):
    if typ == FunctionType.SPHERE.value:
        return Sphere()
    elif typ == FunctionType.RASTRIGIN.value:
        return Rastrigin()
