from django import template
from django.template.loader import get_template

register = template.Library()

manifest_template = get_template('load-manifest.html')
worker_template = get_template('load-worker.html')


@register.inclusion_tag(manifest_template, takes_context=True)
def load_manifest(context):
    return context


@register.inclusion_tag(worker_template, takes_context=True)
def load_worker(context):
    return context
