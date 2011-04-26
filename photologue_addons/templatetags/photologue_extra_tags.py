import re
import logging

from django import template
from django.conf import settings
from django.db import models

Photo = models.get_model('photologue', 'photo')

register = template.Library()

@register.tag
def get_public_photos(parser, token):
    """
    Gets any number of photos ordered by published date and specified by a tag
    and places them in a varable.

    Syntax::

    {% get_public_photos [count] (tagged [tag]) as [var_name] %}

    Example usage::

    (4) {% get_public_photos 10 as rabbit_photos %}
    (7) {% get_public_photos 10 tagged not holes as rabbit_photos %}
    (8) {% get_public_photos 10 tagged rabbits not holes as rabbit_photos %}
    (7) {% get_public_photos 10 tagged all rabbits,holes as rabbit_hole_photos %}
    (9) {% get_public_photos 10 tagged all rabbits,holes not carrots as rabbit_hole_photos %}
    
    """
    args = token.split_contents()
    argc = len(args)

    try:
        assert argc in (4,6,7,9)
    except AssertionError:
        raise template.TemplateSyntaxError('Invalid get_public_photos syntax.')
    # determine what parameters to use
    count = tags = var_name = switch = ex_tags = None
    if argc == 4: t, count, a, var_name = args
    if argc == 6: t, count, n, ex_tags, a, var_name = args
    elif argc == 7: t, count, g, switch, tags, a, var_name = args
    elif argc == 9: t, count, a, g, tags, n, ex_tags, a, var_name = args
    return GetPhotosNode(count=count, switch=switch, tags=tags, ex_tags=ex_tags, var_name=var_name)

class GetPhotosNode(template.Node):
    def __init__(self, count, tags, switch, ex_tags, var_name):
        self.count = int(count)
        if tags:
            self.tags = tags.split(',')
        else:
            self.tags = None
        self.var_name = var_name
        self.switch= switch
        if ex_tags:
            self.ex_tags = ex_tags.split(',')
        else:
            self.ex_tags = None

    def render(self, context):
        logging.debug("get_public_photos switch are %s" % (self.switch))
        if self.tags:
            if self.switch == "not":
                photos = Photo.objects.filter(is_public=True).exclude(tags__name__in=self.tags)[:self.count]
            elif self.switch == "all":
                photos = Photo.objects.filter(is_public=True)
                for t in self.tags:
                    photos = photos.filter(tags__name__in=[t])
                photos = photos[:self.count]
            else:
                photos = Photo.objects.filter(is_public=True, tags__name__in=self.tags)

            if self.ex_tags:
                photos = photos.exclude(tags__name__in=self.ex_tags)

        else:
            photos = Photo.objects.filter(is_public=True)[:self.count]
        context[self.var_name] = photos
        return ''

@register.inclusion_tag('photologue/tags/next_in_gallery.html')
def next_in_gallery(photo, gallery):
    return {'photo': photo.get_next_in_gallery(gallery)}

@register.inclusion_tag('photologue/tags/prev_in_gallery.html')
def previous_in_gallery(photo, gallery):
    return {'photo': photo.get_previous_in_gallery(gallery)}

