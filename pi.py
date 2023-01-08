def pi_bbp(n):
    result = 0
    for k in range(n):
        result += (1 / (16 ** k)) * ((4 / (8 * k + 1)) - (2 / (8 * k + 4)) - (1 / (8 * k + 5)) - (1 / (8 * k + 6)))
        print(result)
    return result

result = pi_bbp(10)

with open("pi.txt", "w") as f:
    f.write(str(result))