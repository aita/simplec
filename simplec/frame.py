import attr


@attr.s(slots=True)
class Var:
    name = attr.ib()
    offset = attr.ib()


@attr.s(slots=True)
class Frame:
    vars = attr.ib(factory=dict)
    offset = attr.ib(default=4)

    def get_var(self, name):
        return self.vars.get(name)

    def new_var(self, name):
        self.offset += 4
        var = Var(name, self.offset)
        self.vars[name] = var
        return var

    def size(self):
        return self.offset
