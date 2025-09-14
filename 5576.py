w_list = [int(input()) for _ in range(10)]
k_list = [int(input()) for _ in range(10)]

w_list.sort(reverse=True)
k_list.sort(reverse=True)

print((w_list[0] + w_list[1] + w_list[2]), (k_list[0] + k_list[1] + k_list[2]))