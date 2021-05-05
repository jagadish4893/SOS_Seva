from django.core.management.base import BaseCommand, CommandError
from informer.tweet_scraper import final_data

class Command(BaseCommand):
    help = "Insert Upazila office reports from a CSV file. " \
           "CSV file name(s) should be passed. " \
           "If no optional argument (e.g.: --acland) is passed, " \
           "this command will insert UNO office reports."

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


    def handle(self, *args, **options):
        data = final_data()
        print("My custom command is Akshit")
        print(data)