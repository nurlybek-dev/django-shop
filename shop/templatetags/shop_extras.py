from django import template

register = template.Library()

@register.inclusion_tag('shop/rating_with_comment.html')
def show_avg_rating(product):
    url = product.get_absolute_url() + '#reviews'
    count = product.reviews.count()
    fill = product.get_avg_rating()
    empty = 5 - fill
    return {
        'url': url,
        'count': count,
        'fill': range(fill),
        'empty': range(empty)
    }


@register.inclusion_tag('shop/rating.html')
def show_rating(review):
    fill = review.rating
    empty = 5 - fill
    return {
        'fill': range(fill),
        'empty': range(empty)
    }
