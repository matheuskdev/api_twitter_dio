from typing import Any, Dict, List

import tweepy

from src.connection import trends_collection
from src.constants import BRAZIL_WOE_ID
from src.secrets import ACCESS_TOKEN, ACCESS_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_SECRET


def _get_trends(woe_id: int, api: tweepy.API) -> List[Dict[str, Any]]:
    """Obtém tópicos em tendência da API do Twitter.

    Args:
        woe_id (int): Identificador da localização.

    Returns:
        List[Dict[str, Any]]: Lista de tendências.
    """
    trends = api.trends_place(woe_id)

    return trends[0]["trends"]


def get_trends() -> List[Dict[str, Any]]:
    """Obtém tópicos em tendência armazenados no MongoDB.

    Args:
        woe_id (int): Identificador da localização.

    Returns:
        List[Dict[str, Any]]: Lista de tendências.
    """
    trends = trends_collection.find({})
    return list(trends)


def save_trends() -> None:
    """Obtém tópicos em tendência e os salva no MongoDB."""
    auth = tweepy.OAuthHandler(consumer_key=CONSUMER_KEY, consumer_secret=CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

    api = tweepy.API(auth)

    trends = _get_trends(woe_id=BRAZIL_WOE_ID, api=api)
    trends_collection.insert_many(trends)
