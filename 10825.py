n = int(input())
students = []
for _ in range(n):
    students.append(input().split())
sorted_student = sorted(students, key=lambda x: (-int(x[1]), int(x[2]), -int(x[3]), x[0]))

for student in sorted_student:
    print(student[0])