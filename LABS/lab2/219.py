n = int(input())
Aida = []
for index in range(n):
    name_dorama,episodes = input().split()
    Aida.append((name_dorama,episodes))
    episodes = int(episodes)

for name_dorama,episodes in set(Aida):
    if Aida.count(name_dorama) == 2:
        episodes += episodes
    print(name_dorama,episodes)