from .models import Invoice

class FindQuery:
    '''raw query version of invoice search'''

    def __init__(self):
        self.filters = {} # filters dict
        self.fq_sql = ''
        self.fq_select = 'SELECT * '
        self.fq_from = 'FROM invoice_invoice '
        self.fq_where = 'WHERE 1=1 '
        self.fq_order = ' ORDER BY iv_created_at DESC'

    def set_filters(self, user, year, client):
        if user:
            self.filters['request_user'] = user

        if year:
            self.filters['selected_year'] = year

        if client:
            self.filters['selected_client'] = client

        # adding here
    
    def apply_filter(self):

        if 'request_user' in self.filters:
            self.fq_where += ' AND iv_created_by = ' + str(self.filters.get('request_user'))

        if 'selected_year' in self.filters:
            self.fq_where += ' AND iv_year = ' + str(self.filters.get('selected_year'))
            
        if 'selected_client' in self.filters:
            self.fq_where += ' AND iv_client = ' + str(self.filters.get('selected_client'))

        # adding here

        # compose query
        self.fq_sql = self.fq_select + self.fq_from + self.fq_where + self.fq_order

        return Invoice.objects.raw(self.fq_sql)