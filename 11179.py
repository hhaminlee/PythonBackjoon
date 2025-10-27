# 백준 11179 2진수 뒤집기

n = int(input())

bin_n = format(n, 'b')
reversed_bin_n = bin_n[::-1]
# 2진수 문자열을 10진수 정수로 변환하는 코드
print(int(reversed_bin_n, 2))