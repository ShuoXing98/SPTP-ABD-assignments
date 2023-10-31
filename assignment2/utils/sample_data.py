import random

n = 60
sample_list = random.sample(range(2500), n)

old_f = open(f"Data/cover_n2500.txt", 'r', encoding='utf-8')

new_f= open(f"Data/cover_n2500_{n}.txt", 'w', encoding='utf-8')

lines = old_f.readlines()

for i in sample_list:
    new_f.write(lines[i])
    
old_f.close()
new_f.close()
