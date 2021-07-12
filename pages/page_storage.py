from pages.loader import Loader


class PageStorage(object):
    container = []
    max_size = 10
    loader = Loader()

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(PageStorage, cls).__new__(cls)
        return cls.instance

    def set_max_size(self, size: int):
        self.max_size = size

    def get(self, page_name: str):
        for page in self.container:
            if page.name == page_name:
                return page
        self._clear_container()
        page = self.loader.get_page(page_name)
        self.container.append(page)
        return page

    def _clear_container(self):
        if len(self.container) == self.max_size:
            del self.container[0]
