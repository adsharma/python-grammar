# Proposed match_expr using keywords pmatch/endpmatch
def test(num):
    a = pmatch num:
        1: "One"
        2: "Two"
        3: "Three"
        _: "Number not between 1 and 3"
    endpmatch

    return a


test(10)
