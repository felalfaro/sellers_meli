from pandas import DataFrame
from constants import countries
from typing import Dict
import requests

URL = 'https://api.mercadolibre.com'


def add_country(cat: Dict, country: str):
    cat['country'] = country
    return cat


def get_payment_type() -> DataFrame:
    """ Get payment methods.

    Returns:
        DataFrame: Payments methods by country.
    """
    data = []
    for country in countries:
        cats = requests.get(
            f"{URL}/sites/{country['id']}/payment_methods").json()
        cats = map(lambda x: add_country(x, country['id']), cats)
        data.extend(cats)

    return DataFrame.from_records(data)


def get_categories() -> DataFrame:
    """Get categories in MeLi.

    Returns:
        DataFrame: Categories by country.
    """
    data = []
    for country in countries:
        cats = requests.get(f"{URL}/sites/{country['id']}/categories").json()
        cats = map(lambda x: add_country(x, country['id']), cats)
        data.extend(cats)

    return DataFrame.from_records(data)


def map_result(result: Dict) -> Dict:
    """Map Json obtained from search result.

    Args:
        result Dict: Dict with data of items. 

    Returns:
        Dict: Data of item mapped. 
    """

    attributes = result['attributes']

    brand_filter = list(filter(lambda x: x['id'] == 'BRAND', attributes))
    model_filter = list(filter(lambda x: x['id'] == 'MODEL', attributes))
    length_filter = list(
        filter(lambda x: x['id'] == 'PACKAGE_LENGTH', attributes))
    weight_filter = list(
        filter(lambda x: x['id'] == 'PACKAGE_WEIGHT', attributes))

    return {'id': result['id'],
            'title': result['title'],
            'condition': result['condition'],
            'listing_type_id': result['listing_type_id'],
            'permalink': result['permalink'],
            'site_id': result['site_id'],
            'category_id': result['category_id'],
            'domain_id': result['domain_id'],
            'thumbnail': result['thumbnail'],
            'currency_id': result['currency_id'],
            'price': result['price'],
            'original_price': result['original_price'],
            'sale_price': result['sale_price'],
            'sold_quantity': result['sold_quantity'],
            'available_quantity': result['available_quantity'],
            'official_store_id': result['official_store_id'],
            'use_thumbnail_id': result['use_thumbnail_id'],
            'accepts_mercadopago': result['accepts_mercadopago'],
            'tags': result['tags'],
            'shipping_store_pick_up': result['shipping']['store_pick_up'],
            'shipping_free_shipping': result['shipping']['free_shipping'],
            'shipping_logistic_type': result['shipping']['logistic_type'],
            'shipping_mode': result['shipping']['mode'],
            'shipping_tags': result['shipping']['tags'],
            'shipping_benefits': result['shipping']['benefits'],
            'shipping_promise': result['shipping']['promise'],
            'seller_id': result['seller']['id'],
            'seller_nickname': result['seller']['nickname'],
            'seller_car_dealer': result['seller']['car_dealer'],
            'seller_real_estate_agency': result['seller']['real_estate_agency'],
            'seller_registration_date': result['seller']['registration_date'],
            'seller_car_dealer_logo': result['seller']['car_dealer_logo'],
            'seller_permalink': result['seller']['permalink'],
            'seller_level_id': result['seller']['seller_reputation']['level_id'],
            'seller_power_seller_status': result['seller']['seller_reputation']['power_seller_status'],
            'seller_transactions_canceled': result['seller']['seller_reputation']['transactions']['canceled'],
            'seller_transactions_completed': result['seller']['seller_reputation']['transactions']['completed'],
            'seller_rating_negative': result['seller']['seller_reputation']['transactions']['ratings']['negative'],
            'seller_rating_neutral': result['seller']['seller_reputation']['transactions']['ratings']['neutral'],
            'seller_rating_positive': result['seller']['seller_reputation']['transactions']['ratings']['positive'],
            'seller_transactions_total': result['seller']['seller_reputation']['transactions']['total'],

            'address_state_id': result['address']['state_id'],
            'address_state_name': result['address']['state_name'],
            'address_city_id': result['address']['city_id'],
            'address_city_name': result['address']['city_name'],
            'brand_id': brand_filter[0]['value_id'] if brand_filter else None,
            'brand_name': brand_filter[0]['value_name'] if brand_filter else None,
            'model_id': model_filter[0]['value_id'] if model_filter else None,
            'model_name': model_filter[0]['value_name'] if model_filter else None,
            'package_length_unit': length_filter[0]['value_id'] if length_filter else None,
            'package_length_number': length_filter[0]['value_name'] if length_filter else None,
            'package_weight_number': weight_filter[0]['value_name'] if weight_filter else None,
            'package_weight_number': weight_filter[0]['value_name'] if weight_filter else None,
            }


def get_items_by_cat(category: str, country: str) -> Dict:
    """Get item by given category and country.

    Args:
        category (str): Id of category.
        country (str): Id of country.

    Returns:
        Dict: Data of items requested.
    """
    data = []
    count_per_request = 50
    offset = 0
    max_items = 1000
    cant = int(max_items/count_per_request)
    for _ in range(cant):
        url = f'{URL}/sites/{country}/search?category={category}&offset={offset}'
        resp = requests.get(url=url).json()
        result = map(map_result, resp['results'])
        data.extend(result)
        offset = offset + count_per_request
        if offset > resp['paging']['total']:
            break
    return data
