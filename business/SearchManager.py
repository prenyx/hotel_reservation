# include all search functions here
# accept search criteria, search by various criteria

import os
from sqlalchemy import select, func
from business.BaseManager import BaseManager
from data_models.models import *


class HotelSearchCriteria:
    """A class for setting up searching criteria for Hotels"""

    def __init__(self, hotel_name=None, hotel_location=None, hotel_rating=None, price_range=None, amenities=None,
                 dates=None, room_types=None, star_category=None):
        self.criteria = {k: v for k, v in
                         {"hotel_name": hotel_name,
                          "hotel_location": hotel_location,
                          "hotel_rating": hotel_rating,
                          "price_range": price_range,
                          "amenities": amenities,
                          "dates": dates,
                          "room_types": room_types,
                          "star_category": star_category}.items() if
                         v is not None}

    def get_criteria(self):
        return self.criteria


if __name__ == "__main__":
    search_criteria1 = HotelSearchCriteria(hotel_name="Paradise Inn",
                                           hotel_location="New York",
                                           hotel_rating=4,
                                           price_range="$100-$200",
                                           amenities="Free WiFi",
                                           dates="2023-01-01 to 2023-01-31",
                                           room_types=["Deluxe", "Suite", "Standard"],
                                           star_category=5)

    print(search_criteria1.get_criteria())

    # search_criteria2 = HotelSearchCriteria(hotel_location="New York",
    #                                       hotel_rating=4,
    #                                       price_range="$100-$200",
    #                                       amenities="Free WiFi",
    #                                       dates="2023-01-01 to 2023-01-31",
    #                                       room_types=["Deluxe", "Suite", "Standard"],
    #                                       star_category=5)
    # print(search_criteria2.get_criteria())
