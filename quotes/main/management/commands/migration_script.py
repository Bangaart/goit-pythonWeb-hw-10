from datetime import datetime

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.db import transaction

from authors.models import Author
from main.management import connect  # noqa
from main.management.models_mongo import Authors, Quotes
from quote.models import Tag, Quote


class Command(BaseCommand):
    help = 'Migrate from MongoDB to PostgreSQL'

    def handle(self, *args, **options):

        with transaction.atomic():
            user = User.objects.get(id=1)
            authors_map = {}
            for item in Authors.objects:
                born_date = datetime.strptime(item.born_date, "%B %d, %Y")
                author, created = Author.objects.get_or_create(
                    full_name=item.fullname,
                    defaults={
                        "born_date": born_date,
                        "born_location": item.born_location,
                        "description": item.description,
                        "user": user}
                )
                authors_map[str(item.id)] = author

            for item in Quotes.objects:
                author = authors_map.get(str(item.author.id))
                quote, _ = Quote.objects.get_or_create(
                    quote=item.quote,
                    author=author,
                    user=user,
                )

                for tag in item.tags:
                    tags, created = Tag.objects.get_or_create(
                        name=tag,
                        user=user)
                    quote.tags.add(tags)
