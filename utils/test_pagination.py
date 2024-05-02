from unittest import TestCase
from utils.pagination import make_pagination_range

class PaginationTest(TestCase):

    def test_make_pagination_range_returns_a_pagination_range(self):
        pagination = make_pagination_range(
            page_range = list(range(1,21)),
            qty_pages = 4,
            current_page = 1,
        )["pagination"]
        self.assertEqual([1,2,3,4], pagination)

    def test_first_range_is_static_if_current_page_is_less_than_middle_page(self):
        pagination = make_pagination_range(
            page_range = list(range(1,21)),
            qty_pages = 4,
            current_page = 1,
        )["pagination"]
        self.assertEqual([1,2,3,4], pagination)

        pagination = make_pagination_range(
            page_range = list(range(1,21)),
            qty_pages = 4,
            current_page = 2,
        )["pagination"]   
        self.assertEqual([1,2,3,4], pagination)
        
    def test_make_sure_middle_ranges_are_correct(self):
        pagination = make_pagination_range(
            page_range = list(range(1,21)),
            qty_pages = 4,
            current_page = 10,
        )["pagination"]   
        self.assertEqual([9,10,11,12], pagination)

        pagination = make_pagination_range(
            page_range = list(range(1,21)),
            qty_pages = 4,
            current_page = 14,
        )["pagination"]   
        self.assertEqual([13,14,15,16], pagination)

    def test_make_pagination_range_is_static_when_last_page_is_next(self):

        pagination = make_pagination_range(
            page_range = list(range(1,21)),
            qty_pages = 4,
            current_page = 18,
        )["pagination"]   
        self.assertEqual([17,18,19,20], pagination)

        pagination = make_pagination_range(
            page_range = list(range(1,21)),
            qty_pages = 4,
            current_page = 19,
        )["pagination"]   
        self.assertEqual([17,18,19,20], pagination)

        pagination = make_pagination_range(
            page_range = list(range(1,21)),
            qty_pages = 4,
            current_page = 20,
        )["pagination"]   
        self.assertEqual([17,18,19,20], pagination)

    # def make_pagination_range( self, page_range, qty_pages, current_page ):
    #     range_len = len(page_range)
    #     page_breaker = int(round qty_pages/2+1.1,0))
    #     if current_page <= page_breaker:
    #         return list(range(1, qty_pages + 1))
    #     elif current_page > (range_len -  qty_pages - page_breaker)):
    #         return list(range(range_len - qty_pages + 1, range_len + 1))
    #     else:
    #         return list(range(current_page - page_breaker + 1, current_page +  qty_pages - page_breaker) + 1))
    #     ...

    # def test_make_pagination_range_returns_a_pagination_range_meu(self):
    #     pagination = self.make_pagination_range(
    #         page_range = list(range(1,21)),
    #         qty_pages = 6,
    #         current_page = 20,
    #     )
    #     self.assertEqual([15,16,17,18,19,20], pagination)