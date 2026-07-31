from sqlalchemy import or_


def apply_search(query, model, search_term, fields):

    if not search_term:
        return query

    filters = []

    for field in fields:
        filters.append(
            getattr(model, field).ilike(
                f"%{search_term}%"
            )
        )

    return query.filter(
        or_(*filters)
    )