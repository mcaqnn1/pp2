import math

def is_prime_wilson(n):
    return n > 1 and (math.factorial(n - 1) + 1) % n == 0

def print_primes(nums):
    found = False
    for n in nums:
        if is_prime_wilson(n):
            print(n, end=" ")
            found = True
    return found

nums = list(map(int, input().split()))

if not print_primes(nums):
    print("No primes")
