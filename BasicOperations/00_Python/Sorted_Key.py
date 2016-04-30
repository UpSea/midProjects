students = [('john', 'A', 15), ('jane', 'C', 12), ('dave', 'B', 10)]
b = sorted(students, key=lambda s: s[1],reverse=False)

print(students)
print(b)