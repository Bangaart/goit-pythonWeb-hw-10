from django.contrib.auth.decorators import login_required
from django.db.models import F
from django.shortcuts import render, redirect
from django.views import generic

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
    context_object_name = 'quote_list'

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
