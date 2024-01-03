import requests

from flask import redirect, render_template, session
from functools import wraps

def searchPrice(card):
    # Use API from yugiohprices.com to search for average prices of Yu-Gi-Oh! cards
    url = (
        f"http://yugiohprices.com/api/get_card_prices/{card}"
    )
    try:
        response = requests.get(url)
        card_data = response.json()
        # print(card_data)
        # if card_data["status"] == "fail" and card_data["message"] == "No card with this name was found.":
        #     return 0
        card_data_sets = len(card_data["data"])
        relevant_data = []
        for i in range(card_data_sets):
            if card_data["status"] == "fail" or card_data["data"][i]["price_data"]["status"] == "fail":
                continue
            card_info = {
                "set": card_data["data"][i]["name"],
                "print_tag": card_data["data"][i]["print_tag"],
                "rarity": card_data["data"][i]["rarity"],
                "avg_price": f'{card_data["data"][i]["price_data"]["data"]["prices"]["average"]:.2f}'
            }
            relevant_data.append(card_info)
        return relevant_data

    except (requests.RequestException, ValueError, KeyError, IndexError):
        return -1

def searchCard(card):

    url = (
        f"https://db.ygoprodeck.com/api/v7/cardinfo.php?name={card}"
    )

    try:
        response = requests.get(url)
        card_data = response.json()
        # print(card_data["data"][0]["card_images"][0]["image_url"])
        return {
            "img_url": card_data["data"][0]["card_images"][0]["image_url"],
            "name": card_data["data"][0]["name"],
            "type": card_data["data"][0]["type"],
            "race": card_data["data"][0]["race"]
        }

    except (requests.RequestException, ValueError, KeyError, IndexError):
        return -1

def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/0.12/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function
