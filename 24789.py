# 백준 24789 Railroad 
x, y = list(map(int, input().split()))
# x 길, y 길이 모두 연결되어야함.
# 홀수일 경우 모든 길이 연결되지 않음
# 짝수일 때는 모든 길이 연결되기 때문에 꼭짓점의 갯수가 짝수 -> 가능 홀수 -> 불가능
print('possible' if (x*4+y*3) % 2 == 0 else 'impossible')