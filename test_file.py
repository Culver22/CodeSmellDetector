# test_smells.py

class LargeExampleClass:
    def method_one(self):
        pass

    def method_two(self):
        pass

    def method_three(self):
        pass

    def method_four(self):
        pass

    def method_five(self):
        pass

    def method_six(self):
        pass

    def method_seven(self):
        pass

    def method_eight(self):
        pass

    def method_nine(self):
        pass

    def method_ten(self):
        pass

    def method_eleven(self):
        pass


def example_long_function():
    total = 0
    for i in range(10):
        total += i
        print(f"Step {i}: total is now {total}")
        total += 1
        total *= 2
        total -= i
        print("Doing more math...")
        if total % 2 == 0:
            print("Even total")
        else:
            print("Odd total")
        for j in range(2):
            print(f"Nested loop level 2: {j}")
        print("End of iteration\n")

    print("Continuing with more lines...")
    a = 1
    b = 2
    c = 3
    d = 4
    e = 5
    f = 6
    g = 7
    h = 8
    i = 9
    j = 10
    k = 11
    l = 12
    m = 13
    n = 14
    o = 15
    p = 16
    q = 17
    r = 18
    s = 19
    t = 20
    print("Done!")


example_long_function()


def too_many_parameters(a, b, c, d, e, f, g):
    # Function with many parameters
    return a + b + c + d + e + f + g


def deeply_nested():
    if True:
        if True:
            for i in range(5):
                while i < 5:
                    try:
                        if i == 3:
                            print("Deep Nesting")
                    except Exception as e:
                        print(e)
