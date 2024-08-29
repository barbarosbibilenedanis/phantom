from django.contrib.admin import SimpleListFilter
from django.utils.html import format_html

class TableIconFilter(SimpleListFilter):
    title = 'Table'  # Filtre başlığı
    parameter_name = 'table'
    
    def lookups(self, request, model_admin):
        # Burada filtreleme seçeneklerini belirleyin
        return [
            (1, 'Masa 1'),
            (2, 'Masa 2'),
            (3, 'Masa 3'),
        ]
    
    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(table=self.value())
        return queryset

    def choices(self, cl):
        # Filtre seçeneklerini alt alta ve ikonlarla göstermek için
        for lookup, title in self.lookup_choices:
            yield {
                'selected': self.value() == str(lookup),
                'query_string': cl.get_query_string({self.parameter_name: lookup}),
                'display': format_html('<div style="margin-bottom: 10px;">'
                                      '<a href="{}">'
                                      '<img src="/static/icons/table{}.png" alt="{}" style="width: 40px; height: 40px; margin-right: 10px;">'
                                      '{}'
                                      '</a></div>',
                                      self.query_string, lookup, title, title),
            }