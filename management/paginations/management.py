from rest_framework import pagination
from rest_framework.response import Response
from collections import OrderedDict 

class ManagementUsersPagination(pagination.PageNumberPagination):
    page_size = 50
    page_query_param = 'page'
    page_size_query_param = 'per_page'
    max_page_size = 1000

    def get_paginated_response(self, data):
        next_page_count = None
        prev_page_count = None 
        if self.page.has_next():
            next_page_count = self.page.next_page_number()
        if self.page.has_previous():
            prev_page_count = self.page.previous_page_number()
        return Response(OrderedDict([
                ('prev', prev_page_count),
                ('current', self.page.number),
                ('next', next_page_count),
                ('page_size', self.page_size),
                ('total_pages', self.page.paginator.num_pages),
                ('total_records', self.page.paginator.count),
                ('results', data)
            ]))
            
class ManagementGroupsPagination(pagination.PageNumberPagination):
    page_size = 50
    page_query_param = 'page'
    page_size_query_param = 'per_page'
    max_page_size = 1000

    def get_paginated_response(self, data):
        next_page_count = None
        prev_page_count = None 
        if self.page.has_next():
            next_page_count = self.page.next_page_number()
        if self.page.has_previous():
            prev_page_count = self.page.previous_page_number()
        return Response(OrderedDict([
                ('prev', prev_page_count),
                ('current', self.page.number),
                ('next', next_page_count),
                ('page_size', self.page_size),
                ('total_pages', self.page.paginator.num_pages),
                ('total_records', self.page.paginator.count),
                ('results', data)
            ]))
