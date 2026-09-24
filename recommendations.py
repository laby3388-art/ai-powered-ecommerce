from collections import Counter
from django.db.models import Count
from .models import Product, OrderItem

def recommendations(user, limit=4):
    bought = list(OrderItem.objects.filter(order__user=user).values_list('product_id', flat=True)) if user.is_authenticated else []
    bought_products = list(Product.objects.filter(id__in=bought).select_related('category'))
    liked_categories = Counter(p.category_id for p in bought_products)
    popular_ids = list(OrderItem.objects.values('product_id').annotate(sales=Count('id')).order_by('-sales').values_list('product_id', flat=True)[:12])
    pool = Product.objects.filter(is_active=True, stock__gt=0).select_related('category').exclude(id__in=bought)
    ranked=[]
    for product in pool:
        same_category = liked_categories.get(product.category_id, 0)
        popularity = popular_ids.index(product.id) if product.id in popular_ids else 99
        if same_category:
            reason=f"Based on your interest in {product.category.name}."
            score=(same_category*10) + max(0, 12-popularity)
        else:
            reason="Popular with other shoppers." if popularity < 99 else "A fresh pick from our catalog."
            score=max(0, 12-popularity)
        ranked.append((score, product, reason))
    ranked.sort(key=lambda row: (-row[0], row[1].name))
    return [{'product':p, 'reason':r} for _,p,r in ranked[:limit]]
