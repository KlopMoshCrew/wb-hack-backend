#from sklearn.cluster import AffinityPropagation
from sklearn.cluster import MiniBatchKMeans
import numpy as np
import pickle
import json

filename = 'finalized_model.sav'


def read_data(path):
	# test_array = [
	# 	[
	# 		0,
	# 		{
	# 			'key1':'test01'
	# 		}
	# 	],
	# 	[
	# 		1,
	# 		{
	# 			'key1':'test11',
	# 			'key2':'test12'
	# 		}
	# 	],
	# 	[
	# 		2,
	# 		{
	# 			'key1':'test21',
	# 			'key2':'test22'
	# 		}
	# 	],
	#
	# ]

	with open('nm.json', 'r', encoding='utf-8') as j:
		json_data = json.load(j)

	result = []

	for ecom in json_data:
		try:
			ecom_dict = {}
			for options in ecom[1]:
				try:
					ecom_dict[options['name']] = options['value']
				except Exception:
					pass
			result.append([ecom[0], ecom_dict])
		except:
			pass

	return result


def process_data(array):
	for item_id in range(len(array)):
		for key in array[item_id][1]:
			array[item_id][1][key] = str(array[item_id][1][key]).split(';')[0].lower()

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
		real_option_means[option] = option_means[option][0] / option_means[option][1]

	for item_id in range(len(array)):
		for option in all_options:
			if option not in array[item_id][1]:
				array[item_id][1][option] = real_option_means[option]
			else:
				array[item_id][1][option] = all_options[option].index(array[item_id][1][option])

	new_arr = np.zeros((len(array), len(all_options)))
	ids = []
	for item in range(len(array)):
		ids.append(array[item][0])
		for option in range(len(array[item][1])):
			new_arr[item][option] = list(array[item][1].values())[option]

	return new_arr.astype(float), ids


def cluster_data(target_label, avg_cluster_size = 100):
	# n_clusters = int(len(ids) / avg_cluster_size)
	#
	# #labels = AffinityPropagation(random_state=5).fit_predict(array)
	# labels = MiniBatchKMeans(n_clusters=n_clusters, random_state=0).fit_predict(array)


	# #print("labels before", id_labels)
	#
	# pickle.dump(id_labels, open(filename, 'wb'))

	labels = pickle.load(open(filename, 'rb'))

	for i in range(len(labels)):
		if labels[i][0] == target_label:
			print(target_label)
			target_id_index = i

	target_label = labels[target_id_index][1]
	target_items = []
	for i in range(len(labels)):
		if labels[i][1] == target_label:
			target_items.append(labels[i][0])

	id_labels = []
	for i in range(len(labels)):
		id_labels.append((labels[i][0], labels[i][1]))

	#print("labels after", labels)
	return target_items


def get_cluster_for_ecom(ecom_id):
	return cluster_data(ecom_id)


if __name__ == "__main__":
	# data = read_data('')
	# print('data loaded', len(data))
	# processed, ids = process_data(data)
	# target_id_index = ids.index(target_id)

	ids = ["0028E87D58B130AC66DF3F96FCDAE178", "0029205189AF82D243E7BD2EFC83C2DC", "0029436C83D4DE12C022C4AC1A31F54F", "00294828AE84F474093535D1E7686D76",
"0029B111EF4ADAD18D5A8C7796E46D60",
"0029EE2F1D44AD47A4EA05FC05339CD1",
"002A75E863B9548D800D7402CAA465C7",
"002B0ADF86105F76540F6C0E7C894075",
"002B2143171FC4116B5B30E92C38A462",
"002B6A27F86AD22DBA49DE4A187000A8",
"002BC2FC60436CDE028FCADCE08E5043",
"002C0758845DF2F8348CC1CADC61A6AC",
"002C4DDC2E74F6358C289B592BC770C8",
"002C508FBF960F216B3FCB2905B39D82",
"002CB9379801900D2756C8852B334DFF",
"002CFF2F842FEF2AEB4299CAAB40091B",
"002D78C7721D8E051DA438463CBDD068",
"002DAA7756F4137A851703E105E81C94",
"002DEA0866E16E299EF915D99662F308",
"002E1B19EEE739265239E59808EBBBA8",
"002E8C0E17C6F09D2966DD8959729B82",
"002ED42E9302DC51FF29E498AE3C5BCB",
"002EE7EE60C4BACB76D8F133C4E49CAA",
"002EF50F3B815B12EA5D79EB3C72E5BC",
"002F0CB2CCBA5C3E7A88E7FDB389DEC4",
"002F3331E7F9C3834A845D6A928290D0",
"002F37454F413EEFAC0756A7DD12BE1A",
"002F856173BD3C2F8BA0A70FB635F798",
"002FCA1604B7760F7F245FF9149DB2CC"]

	# target_id = 'AACEC2ECD765D2E09B5EA323CB308FB4'
	for target_id in ids:
		print(target_id)
		result_items = cluster_data(target_id)
		print("result len ",  len(result_items))
