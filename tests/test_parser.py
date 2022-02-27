from simplec import syntax


def _callFUT(*args, **kwargs):
    from simplec.parser import parse

    return parse(*args, **kwargs)


# def test_identifier():
#     assert _callFUT("a") == syntax.NameExpr(name="a", offset=4)
