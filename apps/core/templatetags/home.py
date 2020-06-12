from django.template import Library
from django.utils.http import urlencode

register = Library()


@register.filter
def pagination_page_numbers(current_page):
    """
    Return a list of page numbers which should be shown for page navigation.

    Example: When there are seven pages in total, the progression of page
    numbers which should be shown (where the current page is highlighted) are as
    follows:

    [1] 2  3  4  7
     1 [2] 3  4  7
     1 [3] 4  5  7
     1 [4] 5  6  7
     1  4 [5] 6  7
     1  4  5 [6] 7
     1  4  5  6 [7]
    """
    num_pages = current_page.paginator.num_pages

    # always show the first and last page number
    page_numbers = [1]
    if num_pages > 1:
        page_numbers.append(num_pages)

    # begin is the first of the incrementing sequence of numbers in the middle
    # which shouldn't be less than 2
    if current_page.number == 1:
        begin = 2
    elif current_page.number <= num_pages - 3:
        begin = current_page.number
    else:
        begin = max(num_pages - 3, 2)

    # end is the last of the incrementing sequence which shouldn't be greater
    # than num_pages - 1
    end = min(begin + 2, num_pages - 1)

    page_numbers.extend(range(begin, end + 1))

    return sorted(page_numbers)


@register.simple_tag(takes_context=True)
def update_query_string(context, **kwargs):
    """Return the current query string updated with the provided kwargs."""
    parameters = dict(context["request"].GET.items())
    parameters.update(kwargs)
    return "?" + urlencode(parameters)
