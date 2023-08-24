from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class CustomPagination(PageNumberPagination):
    page_size = 10  # Set the desired page size
    page_size_query_param = "page_size"  # Optional: Allow the client to override the page size
    max_page_size = 1

    def get_paginated_response(self, data):
        """
        Generates a paginated response containing the given data.

        Parameters:
            - data: The data to be included in the paginated response.

        Returns:
            - A Response object containing the paginated response with the following properties:
                - count: The total count of items in the paginated response.
                - next: The URL for the next page of results, or null if there is no next page.
                - previous: The URL for the previous page of results, or null if there is no previous page.
                - total_pages: The total number of pages in the paginated response.
                - page: The current page number.
                - results: The data included in the current page of the paginated response.
        """
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
