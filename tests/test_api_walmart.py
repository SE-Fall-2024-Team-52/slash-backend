# -*- coding: utf-8 -*-
# @Date    : 2023-10-09 13:59:02
# @Author  : Sathiya Narayanan Venkatesan (sathiyavenkat06@gmail.com)

import os
import sys
import inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
from ..app import search_items_API

def test_api_bestbuy():
    product = 'laptop'
    site = 'wm'
    result = search_items_API(site, product)
    assert result is not None