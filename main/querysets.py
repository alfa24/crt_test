from django.contrib.postgres.search import TrigramSimilarity
from django.db.models import QuerySet


class AdvertQuerySet(QuerySet):
    def search_by_body(self, text):
        """Поиск по тексту объявления. Используется триграммный поиск для поиска с опечатками."""
        qs = self.annotate(
            similarity=TrigramSimilarity('body', text),
        ).filter(similarity__gte=0.3).order_by('-similarity')
        return qs
