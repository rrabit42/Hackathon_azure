from django.conf import settings
from storages.backends.azure_storage import AzureStorage


# static과 media를 별도의 container로 동작하게 하기 위함
# 향후에 azure storage에서 static과 media 컨테이너 만들거임. 저 이름들과 일치시켜줘야함.
class StaticAzureStorage(AzureStorage):
    azure_container = 'static'

    def url(self, name):
        if not settings.DEBUG:
            cdn_host = getattr(settings, 'CDN_HOST', None)
            if cdn_host:
                return "{}/{}/{}".format(cdn_host, self.azure_container, name)
        return super().url(name)


class MediaAzureStorage(AzureStorage):
    azure_container = 'media'
