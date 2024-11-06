from rest_framework.pagination import PageNumberPagination


class LargeResultsSetPagination(PageNumberPagination):
    """
    Paginator für größere Ergebnismengen. Standardmäßig werden 6 Einträge pro Seite
    zurückgegeben, und die Anzahl kann über das `page_size`-Parameter angepasst werden.
    
    Attribute:
        - page_size (int): Standardanzahl der Elemente pro Seite (6).
        - page_size_query_param (str): Name des Parameters zur dynamischen Anpassung der Seitengröße.
        - max_page_size (int): Maximale Anzahl von Einträgen pro Seite (100).
    """
    page_size = 6
    page_size_query_param = 'page_size'
    max_page_size = 100