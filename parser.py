import requests

from constants import CFPLAND_URL


class Parser:
    def get_cfps(self):
        cfps = requests.get(CFPLAND_URL).json().get('items')

        data = []

        for item in cfps:
            cfp = {
                'title': item.get('name'),
                'description': item.get('description', ''),
                'link': item.get('cfp_url'),
                'category': item.get('category'),
                'event_start_date': item.get('event_start_date'),
                'cfp_end_date': item.get('cfp_due_date'),
                'location': item.get('location'),
                'perk_list': item.get('perks_list'),
            }

            data.append(cfp)

        return data
