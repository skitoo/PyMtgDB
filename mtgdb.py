# -*- coding: utf-8 -*-


import requests
import datetime
import urllib

RED = u'red'
GREEN = u'green'
BLUE = u'blue'
BLACK = u'black'
WHITE = u'white'

BASE_URL_SERVICE = 'http://api.mtgdb.info'


class Card(object):
    def __init__(self, data):
        self.id = data["id"]
        self.related_card_id = data["relatedCardId"]
        self.set_number = data["setNumber"]
        self.name = data["name"]
        self.search_name = data["searchName"]
        self.description = data["description"]
        self.flavor = data["flavor"]
        self.colors = data["colors"]
        self.mana_cost = data["manaCost"]
        self.converted_mana_cost = data["convertedManaCost"]
        self.card_set_name = data["cardSetName"]
        self.type = data["type"]
        self.sub_type = data["subType"]
        self.power = data["power"]
        self.toughness = data["toughness"]
        self.loyalty = data["loyalty"]
        self.rarity = data["rarity"]
        self.artist = data["artist"]
        self.card_set_id = data["cardSetId"]
        self.token = data["token"]
        self.promo = data["promo"]
        self.rulings = [Ruling(_) for _ in data["rulings"]]
        self.formats = [Format(_) for _ in data["formats"]]
        if data["releasedAt"] is not None:
            self.released_at = datetime.datetime.strptime(data["releasedAt"], '%Y-%m-%d')
        else:
            self.released_at = None

    def get_image_url(self):
        return '%s/content/card_images/%s.jpeg' % (BASE_URL_SERVICE, self.id)

    def get_hd_image_url(self):
        return '%s/content/hi_res_card_images/%s.jpg' % (BASE_URL_SERVICE, self.id)

    def __str__(self):
        return u'Card: %s' % self.name

    def __repr__(self):
        return str(self)


class Ruling(object):
    def __init__(self, data):
        self.released_at = datetime.datetime.strptime(data["releasedAt"], '%Y-%m-%d')
        self.rule = data['rule']

    def __str__(self):
        return 'Ruling: %s' % self.rule

    def __repr__(self):
        return str(self)


class Format(object):
    def __init__(self, data):
        self.name = data['name']
        self.legality = data['legality']

    def __str__(self):
        return 'Format: %s - %s' % (self.name, self.legality)

    def __repr__(self):
        return str(self)


class CardSet(object):
    def __init__(self, data):
        self.id = data["id"]
        self.name = data["name"]
        self.type = data["type"]
        self.block = data["block"]
        self.description = data["description"]
        self.common_count = data["common"]
        self.uncommon_count = data["uncommon"]
        self.rare_count = data["rare"]
        self.mythic_rare_count = data["mythicRare"]
        self.basic_land_count = data["basicLand"]
        self.total_cards = data["total"]
        if data["releasedAt"] is not None:
            self.release_date = datetime.datetime.strptime(data["releasedAt"], '%Y-%m-%d')
        else:
            self.release_date = None
        self.card_ids = data["cardIds"]

    @property
    def cards(self):
        data = requests.get('%s/sets/%s/cards/' % (BASE_URL_SERVICE, self.id)).json()
        return [Card(_) for _ in data] if data else None

    def get_card(self, number):
        data = requests.get('%s/sets/%s/cards/%s' % (BASE_URL_SERVICE, self.id, number)).json()
        return Card(data) if data else None

    def get_cards_range(self, start, end):
        data = requests.get('%s/sets/%s/cards/?start=%s&end=%s' % (BASE_URL_SERVICE, self.id, start, end)).json()
        return [Card(_) for _ in data] if data else None

    def get_random_card(self):
        data = requests.get('%s/sets/%s/cards/random' % (BASE_URL_SERVICE, self.id)).json()
        return Card(data) if data else None

    def __str__(self):
        return 'CardSet: %s' % self.name

    def __repr__(self):
        return str(self)


class MtgDB(object):
    def get_card(self, id):
        data = requests.get('%s/cards/%s' % (BASE_URL_SERVICE, id)).json()
        return Card(data) if data else None

    def get_card_by_name(self, name):
        data = requests.get('%s/cards/%s' % (BASE_URL_SERVICE, urllib.quote(name))).json()
        return [Card(_) for _ in data] if data else None

    def get_cards(self, ids=[]):
        data = requests.get('%s/cards/%s' % (BASE_URL_SERVICE, ','.join(map(lambda id: str(id), ids)))).json()
        return [Card(_) for _ in data] if data else None

    def get_sets(self, ids=[]):
        data = requests.get('%s/sets/%s' % (BASE_URL_SERVICE, ','.join(ids))).json()
        return [CardSet(_) for _ in data] if data else None

    def get_set(self, id):
        data = requests.get('%s/sets/%s' % (BASE_URL_SERVICE, id)).json()
        return CardSet(data) if data else None

    def get_card_types(self):
        return requests.get('%s/cards/types' % (BASE_URL_SERVICE)).json()

    def get_card_subtypes(self):
        return requests.get('%s/cards/subtypes' % (BASE_URL_SERVICE)).json()

    def get_card_rarity(self):
        return requests.get('%s/cards/rarity' % (BASE_URL_SERVICE)).json()

    def search(self, text, start=0, limit=0, is_complex=False):
        pass

    def filter_cards(self, **kwargs):
        data = requests.get('%s/cards?%s' % (BASE_URL_SERVICE, urllib.urlencode(kwargs))).json()
        return [Card(_) for _ in data] if data else None
