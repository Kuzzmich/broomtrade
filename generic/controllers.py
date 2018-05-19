from django.views.generic.list import View


class PageNumberView(View):
    def get(self, request, *args, **kwargs):
        try:
            self.sort = self.request.GET['sort']
        except KeyError:
            self.sort = '0'
        try:
            self.order = self.request.GET['order']
        except KeyError:
            self.order = 'A'
        return super().get(request, *args, **kwargs)

    # def post(self, request, *args, **kwargs):
    #     try:
    #         pn = request.GET['page']
    #     except KeyError:
    #         pn = '1'
    #     self.success_url = self.success_url + '?page=' + pn
    #     return super().post(request, *args, **kwargs)
