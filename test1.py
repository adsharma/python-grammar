# match_stmt from python 3.10
def test(num: int):
    match num:
        # pattern 1
        case 1:
            print("One")
        # pattern 2
        case 2:
            print("Two")
        # pattern 3
        case 3:
            print("Three")
        # default pattern
        case _:
            print("Number not between 1 and 3")
