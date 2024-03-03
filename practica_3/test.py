procesos = [{'id': 1, 'tiempo': 14, 'operacion': '94 - 56'}, {'id': 2, 'tiempo': 18, 'operacion': '80 + 76'}, {'id': 3, 'tiempo': 18, 'operacion': '91 - 16'}, {'id': 4, 'tiempo': 13, 'operacion': '21 % 62'}, {'id': 5, 'tiempo': 8, 'operacion': '16 ** 82'}, {'id': 6, 'tiempo': 17, 'operacion': '95 - 2'}, {'id': 7, 'tiempo': 16, 'operacion': '89 % 83'}, {'id': 8, 'tiempo': 8, 'operacion': '87 + 5'}, {'id': 9, 'tiempo': 9, 'operacion': '95 - 93'}, {'id': 10, 'tiempo': 10, 'operacion': '26 + 27'}]

print(sum(tiempo['tiempo'] for tiempo in procesos))



