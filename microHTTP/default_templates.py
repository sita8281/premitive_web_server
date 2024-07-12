import os

class DefaultTemplates:
    def __init__(self):
        pass

    def __get_file_html(self, name: str):
        normalize_path = os.path.join(os.path.dirname(__file__), name)
        with open(file=normalize_path, mode='rb') as file:
            return file.read(), file.__sizeof__()

    @property
    def get_405(self):
        return self.__get_file_html('base_templates/not_allowed.html')

    @property
    def get_404(self):
        return self.__get_file_html('base_templates/not_found.html')

    @property
    def get_403(self):
        return self.__get_file_html('base_templates/forbidden.html')

    @property
    def get_401(self):
        return self.__get_file_html('base_templates/unauthorized.html')

    @property
    def get_400(self):
        return self.__get_file_html('base_templates/bad_request.html')

    @property
    def get_500(self):
        return self.__get_file_html('base_templates/error.html')

