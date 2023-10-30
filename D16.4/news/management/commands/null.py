from django.core.management.base import BaseCommand, CommandError
from news.models import News, Category


class Command(BaseCommand):
    help = 'Удаление новостей из данной категории'


    def add_arguments(self, parser):
        parser.add_argument('category', type=str)

    def handle(self, *args, **options):

        self.stdout.readable()
        self.stdout.write(
            'Do you really want to delete all news? yes/no')
        answer = input()

        if answer != 'yes':
            self.stdout.write(self.style.ERROR('Отменено'))
            return
        try:
            category = Category.objects.get(name=options['category'])
            News.objects.filter(category=category).delete()
            self.stdout.write(self.style.SUCCESS(
                f'Succesfully deleted all news from category {category.name}'))
        except News.DoesNotExist:
            self.stdout.write(self.style.ERROR('Could not find category'))