n = int(input())
nums = list(map(int,input().split()))
arr = []
for i in nums:
    arr.append(i)
max_arr_index = arr.index(max(arr))
max_arr = max(arr)
min_arr = min(arr)
count = 0
for index in range(n):
    if arr[index] == max_arr:
        arr[index] = min_arr
    print(arr[index], end= " ")

                        


    
