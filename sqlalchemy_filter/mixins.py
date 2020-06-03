import sqlalchemy_filter.exceptions

__all__ = ["FilterSetMixin"]


class FilterSetMixin:
    filter_class = None

    def filter_query(self, query, filter_params):
        if not hasattr(self, "filter_class") or self.filter_class is None:
            raise sqlalchemy_filter.exceptions.FilterException(
                "Should be declared filter_class for using FilterSetMixin"
            )

        filter_ = self.filter_class()
        if not hasattr(filter_, "filter_query"):
            raise sqlalchemy_filter.exceptions.FilterException("Unknown filter_class")

        return filter_.filter_query(query, filter_params)
