# 백준 1339 단어 수학
# 긴 문자열 알파벳부터 높은 숫자를 배정
# 길이가 다음으로 긴 문자열이 나오면 그 문자에 숫자를 배정해야함

n = int(input())
words = [input().strip() for _ in range(n)]
weights = {}
for word in words:
    length = len(word)
    for i, ch in enumerate(word):
        weight = 10 ** (length - i - 1)
        weights[ch] = weights.get(ch, 0) + weight # 값이 없을 때에는 0을 가져오기

sorted_weights = sorted(weights.items(), key=lambda x: x[1], reverse=True)

val = 9
num_to_char = {}
for ch, _ in sorted_weights:
    num_to_char[ch] = val
    val -= 1

words_to_int = ''
result = 0
for word in words:
    words_to_int = ''.join(str(num_to_char[ch]) for ch in word)
    result += int(words_to_int)
print(result)