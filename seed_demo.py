from django.core.management.base import BaseCommand
from shop.models import Category, Product
class Command(BaseCommand):
    help='Create a small demo catalog (safe to run more than once).'
    def handle(self,*args,**kwargs):
        data={
          'Home & Living':[('Soft Form Ceramic Vase','A hand-finished silhouette for a quiet corner.',34),('Sunday Linen Throw','Easy texture for slow mornings.',68)],
          'Everyday Carry':[('Field Notes Tote','A sturdy canvas companion for the everyday.',29),('Pebble Key Tray','A home for all the little things.',22)],
          'Wellbeing':[('Evening Ritual Candle','A warm cedar and fig blend for winding down.',31),('Daily Reset Journal','A simple place to clear your mind.',24)]}
        for category_name, products in data.items():
            slug=category_name.lower().replace(' & ','-').replace(' ','-')
            category,_=Category.objects.get_or_create(name=category_name,defaults={'slug':slug})
            for name,description,price in products: Product.objects.get_or_create(name=name,defaults={'description':description,'category':category,'price':price,'stock':12})
        self.stdout.write(self.style.SUCCESS('Demo catalog is ready.'))
