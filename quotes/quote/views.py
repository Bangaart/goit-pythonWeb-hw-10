from datetime import datetime

import requests
from bs4 import BeautifulSoup
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import transaction
from django.db.models import F
from django.shortcuts import render, redirect
from django.views import generic

from authors.models import Author
from quote.forms import QuoteAddForm
from quote.models import Quote, Tag


# Create your views here.

@login_required
def add_quote(request):
    if request.method == 'POST':
        form = QuoteAddForm(request.POST)
        if form.is_valid():
            quote = form.save(commit=False)
            quote.user = request.user
            quote.save()
            form.save_m2m()
            return redirect(to='main:main')
        else:
            form = QuoteAddForm()
            return render(request, 'quote/add_quote.html', {'form': form})
    return render(request, 'quote/add_quote.html', {'form': QuoteAddForm()})


class QuoteListView(generic.ListView):
    paginate_by = 10
    model = Quote
    template_name = 'quote/quote_list.html'

    def get_queryset(self):
        return Quote.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['top_tags'] = Tag.objects.order_by("-counter")[:10]
        return context


class TagsQuoteListView(generic.ListView):
    template_name = 'quote/tags_quote.html'
    context_object_name = 'quote_list'
    model = Quote

    def get_queryset(self, **kwargs):
        return Quote.objects.filter(tags__id=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag'] = Tag.objects.get(pk=self.kwargs['pk'])
        return context

    def dispatch(self, request, *args, **kwargs):
        Tag.objects.filter(id__exact=self.kwargs['pk']).update(counter=F('counter') + 1)

        return super().dispatch(request, *args, **kwargs)


def get_scraping_data():
    url = 'https://quotes.toscrape.com'
    soup = BeautifulSoup(requests.get(url).content, 'html.parser')
    quotes = {}
    while True:
        page = soup.find_all('div', class_='quote')
        for item in page:
            author_link = item.find('a')['href']
            quote = item.find('span', class_='text').get_text()
            tags = [i.get_text() for i in item.find('div', class_='tags').find_all('a')]
            author_soup = BeautifulSoup(requests.get(url + author_link).content, 'html.parser')
            authors_details = author_soup.find('div', class_='author-details')
            full_name = authors_details.find('h3', class_='author-title').get_text()
            born_date = authors_details.select_one('p span.author-born-date').get_text()
            born_location = authors_details.select_one('p span.author-born-location').get_text()
            description = authors_details.find('div', class_="author-description").get_text()
            quotes[quote] = {'tags': tags,
                             'author': {'full_name': full_name, "born_date": born_date,
                                        "born_location": born_location,
                                        "description": description}}
            print(1)

        next_href = soup.select_one('li.next > a')
        if not next_href:
            break
        next_url = url + next_href['href']
        soup = BeautifulSoup(requests.get(next_url).content, 'html.parser')

    return quotes


def fill_database(request):
    with transaction.atomic():
        quotes_dict = get_scraping_data()
        user = User.objects.get(id=1)
        for key, value in quotes_dict.items():
            born_date = datetime.strptime(value['author']['born_date'], "%B %d, %Y")
            author, created = Author.objects.get_or_create(
                full_name=value['author']['full_name'],
                defaults={
                    "born_date": born_date,
                    "born_location": value['author']['born_location'],
                    "description": value['author']['description'],
                    "user": user}
            )

            quote, _ = Quote.objects.get_or_create(
                quote=key,
                author=author,
                user=user,
            )

            for tag in value['tags']:
                tags, created = Tag.objects.get_or_create(
                    name=tag,
                    user=user)
                quote.tags.add(tags)

    return redirect(to='quote:quote_list')
