from django.core.paginator import *
from django.db import connection, transaction
# from django.db import connection, transaction, OperationalError


class TimeLimitedPaginator(Paginator):
   """
   Paginator that enforces a timeout on the count operation.
   If the operations times out, a fake bogus value is
   returned instead.
   """

   @cached_property
   def count(self):
       # # We set the timeout in a db transaction to prevent it from
       # # affecting other transactions.
       # with transaction.atomic(), connection.cursor() as cursor:
       #     cursor.execute('SET LOCAL statement_timeout TO 200;')
       #     try:
       #         return super().count
       #     except OperationalError:
       #         return 9999999999
       return 9999999999

def PaginatedData(limit=None, page=None, data=None):
    # ============== setup for pagination ================
    if limit is None or limit is '' or limit is 0:
        limit = 10

    if page is None or page is '' or page is 0:
        page = 1

    if data is None or data is '' or data is 0:
        data = []

    record_size = int(limit)
    # ============== end setup for pagination ============

    total_objects = len(data)#data.count()
    Paginator = TimeLimitedPaginator
    paginator = Paginator(data, int(record_size))
    paginated_data = paginator.get_page(page)

    try:
        PageExists = paginator.page(page)
    except InvalidPage:
        PageExists = False;

    if PageExists:
        result = paginated_data
    else:
        result = data

    response = {
        "result":result,
        "total":total_objects
    }
    return response
