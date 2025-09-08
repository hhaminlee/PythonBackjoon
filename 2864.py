a, b = input().split()
max_a_five = a.replace('6', '5')
max_b_five = b.replace('6', '5')
max_a_six = a.replace('5', '6')
max_b_six = b.replace('5', '6')

max_five = int(''.join(max_a_five)) + int(''.join(max_b_five))
max_six = int(''.join(max_a_six)) + int(''.join(max_b_six))
print(max_five, max_six)