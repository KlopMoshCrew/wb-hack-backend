from sklearn.cluster import AffinityPropagation
import numpy as np

def read_data(path):
	test_array = [
		[
			0,
			{
				'key1':'test01'
			}
		],
		[
			1,
			{
				'key1':'test11',
				'key2':'test12'
			}
		],
		[
			2,
			{
				'key1':'test21',
				'key2':'test22'
			}
		],

	]
	return test_array

def process_data(array):
	for item_id in range(len(array)):
		for key in array[item_id][1]:
			array[item_id][1][key] = str(array[item_id][1][key]).split(';')[0]

	all_options = {}
	for item in array:
		for option in item[1]:
			if option not in all_options:
				all_options[option] = [item[1][option]]
			else:
				if item[1][option] not in all_options[option]:
					all_options[option].append(item[1][option])

	option_means = {}
	for option in all_options:
		option_means[option] = [0 ,0]

	for item in array:
		for option in item[1]:
			option_means[option][0] += all_options[option].index(item[1][option])
			option_means[option][1] += 1 

	real_option_means = {}
	for option in option_means:
		real_option_means[option] = np.rint( option_means[option][0] /  option_means[option][1])

	for item_id in range(len(array)):
		for option in all_options:
			if option not in array[item_id][1]:
				array[item_id][1][option] = real_option_means[option]
			else:
				array[item_id][1][option] = all_options[option].index(item[1][option])

	new_arr = np.zeros((len(array), len(all_options) + 1))
	for item in range(len(array)):
		new_arr[item][0] = array[item][0]
		for option in range(len(array[item][1])):
			new_arr[item][option + 1] = list(array[item][1].values())[option]

	return new_arr.astype(int)



def cluster_data(array, target_id):
	labels = AffinityPropagation(random_state=5).fit_predict(array[:,1:])
	print(labels)
	target_label = labels[target_id]
	target_items = []
	for i in range(len(array)):
		if labels[i] == target_label:
			target_items.append(array[i][0])

	return target_items


if __name__ == "__main__":
	data = read_data('')
	target_id = 1
	processed = process_data(data)
	print(processed)
	result_items = cluster_data(processed, target_id)
	print("result", result_items)
