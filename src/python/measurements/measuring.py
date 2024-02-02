from collections import defaultdict


# file_path_unstr = 'time-measure-unstr.txt'
file_path_str = 'time-measure-str.txt'
with open(file_path_str, 'r') as file:
    file_content = file.read()

t_numbers_data = defaultdict(list)

for line in file_content.strip().split('\n'):
    t_number, value = line.split('-')
    t_numbers_data[t_number].append(float(value))

# min, max, and avg
result = {}
for t_number, values in t_numbers_data.items():
    result[t_number] = {
        'min': min(values),
        'max': max(values),
        'avg': sum(values) / len(values)
    }

# results
# with open("results-unstr.txt", "a+") as file_res:
with open("results-str.txt", "a+") as file_res:
    for t_number, stats in result.items():
        file_res.write(f"{t_number}: Min = {stats['min']}, Max = {stats['max']}, Avg = {stats['avg']}\n")

# print(f"{t_number}: Min = {stats['min']}, Max = {stats['max']}, Avg = {stats['avg']}")