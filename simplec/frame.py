import attr


@attr.s(slots=True)
class Var:
    name = attr.ib()
    symbol = attr.ib()
    offset = attr.ib()


@attr.s(slots=True)
class Frame:
    size = attr.ib()
    vars = attr.ib(factory=dict)
