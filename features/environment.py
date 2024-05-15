from splinter.browser import Browser
from django.core.management.base import BaseCommand
from django.conf import settings
import os


def before_all(context):
    context.browser = Browser('chrome', headless=True)


def after_all(context):
    context.browser.quit()
    context.browser = None
