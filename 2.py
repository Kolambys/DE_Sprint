def palindrom(n):
    n = n.replace(" ", "")
    if n == n[::-1]:
        return True
    else:
        return False

X = input()
print(palindrom(X))