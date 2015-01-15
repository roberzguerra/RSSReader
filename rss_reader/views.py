# -*- coding:utf-8 -*-
from django.views.generic import TemplateView
from django.core.paginator import Paginator
from xml.dom import minidom
from datetime import datetime
import urllib


# Create your views here.
class HomePageView(TemplateView):
    """

    """
    template_name = "rss_reader/homepage.html";
    url_rss = 'http://g1.globo.com/dynamo/economia/rss2.xml'

    def get(self, request, page_number=1, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        rss_reader = RssReader(self.url_rss)
        rss_reader.reader()
        page_number = int(page_number)
        paginator = Paginator(rss_reader.get_itens_for_paginator(page_number - 1), 1)
        if page_number > paginator.count:
            page_number = paginator.count
        context['page'] = paginator.page(page_number)
        return self.render_to_response(context)

class RssReader(object):
    url = ''
    page_number = ''
    xml = None

    def __init__(self, url=''):
        if url:
            self.url = url
            self.reader()

    def reader(self):
        page = urllib.urlopen(self.url)
        self.xml = minidom.parse(page)
        page.close()

    def get_itens(self):
        return self.xml.getElementsByTagName('item')

    def get_itens_for_paginator(self, item_number):
        """
        Retorna uma lista de objetos para paginacao,
        somente a pagina selecionada eh retornada com o objeto Item preenchido
        """
        itens = self.get_itens()
        if item_number < 0:
            item_number = 1
        elif item_number >= len(itens):
            item_number = len(itens) - 1

        xml_item = itens[item_number]
        title = xml_item.getElementsByTagName('title')
        description = xml_item.getElementsByTagName('description')
        if title or description:
            link = xml_item.getElementsByTagName('link')
            category = xml_item.getElementsByTagName('category')
            pub_date = xml_item.getElementsByTagName('pubDate')

            item = Item()
            if title:
                item.title = title[0].childNodes[0].nodeValue
            if description:
                item.description = description[0].childNodes[0].nodeValue
            if link:
                item.link = link[0].childNodes[0].nodeValue
            if pub_date:
                pub_date = pub_date[0].childNodes[0].nodeValue
                datetime.strptime(pub_date[0:25], "%a, %d %b %Y %H:%M:%S")
            itens[item_number] = item

        return itens


class Item(object):
    """
    Modelo de Item:
    <title>Titulo da Noticia</title>
    <link>http://.....html</link>
    <description>DESCRIÇÃO DA NOTICIA </description>
    <category>Categoria</category>
    <pubDate>Wed, 14 Jan 2015 13:21:00 -0200</pubDate> # Data da publicacao em ingles
    """
    def __init__(self):
        self.title = u""
        self.link = ''
        self.description = u""
        self.category = u""
        self.pub_date = datetime.now()
        self.item_number = 0