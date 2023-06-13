from time import sleep


def ci():
    def CI(sum, rate, time):
        if time == 0:
            return sum
        if time == 1:
            return float(sum) + (float(sum) * float(rate) / 100)
        else:
            return CI(sum, rate, (time - 1)) + (CI(sum, rate, (time - 1)) * rate / 100)

    print("enter the values to calculate compound interest:")
    sm = float(input("sum : "))
    rt = float(input("Rate : "))
    tm = float(input("Time : "))
    if tm < 23:
        for s in range(int(tm)):
            if s == 0:
                print(f"Interest for {s + 1}st year: {(CI(sm, rt, s + 1) - CI(sm, rt, s))}")
                sleep(.5)
            elif s == 1:
                print(f"Interest for {s + 1}nd year: {(CI(sm, rt, s + 1) - CI(sm, rt, s))}")
                sleep(.5)
            elif s == 2:
                print(f"Interest for {s + 1}rd year: {(CI(sm, rt, s + 1) - CI(sm, rt, s))}")
                sleep(.5)
            else:
                print(f"Interest for {s+1}th year: {(CI(sm, rt, s+1) - CI(sm, rt, s))}")
                sleep(.5)
    else:
        print("Can't calculate the interest for more than 22 years")
    print(f"total amount:{CI(sm, rt, tm)}")
    sleep(1)

