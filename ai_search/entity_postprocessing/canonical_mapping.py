class CanonicalMapper:

    LISTING_TYPE_MAP = {
        "sell": ["sell", "buy", "purchase", "acquire", "sale"],
        "rent": ["rent", "rental", "renting","lease"]
    }

    PROPERTY_TYPE_MAP = {
        "Flat": ["flat", "flats", "apartment", "apartments"],
        "Independent House": [
            "house",
            "houses",
            "independent house",
            "independent houses",
            "villa",
            "villas"
        ],
        "Residential Plot": ["plot", "plots"],
        "Land": ["land"],
        "Duplex": ["duplex"],
        "office space": ["office space","officespace", "office", "office facility"],
    }

    @staticmethod
    def reverse_lookup(value, mapping_dict):
        """
        Convert a synonym into its canonical form.
        """
        if not value:
            return value

        value = value.lower()

        for canonical, synonyms in mapping_dict.items():
            if value in synonyms:
                return canonical

        return value  # fallback

    @classmethod
    def map_entities(cls, entities: dict):

        # make a shallow copy so we don't mutate original
        canonical = dict(entities)

        # -------- LISTING TYPE--------
        if canonical.get("listing_type"):
            canonical["listing_type"] = [
                cls.reverse_lookup(v, cls.LISTING_TYPE_MAP)
                for v in canonical["listing_type"]
            ]

        # -------- PROPERTY TYPE --------
        if canonical.get("property_type"):

            # ensure list
            values = canonical["property_type"]

            if not isinstance(values, list):
                values = [values]

            canonical["property_type"] = [
                cls.reverse_lookup(v, cls.PROPERTY_TYPE_MAP)
                for v in values
            ]

        # -------- CLEAN EMPTY ARRAYS --------
        for key, value in canonical.items():
            if not value:
                canonical[key] = None

        return canonical