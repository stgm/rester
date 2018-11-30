from collections import defaultdict

nested_dict = lambda: defaultdict(nested_dict)
nest = nested_dict()

nest[0][1]['hoi'][3][4][5] = 6

print(nest)
