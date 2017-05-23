
def solution(S):
    b = int(S, 2)
    print(b)
    count = 0
    while b != 0:
        count = count + 1
        v = b % 2 == 0
        if v == True:
            b = b / 2
            print(b)
        else:
            b = b - 1
            print(b)
    print(count)
    return count

solution("1111")