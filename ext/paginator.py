import discord
from collections import OrderedDict
import asyncio

class PaginatorSession:
    '''Class that paginates embeds using discord reactions'''
    
    def __init__(self, ctx, timeout=60, pages=[], 
