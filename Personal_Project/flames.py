# FLAMES
name1 = input("Enter the first name: ")
name2 = input("Enter the second name: ")
name1 = name1.lower().replace(" ", "")
name2 = name2.lower().replace(" ", "")

name1list = list(name1)
name2list = list(name2)

common = []
for i in name1list[:]:
    if i in name2list:
        common.append(i)
        name1list.remove(i)
        name2list.remove(i)

count = len(name1list) + len(name2list)

result = ["Friends", "Love", "Affection", "Marriage", "Enemy", "Siblings"]

while len(result) > 1:
    index = (count - 1) % len(result)
    result.pop(index)

print(result[0])
