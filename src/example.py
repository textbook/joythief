from joythief.data_structures import DictContaining
from joythief.objects import InstanceOf

assert dict(foo=123, bar=456) == DictContaining(foo=InstanceOf(int))
