import json, time
import numpy as np
import matplotlib.pyplot as plt

with open('act_data.json', 'r') as file:
	act_data = json.load(file)

# cumulative_score = float(int(input("Enter Cumulative Score: ")))
# while cumulative_score < 1.0 or cumulative_score > 36.0:
# 	cumulative_score = float(int(input("Please Enter Valid Cumulative Score: ")))

scores = [x for x in range(1, 37)]
no_figure = 1

plt.ion()

for cumulative_score in scores:
	# school categories
	safety = []
	target = []
	realistic_reach = []
	out_of_reach = []

	start_time = time.time()
	# searches schools
	for school in act_data:
		# safety
		if cumulative_score >= school["latest.admissions.act_scores.75th_percentile.cumulative"]:
			safety.append(school)
			school["category"] = "safety"
		# target
		if cumulative_score <= school["latest.admissions.act_scores.75th_percentile.cumulative"] and cumulative_score >= school["latest.admissions.act_scores.midpoint.cumulative"]:
			target.append(school)
			school["category"] = "target"
		# realistic reach
		if cumulative_score >= school["latest.admissions.act_scores.25th_percentile.cumulative"] and cumulative_score <= school["latest.admissions.act_scores.midpoint.cumulative"]:
			realistic_reach.append(school)
			school["category"] = "realistic reach"
		# out of reach
		if cumulative_score <= school["latest.admissions.act_scores.25th_percentile.cumulative"]:
			out_of_reach.append(school)
			school["category"] = "out of reach"

	# graphs data
	plt.figure(no_figure)
	label = ["out_of_reach", "realistic_reach", "target", "safety"]
	index = np.arange(len(label))
	no_school= [len(out_of_reach), len(realistic_reach), len(target), len(safety)]
	plt.ylim(0, 1300)
	plt.bar(index, no_school)
	plt.xlabel("School Type", fontsize=10)
	plt.ylabel("# of Schools", fontsize=10)
	plt.xticks(index, label, fontsize=10, rotation=30)
	plt.title(f"Cumulative ACT Score: {cumulative_score}")
	plt.pause(.1)
	no_figure += 1

	# print(len(safety))
	# print(len(target))
	# print(len(realistic_reach))
	# print(len(out_of_reach))

plt.show()

# process time

