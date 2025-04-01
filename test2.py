# Proposed match_expr using the keyword pmatch
def test(num, num2):
    a = pmatch num:
        1: "One"
        2: "Two"
        3: pmatch num2:
           1: "One"
           2: "Two"
           3: "Three"
        _: "Number not between 1 and 3"
    return a


test(3, 2)
