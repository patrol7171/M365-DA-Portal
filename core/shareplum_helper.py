from shareplum import Office365
from shareplum import Site
from shareplum.site import Version
from django.conf import settings


SP_USERNAME = settings.SP_USERNAME
SP_PASSWORD = settings.SP_PASSWORD


def get_data(team_slug, folder_name, file_name):
    authcookie = Office365('https://devpatrol.sharepoint.com', username=SP_USERNAME, password=SP_PASSWORD).GetCookies()
    site = Site('https://devpatrol.sharepoint.com/sites/'+team_slug, version=Version.v365, authcookie=authcookie, verify_ssl=False);
    folder = site.Folder('Shared Documents/'+ folder_name)
    response = folder.get_file(file_name)
    return response