n = int(input())
students = [input().split() for _ in range(n)]
students.sort(key = lambda x: (int(x[3]), int(x[2]), int(x[1])))

print(students[-1][0], '\n', students[0][0], sep='')