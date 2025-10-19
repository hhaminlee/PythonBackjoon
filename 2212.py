# 백준 2212 센서
import sys
input = sys.stdin.readline

n = int(input())
k = int(input())
sensors = list(map(int, input().split()))
sensors.sort(reverse=True)

sub_dist = []
for i in range(len(sensors)-1):
    sub_dist.append(sensors[i] - sensors[i+1])
sub_dist.sort(reverse=True)

print(sum(sub_dist[k-1:]))
