import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True
    dependencies = [migrations.swappable_dependency(settings.AUTH_USER_MODEL)]
    operations = [
        migrations.CreateModel(name='Category', fields=[('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')), ('name', models.CharField(max_length=80, unique=True)), ('slug', models.SlugField(unique=True))]),
        migrations.CreateModel(name='Order', fields=[('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')), ('status', models.CharField(choices=[('pending','Pending'),('processing','Processing'),('shipped','Shipped'),('delivered','Delivered'),('cancelled','Cancelled')], default='pending', max_length=20)), ('total', models.DecimalField(decimal_places=2, max_digits=10)), ('created_at', models.DateTimeField(auto_now_add=True)), ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='orders', to=settings.AUTH_USER_MODEL))]),
        migrations.CreateModel(name='Product', fields=[('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')), ('name', models.CharField(max_length=160)), ('description', models.TextField()), ('price', models.DecimalField(decimal_places=2, max_digits=10)), ('stock', models.PositiveIntegerField(default=0)), ('image_url', models.URLField(blank=True)), ('is_active', models.BooleanField(default=True)), ('created_at', models.DateTimeField(auto_now_add=True)), ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='products', to='shop.category'))]),
        migrations.CreateModel(name='OrderItem', fields=[('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')), ('product_name', models.CharField(max_length=160)), ('unit_price', models.DecimalField(decimal_places=2, max_digits=10)), ('quantity', models.PositiveIntegerField()), ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='shop.order')), ('product', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='shop.product'))]),
        migrations.CreateModel(name='CartItem', fields=[('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')), ('quantity', models.PositiveIntegerField(default=1)), ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.product')), ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cart_items', to=settings.AUTH_USER_MODEL))], options={'constraints':[models.UniqueConstraint(fields=('user','product'), name='unique_cart_product')]}),
    ]
