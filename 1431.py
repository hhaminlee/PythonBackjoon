import sys
input = sys.stdin.readline

n = int(input())
serial = [input().strip() for _ in range(n)]

sorted_serial = sorted(serial, key = lambda x : (len(x), sum(int(ch) for ch in x if ch.isdigit()), x))

print("\n".join(map(str, sorted_serial)))