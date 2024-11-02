import os
import sys
import inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
from app import search_items_API

def test_api_ebay():
    product = 'lenovo'
    site = 'eb'
    result = search_items_API(site, product)
    assert result is not None
