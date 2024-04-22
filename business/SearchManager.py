# include all search functions here
# accept search criteria, search by various criteria

class HotelSearchCriteria:
    """A class for setting up searching criteria for Hotels"""

    def __init__(self, hotel_name, hotel_location, hotel_rating):
        self.hotel_name = hotel_name
        self.hotel_location = hotel_location
        self.hotel_rating = hotel_rating

    @staticmethod
    def setup(location=None, rating=None, price_range=None, amenities=None, dates=None, room_type=None,
              star_category=None):
        """A function that accepts various criteria"""
        criteria = {
            "location": location,
            "rating": rating,
            "price_range": price_range,
            "amenities": amenities,
            "dates": dates,
            "room_type": room_type,
            "star_category": star_category,
        }
        return {k: v for k, v in criteria.items() if
                v is not None}  # a dictionary comprehension is used to create a new dictionary
        # This new dictionary only includes the key-value pairs from the criteria dictionary where the value is not None.

# criteria = HotelSearchCriteria.setup(location="Paris", rating=4, price_range=(100, 200))

