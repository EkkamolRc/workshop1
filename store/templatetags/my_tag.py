
from django import template

from ..models import image_product

register = template.Library()
@register.filter
def getHtmlSliderImgs(idProduct):
    lstImg = image_product.objects.filter(product=idProduct)
    ls = []
    for i, img in enumerate(lstImg):
        ls.append({'index': i+1, 'value': img, 'length': len(lstImg)})
    return ls