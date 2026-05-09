def add(a, b):
    return a + b
def classify(n):
    if n > 0:
        return "positive"
    elif n == 0:
        return "zero"
    else:
        return "negative"
print("=== Merror Full Test ===")
result = add(10, 32)
print("10 + 32 = " + str(result))
print(classify(5))
print(classify(0))
print(classify(-3))
count = 0
while count < 3:
    print("count: " + str(count))
    count = count + 1
print("squares:")
for i in range(1, 6):
    print((str(i) + "^2 = ") + str(i * i))
print("even numbers < 10 (skip 4):")
for n in range(10):
    if n == 4:
        continue
    if n > 7:
        break
    if (n * 1) == n:
        print(str(n))
flag = True
nothing = None
print("flag is: " + str(flag))
print("nothing is: " + str(nothing))
print("=== Done ===")
