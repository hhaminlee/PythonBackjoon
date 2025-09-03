# 3의 배수 + 5의 배수 = fizzbuzz -> 15의 배수
# 3의 배수 + !5의 배수 = fizz -> 3의 배수인데 15의 배수 제외
# !3의 배수 + 5의 배수 = buzz -> 5의 배수인데 15의 배수 제외
# !3의 배수 + !5의 배수 = i

fiz = [input() for _ in range(3)]
result = 0

if fiz[0].isdigit():
    result += int(fiz[0]) + 3
elif fiz[1].isdigit():
    result += int(fiz[1]) + 2
elif fiz[2].isdigit():
    result += int(fiz[2]) + 1

if result % 15 == 0:
    print('FizzBuzz')
elif result % 5 == 0:
    print('Buzz')
elif result % 3 == 0:
    print('Fizz')
else:
    print(result)