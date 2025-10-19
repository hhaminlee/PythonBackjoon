# 백준 20920 영단어 암기는 괴로워
import sys
from collections import Counter
input = sys.stdin.readline

n, m = list(map(int, input().split()))
word_list = [input().strip() for _ in range(n)]
word_list = [word for word in word_list if len(word) >= m]

counter = Counter(word_list)
# counter.keys는 단어를 한번씩만 포함해줌
sorted_list = sorted(counter.keys(), key=lambda x: (-counter[x], -len(x), x))

print("\n".join(sorted_list))