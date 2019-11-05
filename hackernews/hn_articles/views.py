from django.shortcuts import render
from hn_articles.models import Entries
import http.client
from aylienapiclient import textapi
import json
from environs import Env

# Create your views here.

def hn_articles(request):
	conn = http.client.HTTPSConnection("hacker-news.firebaseio.com")
	payload = "{}"
	conn.request("GET", "/v0/topstories.json?print=pretty", payload)
	res = conn.getresponse()
	data = res.read()
	data_decoded = data.decode("utf-8")
	data_top_ten = json.loads(data_decoded)[:10]
	env = Env()
	env.read_env()
	api_id = env("API_ID")
	api_key = env("API_KEY")
	client = textapi.Client(api_id, api_key)

	for dat_id in data_top_ten:
		entries = Entries.objects.all().filter(json_id=dat_id)
		if not entries:
			conn.request("GET", "/v0/item/" + str(dat_id) + ".json?print=pretty", payload)
			result = conn.getresponse()
			result_data = result.read()
			json_result_data = json.loads(result_data.decode("utf-8"))
			sentiment = client.Sentiment({'text': json_result_data["title"]})
			entry = Entries(
				json_id = json_result_data["id"],
		        username = json_result_data["by"],
				title = json_result_data["title"],
			    url = json_result_data["url"] if "url" in json_result_data else "",
			    score = json_result_data["score"],
			    sentiment = sentiment["polarity"]
		    )
			entry.save()

	entries = Entries.objects.all().filter(json_id__in=data_top_ten)
	context = {
		"entries": entries,
	}

	return render(request, 'hn_articles.html', context)
