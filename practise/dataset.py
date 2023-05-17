import itertools

features = ['color', 'fabric_type', 'time_available', 'soil_level', 'fabric_care', 'size', 'water_temp']
color_dict = {'white': 0, 'light': 1, 'dark': 2, 'mix': 3}
fabric_type_dict = {'cotton': 0, 'silk': 1, 'wool': 2 , 'synthetic': 3, 'jeans': 4, 'mix': 5}
time_available = [15, 30, 60, 90, 120]
soil_level_dict = {'light': 0, 'normal': 1, 'heavy': 2}
fabric_care_dict = {'delicate': 0, 'normal': 1, 'heavy': 2}
size_dict = {'small': 0, 'medium': 1, 'large': 2}
water_temp_dict = {'cold': 0, 'hot': 1, 'warm': 2}
recommendations = []
fabric_type = ['cotton', 'silk', 'wool','synthetic', 'jeans']

print(f'Unique Values For Each Feature\n')
print('color')
[print(f'{key}: {str(value)}')for key, value in color_dict.items()]
print('\nfabric_type')
[print(f'{key}: {str(value)}')for key, value in fabric_type_dict.items()]
print('\ntime_available')
[print(elem) for elem in time_available]
print('\nsoil_level')
[print(f'{key}: {str(value)}')for key, value in soil_level_dict.items()]
print('\nfabric_care')
[print(f'{key}: {str(value)}')for key, value in fabric_care_dict.items()]
print('\nsize')
[print(f'{key}: {str(value)}')for key, value in size_dict.items()]
print('\nwater_temp')
[print(f'{key}: {str(value)}')for key, value in water_temp_dict.items()]

fabric_type_combs = list(itertools.combinations(fabric_type_dict.keys(), 2))
fabric_type_combs += list(itertools.combinations(fabric_type_dict.keys(), 3))
fabric_type_combs += list(itertools.combinations(fabric_type_dict.keys(), 4))
fabric_type += fabric_type_combs
print(fabric_type, len(fabric_type))





