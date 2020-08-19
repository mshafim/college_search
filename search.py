import requests, json, time, multiprocessing
start_time = time.time()

# main api handler
def act_request():
	# creates data storage
	manager = multiprocessing.Manager()
	data = manager.list()
	cleaned_data = []

	# initial request to obtain total pages
	query = requests.get(f"https://api.data.gov/ed/collegescorecard/v1/schools?_fields=id,school.name,latest.admissions.act_scores.midpoint.cumulative,latest.admissions.act_scores.25th_percentile.cumulative,latest.admissions.act_scores.75th_percentile.cumulative&page=0&per_page=100&api_key={api_key}").json()

	# calculates all pages
	total_pages = query["metadata"]["total"] / 100
	total_pages_list = [(page, data) for page in range(int(total_pages + 1))]

	# obtains all data	
	process = multiprocessing.Pool(3)
	process_request = process.starmap(act_page_request, total_pages_list)

	for page in data:
		for school in page:
			if school["latest.admissions.act_scores.midpoint.cumulative"] != None:
				cleaned_data.append(school)
				school["category"] = None
	return cleaned_data

# page specific api call
def act_page_request(page, data):
	query = requests.get(f"https://api.data.gov/ed/collegescorecard/v1/schools?_fields=id,school.name,latest.admissions.act_scores.midpoint.cumulative,latest.admissions.act_scores.25th_percentile.cumulative,latest.admissions.act_scores.75th_percentile.cumulative&page={page}&per_page=100&api_key={api_key}").json()
	for school in query["results"]:
		print(school)
	data.append(query["results"])
	print("Page"+ str(page))

# main code

# api keys
api_key = ""

# main data storage
with open('act_data.json', 'w') as file:
	json.dump(act_request().copy(), file)

#process time
end_time = time.time()
print(str(end_time - start_time) + "seconds")
