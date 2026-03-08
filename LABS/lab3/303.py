import sys

TRI_TO_DIG = {
    "ZER": "0",
    "ONE": "1",
    "TWO": "2",
    "THR": "3",
    "FOU": "4",
    "FIV": "5",
    "SIX": "6",
    "SEV": "7",
    "EIG": "8",
    "NIN": "9",
}

DIG_TO_TRI = {v: k for k, v in TRI_TO_DIG.items()}

def decode_triplets(t: str) -> int:
    # t length should be multiple of 3
    digits = []
    for i in range(0, len(t), 3):
        digits.append(TRI_TO_DIG[t[i:i+3]])
    return int("".join(digits)) if digits else 0

def encode_number(x: int) -> str:
    if x == 0:
        return "ZER"
    if x < 0:
        return "-" + encode_number(-x)  # на всякий случай
    return "".join(DIG_TO_TRI[ch] for ch in str(x))

def main():
    s = sys.stdin.readline().strip()

    op_pos = -1
    op = ""
    for i, ch in enumerate(s):
        if ch in "+-*":
            op_pos = i
            op = ch
            break

    left = s[:op_pos]
    right = s[op_pos + 1:]

    a = decode_triplets(left)
    b = decode_triplets(right)

    if op == "+":
        res = a + b
    elif op == "-":
        res = a - b
    else:  # "*"
        res = a * b

    sys.stdout.write(encode_number(res))

if __name__ == "__main__":
    main()
