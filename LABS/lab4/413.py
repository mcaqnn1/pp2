import json
import re
from types import SimpleNamespace


_token_re = re.compile(r"""
    ([A-Za-z_]\w*)          # user, friends, name
  | \[(\d+)\]               # [0], [12]
  | \[(['"])(.*?)\3\]       # ["key"], ['key']
""", re.VERBOSE)


def get_by_path(data, path: str):
    path = path.strip()

    # allow $ / $. prefix
    if path.startswith("$."):
        path = path[2:]
    elif path.startswith("$"):
        path = path[1:]

    cur = data
    pos = 0

    for m in _token_re.finditer(path):
        # between tokens only allow dots/spaces
        between = path[pos:m.start()]
        if between and not all(ch in ". \t" for ch in between):
            raise ValueError(f"Bad path part: {between!r}")
        pos = m.end()

        name, idx, key = m.group(1), m.group(2), m.group(4)

        if name:
            if isinstance(cur, dict):
                cur = cur[name]
            else:
                cur = getattr(cur, name)
        elif idx:
            cur = cur[int(idx)]
        else:
            # ["key"] or ['key']
            if isinstance(cur, dict):
                cur = cur[key]
            else:
                cur = getattr(cur, key)

    return cur


def to_plain(x):
    """SimpleNamespace -> dict, list -> list (print үшін ыңғайлы)"""
    if isinstance(x, SimpleNamespace):
        return {k: to_plain(v) for k, v in vars(x).items()}
    if isinstance(x, list):
        return [to_plain(v) for v in x]
    if isinstance(x, dict):
        return {k: to_plain(v) for k, v in x.items()}
    return x


class QueryEngine:
    def __init__(self, js_obj: str, js_met_arr: list[str], n: int):
        self.js_obj = js_obj
        self.js_met_arr = js_met_arr
        self.n = n

    def func(self):
        obj = json.loads(self.js_obj, object_hook=lambda d: SimpleNamespace(**d))
        for i in range(self.n):
            val = get_by_path(obj, self.js_met_arr[i])

            # әдемі шығару:
            val_plain = to_plain(val)
            if isinstance(val_plain, (dict, list)):
                print(json.dumps(val_plain, ensure_ascii=False))
            else:
                print(val_plain)


# ---- input / run ----
js_obj = input().strip()
n = int(input())
js_met_arr = [input().strip() for _ in range(n)]

cl = QueryEngine(js_obj, js_met_arr, n)
cl.func()