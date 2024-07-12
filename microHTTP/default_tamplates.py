
class DefaultTemplates:
    def __init__(self):
        pass

    def __get_file_html(self, name: str):
        with open(file=name, mode='wb') as file:
            return file.read()


    @property
    def get_405(self):
        return self.__get_file_html('base_templates/not_allowed.html')

    @property
    def get_404(self):
        pass

    @property
    def get_403(self):
        pass

    @property
    def get_401(self):
        pass

    @property
    def get_400(self):
        pass

    @property
    def get_500(self):
        pass

