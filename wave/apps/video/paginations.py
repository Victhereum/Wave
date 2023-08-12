from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class CustomPagination(PageNumberPagination):
    page_size = 10  # Set the desired page size
    page_size_query_param = "page_size"  # Optional: Allow the client to override the page size
    max_page_size = 1

    def get_paginated_response(self, data):
        count = self.page.paginator.count
        next_link = self.get_next_link()
        previous_link = self.get_previous_link()
        total_pages = self.page.paginator.num_pages
        page_number = self.page.number

        return Response(
            {
                "count": count,
                "next": next_link,
                "previous": previous_link,
                "total_pages": total_pages,
                "page": page_number,
                "results": data,
            }
        )
