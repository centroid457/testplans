from typing import *


# =====================================================================================================================
# TODO: move to funcs_aux
# TODO: move to funcs_aux
# TODO: move to funcs_aux
# TODO: move to funcs_aux
# TODO: move to funcs_aux


# =====================================================================================================================
def _explore_and_why_it_need():
    class Cls:
        pass

    # THIS IS OK!!!!!=======
    if False:
        result = Cls.hello

    # IT DEPANDS!!!!!=======
    print(
        all([
            False,
            False and Cls.hello1,  #this is OK!!!!
            # True and Cls.hello2,  #this is EXX!!!! AttributeError: type object 'Cls' has no attribute 'hello2'
        ])
    )

    # THIS IS EXX!!!!!=======
    result = False
    # result &= Cls.hello3,  #this is EXX!!!! AttributeError: type object 'Cls' has no attribute 'hello3'

    print(
        all([
            False,
            Cls,
            # Cls.hello4, #this is EXX!!!! AttributeError: type object 'Cls' has no attribute 'hello4'
        ])
    )

    def func():
        return Cls.hello5  # this is OK!!!!

    # func()      # AttributeError: type object 'Cls' has no attribute 'hello5'


# =====================================================================================================================
class ChainStep:
    pass


# =====================================================================================================================
