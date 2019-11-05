from django.shortcuts import render
from hn_articles.models import Entries

# Create your views here.

def hn_search(request):
	text = request.GET.get('text')
	entries = Entries.objects.filter(title__contains=text)
	context = {
		"entries": entries,
	}

	return render(request, 'hn_search.html', context)
