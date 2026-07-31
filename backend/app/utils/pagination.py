from math import ceil


def paginate_query(query, page=1, per_page=10):

    page = max(page, 1)
    per_page = max(min(per_page, 100), 1)

    total_items = query.count()

    items = query.offset(
        (page - 1) * per_page
    ).limit(
        per_page
    ).all()

    return {

        "items": items,

        "pagination": {

            "page": page,

            "per_page": per_page,

            "total_items": total_items,

            "total_pages": ceil(
                total_items / per_page
            ) if total_items else 0

        }

    }