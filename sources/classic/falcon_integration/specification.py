import inspect

from spectree import SpecTree

from classic.components import (
    doublewrap,
    add_extra_annotation,
    Registry,
    component,
)


@component
class SpecificationRegistry(Registry):
    spec: SpecTree

    def register(self, resource):
        for name, member in inspect.getmembers(resource):
            if inspect.isfunction(member) and hasattr(member, '__spec__'):
                wrapper = self.spec.validate(**member.__spec__)(member)
                setattr(wrapper, '__original__', member)
                setattr(resource, name, wrapper)

    def unregister(self, resource):
        for name, member in inspect.getmembers(resource):
            if inspect.isfunction(member) and hasattr(member, '__original__'):
                setattr(resource, name, member.__original__)


@doublewrap
def specification(
    method,
    prop: str = 'spec',
    type_: SpecTree = SpecTree,
    **params,
):

    setattr(method, '__spec__', params)

    return add_extra_annotation(method, prop, type_)
