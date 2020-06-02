__all__ = ["FilterSetMixin"]


class FilterSetMixin:
    filter_class = None

    def filter_query(self, query, filter_params):
        if not hasattr(self, "filter_class") or self.filter_class is None:
            raise Exception("Should be declared filter_class for using FilterSetMixin")

        filter_ = self.filter_class()
        if not hasattr(filter_, "filter_query"):
            raise Exception("Unknown filter_class")

        return filter_.filter_query(query, filter_params)
