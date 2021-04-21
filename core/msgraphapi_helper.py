from requests_oauthlib import OAuth2Session


graph_url = 'https://graph.microsoft.com/v1.0'


def get_user(token):
    graph_client = OAuth2Session(token=token)
    # Configure query parameters to modify the results
    query_params = {
    '$select': 'displayName,givenName,jobTitle,department,mail,userPrincipalName',
    }   
    user = graph_client.get('{0}/me'.format(graph_url), params=query_params)
    # Return the JSON result
    return user.json()


def get_team_members(token, grpid):
    graph_client = OAuth2Session(token=token)
    # Configure query parameters to modify the results
    query_params = {
    '$select': 'displayName,userPrincipalName,department,jobTitle',
    }
    members = graph_client.get('{0}/groups/{1}/members'.format(graph_url,grpid), params=query_params)
    # Return the JSON result
    return members.json()
    
 
#def get_photo(token):
#    graph_client = OAuth2Session(token=token)    
#    photo_response = graph_client.get('{0}/me/photos/48x48/$value'.format(graph_url))
#    photo = photo_response.raw.read()
#    # Remove /$value from endpoint to get metadata endpoint
#    metadata_response = session.get(api_endpoint(endpoint[:-7]))
#    content_type = metadata_response.json().get('@odata.mediaContentType', '')            
#    return (photo, content_type)    
    
