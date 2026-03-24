import re
from typing import Optional


class EntityNormalizer:

    PRICE_MULTIPLIERS = {
        "l": 100000,
        "lac": 100000,
        "lacs": 100000,
        "lakh": 100000,
        "lakhs": 100000,
        "cr": 10000000,
        "crore": 10000000,
        "crores": 10000000,
        "k": 1000
    }

    # ----------------------------
    # Helper Methods
    # ----------------------------

    @staticmethod
    def extract_number(text: str) -> Optional[int]:
        if not text:
            return None

        match = re.search(r"\d+(\.\d+)?", str(text))
        if match:
            return int(float(match.group()))
        return None

    # @classmethod
    # def normalize_price(cls, price_text) -> Optional[int]:
    #     if price_text is None:
    #         return None
    #
    #     text = str(price_text).lower().strip()
    #
    #     number_match = re.search(r"\d+(\.\d+)?", text)
    #     if not number_match:
    #         return None
    #
    #     number = float(number_match.group())
    #     multiplier = 1
    #
    #     for unit, factor in cls.PRICE_MULTIPLIERS.items():
    #         if unit in text:
    #             multiplier = factor
    #             break
    #
    #     return int(number * multiplier)

    @staticmethod
    def normalize_property_attributes(value) -> Optional[int]:
        if value is None:
            return None

        return EntityNormalizer.extract_number(str(value))

    # @staticmethod
    # def normalize_area(value) -> Optional[int]:
    #     if value is None:
    #         return None
    #
    #     return EntityNormalizer.extract_number(str(value))

    @staticmethod
    def normalize_list_of_strings(values):
        if not values:
            return []

        return [str(v).lower().strip() for v in values]

    # ----------------------------
    # Main API
    # ----------------------------

    @classmethod
    def normalize_entities(cls, entities):
        """
        Strict normalization only.
        No semantic mapping.
        """

        # Lowercase listing_type
        entities["listing_type"]= cls.normalize_list_of_strings(
            entities["listing_type"]
        )

        # Lowercase property_type
        entities["property_type"] = cls.normalize_list_of_strings(
            entities["property_type"]
        )

        # Lowercase location
        entities["location"] = cls.normalize_list_of_strings(
            entities["location"]
        )

        # Numeric conversions
        entities["property_attributes"]= cls.normalize_property_attributes(
            entities["property_attributes"]
        )

        # entities.property_attributes.price = cls.normalize_price(
        #     entities.property_attributes.price
        # )

        # entities.property_attributes.area_size = cls.normalize_area(
        #     entities.property_attributes.area_size
        # )

        return entities