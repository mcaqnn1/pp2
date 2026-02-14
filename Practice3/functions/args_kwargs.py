def f(a, *args, **kwargs):
    print(a, args, kwargs)

f(1, 2, 3, x=10, y=20)