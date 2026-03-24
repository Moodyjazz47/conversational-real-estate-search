class QueryBuilder:

    BASE_TABLE = "propertyowner"

    @staticmethod
    def _normalize_value(value):
        """
        Normalize entity values coming from JSON.
        Converts single-item lists to scalar values.
        """
        if isinstance(value, list):
            if len(value) == 1:
                return value[0]
        return value

    @staticmethod
    def build_where_clause(entities: dict):
        conditions = []
        parameters = []

        # -------- LISTING TYPE --------
        listing_type= entities.get("listing_type")

        if listing_type:
            if isinstance(listing_type, list):
                conditions.append(
                    "(property_attr -> 'metadata' ->> 'listingType') = ANY(%s)"
                )
                parameters.append(listing_type)
            else:
                conditions.append(
                    "(property_attr -> 'metadata' ->> 'listingType') = %s"
                )
                parameters.append(listing_type)

        # -------- PROPERTY TYPE --------
        property_type = entities.get("property_type")

        if property_type:
            if isinstance(property_type, list):
                conditions.append(
                    "(property_attr -> 'metadata' ->> 'subPropertyTypeName') ILIKE ANY(%s)"
                )
                parameters.append(property_type)
            else:
                conditions.append(
                    "(property_attr -> 'metadata' ->> 'subPropertyTypeName') ILIKE %s"
                )
                parameters.append(property_type)

        # -------- LOCATION --------
        location = entities.get("location")

        if location:
            conditions.append(
                "(property_attr -> 'location' ->> 'address') ILIKE %s"
            )
            parameters.append(f"%{location}%")

        # -------- BEDROOMS --------
        bedrooms = entities.get("property_attributes")

        if bedrooms is not None:
            conditions.append(
                "CAST(property_attr -> 'attributes' ->> 'numBedrooms' AS INTEGER) = %s"
            )
            parameters.append(bedrooms)

        # -------- BUILD WHERE --------
        if conditions:
            where_clause = " WHERE " + " AND ".join(conditions)
        else:
            where_clause = ""

        return where_clause, parameters

    @classmethod
    def build_full_query(cls, entities: dict):

        where_clause, parameters = cls.build_where_clause(entities)

        query = f"""
        SELECT *
        FROM {cls.BASE_TABLE}
        {where_clause}
        """

        return query.strip(), parameters