import random

sample_list = random.sample(range(4500), 1000)

old_f = open(f"data/corel.txt", 'r', encoding='utf-8')

new_f= open(f"data/corel_1000.txt", 'w', encoding='utf-8')

lines = old_f.readlines()

for i in sample_list:
    new_f.write(lines[i])
    
old_f.close()
new_f.close()
