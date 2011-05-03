from xml.dom import minidom
from SugarsyncObjects import xml2Dic as reformat
from SugarsyncObjects import *
import urllib2, urllib
import base64
import mimetypes
import mimetools

from pylabs import q
#sugarsync status codes: http://www.sugarsync.com/developers/rest-api-reference/responseCodes/index.html

HTTP_CREATED = 201 #from practical examples, authorization created returns 201
HTTP_OK = 200
HTTP_NO_CONTENT = 204 #An authorization token was created and provided to the client in the Location header.
HTTP_AUTH_REQUIRED = 401 # Authorization required.
HTTP_FORBIDDEN = 403  #Authentication failed.
HTTP_NOT_FOUND = 404

STATUS_OK = set([HTTP_CREATED, HTTP_OK, HTTP_NO_CONTENT])
STATUS_AUTH_REQ = set([HTTP_AUTH_REQUIRED, HTTP_FORBIDDEN])

AUTHORIZATION_HEADER = 'Authorization'
class AuthorizationError(Exception):
    pass

class SugarsyncClient(object):

    def authenticate(self, username, password, accesskeyid, privateaccesskey):
        
        '''Creating an Authorization Token
        
        After successful authentication, the method calls getUserInfo and populates the q.clients.sugarsync.user object with essential info about user and folders
        @param username: valid sugarsync login
        @param password: sugarsync password
        @param accesskeyid: access key associated with this account, a user can have multiple key-pairs
        @param privateaccesskey: second key of the key-pair
        @return: True if successful
        '''
        
        httpClientConnection = q.clients.http.getConnection()
        _baseurl = 'https://api.sugarsync.com/authorization'
        params = {'username':username, 'password':password, 'accessKeyId':accesskeyid, 'privateAccessKey':privateaccesskey}
        template = '''<?xml version="1.0" encoding="UTF-8" ?>
<authRequest>
    <username>%(username)s</username>
    <password>%(password)s</password>
    <accessKeyId>%(accessKeyId)s</accessKeyId>
    <privateAccessKey>%(privateAccessKey)s</privateAccessKey>
</authRequest>'''
        data = template%params
        headers = {'Content-Type' : 'application/xml'
                   ,'Content-Length' : len(data)
                   ,'Authorization' : None}
        resp = httpClientConnection.post(_baseurl, data=data, headers=headers)
        #resp = self._http_request(_baseurl, None, data=data, headers=headers)
        bodyDic = reformat(resp.read())
        auth_token_expiration = bodyDic['authorization'].expiration
        user = bodyDic['authorization'].user
        auth_token = resp.headers['location']
        return {'auth_token':auth_token, 'user':user, 'auth_token_expiration':auth_token_expiration}                                                                                          
        
    def getUserInfo(self, auth_token):
        '''Retrieving User Information
        
        There is no need to call this method explicitly since it is invoked during authentication to populate q.client.sugarsync.user object
        @return: user object
        '''
        httpClientConnection = q.clients.http.getConnection()
        _baseurl = 'https://api.sugarsync.com/user'
        resp = httpClientConnection.get(_baseurl, headers={'Authorization' : auth_token})
        #resp = self._http_request(_baseurl, headers={'Authorization' : auth_token})
        return User(resp.read())

    def _crudFolder(self, auth_token, folderUrl, displayName, method):
        
        httpClientConnection = q.clients.http.getConnection()
        _baseurl = folderUrl #'https://api.sugarsync.com/folder/myfolder'
        if method == 'DELETE':
            params, data = None, None
        else:
            params = {'displayName' : displayName}
            template = '''<?xml version="1.0" encoding="UTF-8"?>
    <folder>
        <displayName>%(displayName)s</displayName>
    </folder>'''
            data = template%params
        headers = {'Content-Type' : 'application/xml'
                   ,'Content-Length' : len(data) if data else 0
                   ,'Authorization' : auth_token}

        method = method.lower()
        resp = httpClientConnection.__getattribute__(method)(_baseurl, data=data, headers=headers)
        #resp = self._http_request(_baseurl, data=data, headers=headers, method=method)
        if method == 'delete':
            return True #resp headers don't carry any info and body is empty
        else:
            newFolderUrl = resp.headers['location'] 
            return newFolderUrl

    def createFolder(self, auth_token, parentFolderUrl, displayName):
        '''
        Creates a new folder under the parent folder url e.g. q.clients.sugarsync.user.webArchive acts as the root folder
        
        The new folder url is both returned and set as an attribute of the object q.client.sugarsync.recentFolders as a cache for future use
        @param parentFolderUrl: a valid sugarsync folder url owned by the current user e.g. webArchive and sub folders
        @displayName: name of the new folder, will be the name of the attribute of q.clients.sugarsync.recentFolders holding the URL
        @return: new folder url for future use 
        '''
        return self._crudFolder(auth_token, parentFolderUrl, displayName, 'POST')

    def renameFolder(self, auth_token, folderUrl, displayName):
        '''
        Change the name of an existing folder
        
        @param folderUrl: url of an existing folder
        @param displayName: new name 
        '''
        return self._crudFolder(auth_token, folderUrl, displayName, 'PUT')
    
    def deleteFolder(self, auth_token, folderUrl):
        '''
        Deletes an existing folder
        
        @param folderUrl: url of an existing folder 
        '''
        return self._crudFolder(auth_token, folderUrl, None, 'DELETE')
    
    def _crudFile(self, auth_token, fileUrl, displayName, mediaType, method, opt=None):
        
        httpClientConnection = q.clients.http.getConnection()
        _baseurl = fileUrl
        if method == 'DELETE':
            params, data = None, None
        else:
            params = {'displayName' : displayName, 'mediaType' : mediaType, 'optional' : '<ParentCollection>%s</ParentCollection>'%opt if opt else ''}
            template = '''<?xml version="1.0" encoding="UTF-8"?>
    <file>
        <displayName>%(displayName)s</displayName>
        <mediaType>%(mediaType)s</mediaType>
        %(optional)s
    </file>'''
            data = template%params
            
        headers = {'Content-Type' : 'application/xml'
                   ,'Content-Length' : len(data) if data else 0
                   ,'Authorization' : auth_token}
        
        method = method.lower()
        resp = httpClientConnection.__getattribute__(method)(_baseurl, data=data, headers=headers)
        #resp = self._http_request(_baseurl, data=data, headers=headers, method=method)
        if method == 'DELETE': 
            return True #resp headers don't carry any info and body is empty
        else:
            newfileUrl = resp.headers['location']
            return newfileUrl
        
    def createFile(self, auth_token, parentFolderUrl, displayName, mediaType):
        '''
        Create the metadata for a new file
        
        @param parentFolderUrl: url of the parent folder
        @param displayName: name of the new file entry
        @param mediaType: mimeType of the new file, you can use mimetypes.guess_type(localFilePath)[0] to produce this
        @return: new file url
        '''
        return self._crudFile(auth_token, parentFolderUrl, displayName, mediaType, 'POST')
    
    def renameFile(self, auth_token, fileUrl, newDisplayName, newMediaType, parentFolderUrl=None):
        '''
        Edit the metadata of an existing file
        
        @param fileUrl: url of an existing file
        @param newDisplayName: new name
        @param newMediaType: new mimetype if changed
        @param parentFolderUrl: optional, url of the parent folder 
        '''
        return self._crudFile(auth_token, fileUrl, newDisplayName, newMediaType, 'PUT', opt=parentFolderUrl)
        
    def deleteFile(self, auth_token, fileUrl):
        '''
        Delete an existing file
        @param fileUrl: url of an existing file
        @return True 
        '''
        return self._crudFile(auth_token, fileUrl, None, None, method='DELETE')
    
    def copyFile(self, auth_token, sourceFileUrl, targetFolder, targetFileName):
        '''
        Copy an existing file under another folder optionally with a new name
        
        @param sourceFileUrl: url of an existing file
        @param targetFolder: url of an existing folder
        @param targetFileName: name of the target file 
        '''
        httpClientConnection = q.clients.http.getConnection()
        _baseurl = targetFolder
        params = {'source' : sourceFileUrl, 'displayName' : targetFileName}
        template = '''<?xml version="1.0" encoding="UTF-8"?>
<fileCopy source="%(source)s">
   <displayName>%(displayName)s</displayName>
</fileCopy>'''
        data = template%params
        headers = {'Content-Type' : 'application/xml'
                   ,'Content-Length' : len(data)
                   ,'Authorization' : auth_token}
        resp = httpClientConnection.post(_baseurl, data=data, headerse=headers)
        return resp #self._http_request(_baseurl, data=data, headers=headers, method='POST')
    
    def _crudPublicFileLink(self, auth_token, fileUrl, enable=True):
        httpClientConnection = q.clients.http.getConnection()
        _baseurl = fileUrl
        params = {'enabled' : str(enable).lower()}
        template = '''<?xml version="1.0" encoding="UTF-8"?>
<file>
<publicLink enabled="%(enabled)s"/>
</file>'''
        data = template%params
        headers = {'Content-Type' : 'application/xml'
                   ,'Content-Length' : len(data)
                   ,'Authorization' : auth_token}
        #resp = self._http_request(_baseurl, data=data, headers=headers, method='PUT')
        resp = httpClientConnection.post(_baseurl, data=data, headers=headers)
        return File(resp.read())
    
    def filePublicLinkCreate(self, auth_token, fileUrl):
        '''
        Create a public link for an existing file for sharing
        
        @param fileUrl: url of an existing file
        @return: public link 
        '''
        return self._crudPublicFileLink(auth_token, fileUrl, True)
        
    def filePublicLinkDestroy(self, auth_token, fileUrl):
        '''
        Delete an existing public link, effectively disabling sharing
        
        @param fileUrl: url of an existing file, with sharing previously enabled
        '''
        return self._crudPublicFileLink(auth_token, fileUrl, False)
             
    def getFolderInfo(self, auth_token, folderUrl):
        '''Retrieving Folder Representation
        
        @param folderUrl: url of an existing folder
        @return: Folder object
        '''
        httpClientConnection = q.clients.http.getConnection()
        _baseurl = folderUrl
        resp = httpClientConnection.get(_baseurl, data=None, headers = {'Authorization' : auth_token})
        #resp = self._http_request(_baseurl, headers={'Authorization' : auth_token})
        return Folder(resp.read())

    def getFileInfo(self, auth_token, fileUrl):
        '''Retrieving File Representation
        
        @param fileUrl: url of an existing file
        @return: File object
        '''
        httpClientConnection = q.clients.http.getConnection()
        _baseurl = fileUrl
        resp = httpClientConnection.get(_baseurl, data=None, headers = {'Authorization' : auth_token})
        #resp = self._http_request(_baseurl, headers={'Authorization' : auth_token})
        return File(resp.read())

    def getWorkspaceInfo(self, auth_token, workspaceUrl):
        '''
        Retrieving Workspace Representation
        
        @param workspaceUrl: url of an existing workspace, Note workspaces cannot be created using the REST APIs
        @return: Workspace object
        '''
        httpClientConnection = q.clients.http.getConnection()
        _baseurl = workspaceUrl
        resp = httpClientConnection.get(_baseurl, data=None, headeres={'Authorization' : auth_token})
        #resp = self._http_request(_baseurl, headers={'Authorization' : auth_token})
        return Workspace(resp.read())
    
    def getAlbumsCollectionInfo(self, auth_token, albumsUrl):
        '''
        Retrieving Album Representation
        
        @param albumsUrl: url of albums collection, albums are folder that contain image files
        @return: Collection object 
        '''
        httpClientConnection = q.clients.http.getConnection()
        _baseurl = albumsUrl
        resp = httpClientConnection.get(_baseurl, data = None, headers={'Authorization' : auth_token})
        #resp = self._http_request(_baseurl, headers={'Authorization' : auth_token})
        return Albums(resp.read())
    
    def getAlbumInfo(self, auth_token, albumUrl):
        '''
        Retrieving a single album info, album is a folder that contain image files
        
        @param albumUrl: url of an existing album of an albums collection
        @return: Album object 
        '''
        httpClientConnection = q.clients.http.getConnection()
        _baseurl = albumUrl
        resp = httpClientConnection.get(_baseurl, data=None, headers={'Authorization' : auth_token})
        #resp = self._http_request(_baseurl, headers={'Authorization' : auth_token})
        return Album(resp.read())

    def _updateUrlParams(self, url, **kwargs):
        _scheme, _netloc, _url, _params, _query, _fragment = urllib2.urlparse.urlparse(url)
        params = urllib2.urlparse.parse_qs(_query)
        for k, v in params.items():#parse_qs puts the values in a list which corrupts the url later on
            params[k] = v.pop() if isinstance(v, list) else v
            
        for k, v in kwargs.items():
            if v is not None: params[k] = v
        _query = urllib.urlencode(params)
        return urllib2.urlparse.urlunparse((_scheme, _netloc, _url, _params, _query, _fragment))

    def getCollectionContents(self, auth_token, contentsUrl, type=None, start=0, max_=500):
        '''Retrieving CollectionContents Representation
        
        A Collection is a generic term that can reference a folder, album or workspace
        @param contentsUrl: url of a collection, preferably ending with /contents, the method appends this suffix if missing
        @param type: type of contents to enumerate. Valid values are "file" and "folder"
        @param start: numeric value to specify the start index to facilitate enumerating the contents in pages
        @param max: numeric value to specify the size of the returned collection to facilitate enumerating the contents in pages
        @return: CollectionContents object
        '''
        httpClientConnection = q.clients.http.getConnection()
        _baseurl = contentsUrl if contentsUrl.split('/')[-1].startswith('contents') else '%s/contents'%contentsUrl
        _baseurl = self._updateUrlParams(_baseurl, type=type, start=start, max=max_)
        resp = httpClientConnection.get(_baseurl, data=None, headers={'Authorization' : auth_token})
        #resp = self._http_request(_baseurl, headers={'Authorization' : auth_token})
        return CollectionContents(resp.read())

    def getFolderContents(self, auth_token, folderUrl, start=0, max_=500):
        '''
        Retrieves the files in a given folder
        
        @param folderUrl: url of an existing folder
        @param start: numeric value to specify the start index to facilitate enumerating the contents in pages
        @param max: numeric value to specify the size of the returned collection to facilitate enumerating the contents in pages
        @return: CollectionContents object representing the folder contents
        '''
        return self.getCollectionContents(auth_token, folderUrl, 'file', start, max_)

    def getSubFolders(self, auth_token, folderUrl, start=0, max_=500):
        '''
        Retrieves the sub folders in a given folder
        
        @param folderUrl: url of an existing folder
        @param start: numeric value to specify the start index to facilitate enumerating the contents in pages
        @param max: numeric value to specify the size of the returned collection to facilitate enumerating the contents in pages
        @return: CollectionContents object representing the folder contents
        '''
        return self.getCollectionContents(auth_token, folderUrl, type='folder', start=start, max_=max_)
        
    def getWorkspaceContents(self, auth_token, workspaceUrl, start=0, max_=500):
        '''
        Retrieves the folders in a given workspace
        
        @param workspaceUrl: url of an existing workspace
        @param start: numeric value to specify the start index to facilitate enumerating the contents in pages
        @param max: numeric value to specify the size of the returned collection to facilitate enumerating the contents in pages
        @return: CollectionContents object representing the workspace contents
        '''
        return self.getCollectionContents(auth_token, workspaceUrl, 'folder', start, max_)
    
    def getAlbumsCollectionContents(self, auth_token, albumsCollectionUrl, start=0, max_=500):
        '''
        Retrieves the contents in a given Albums Collection
        
        @param albumsCollectionUrl: url of an existing Albums Collection
        @param start: numeric value to specify the start index to facilitate enumerating the contents in pages
        @param max: numeric value to specify the size of the returned collection to facilitate enumerating the contents in pages
        @return: CollectionContents object representing the albumsCollection contents
        '''        
        return self.getCollectionContents(auth_token, albumsCollectionUrl, type='folder', start=start, max_=max_)
    
    def getAlbumContents(self, auth_token, albumUrl, start=0, max_=500):
        '''
        Retrieves the contents in a given Album
        
        @param albumUrl: url of an existing Albums
        @param start: numeric value to specify the start index to facilitate enumerating the contents in pages
        @param max: numeric value to specify the size of the returned collection to facilitate enumerating the contents in pages
        @return: CollectionContents object representing the album contents
        '''           
        return self.getCollectionContents(auth_token, albumUrl, type=None, start=start, max_=max_)
        
    def putFileData(self, auth_token, fileUrl, localFilePath):
        '''
        Send the file data to server, the file metadata entry must have been created previously
        
        @param fileUrl: url of an existing file, previously created metadata entry
        @param localFilePath: path to a local file
        @return: True
        '''
        httpClientConnection = q.clients.http.getConnection()
        _baseurl = fileUrl if fileUrl.split('/')[-1].startswith('data') else '%s/data'%fileUrl
        try:
            data = open(localFilePath).read()
            content_type = mimetypes.guess_type(localFilePath)[0]
            headers = {'Content-Type' : content_type
                       ,'Content-Length' : len(data)
                       ,'Authorization' : auth_token}
            resp = httpClientConnection.put(_baseurl, data=data, headers=headers)
            #resp = self._http_request(_baseurl, data=data, headers=headers, method='PUT')
            return True
        except:
            return Falses
            
    def retrieveFileData(self, auth_token, fileUrl, downloadPath, customHeaders={}):
        '''
        Download a file from server to a local path
        
        @param fileUrl: url of an existing file that has its data available on server (sent earlier)
        @param downloadPath: local directory to download into
        @param customHeaders: allows this method to be used to retrieve edited copies of an image
        @return: True
        '''
        httpClientConnection = q.clients.http.getConnection()
        _baseurl = fileUrl if fileUrl.split('/')[-1].startswith('data') else '%s/data'%fileUrl        
        
        customHeaders['Authorization'] = auth_token
        return httpClientConnection.download(fileUrl, downloadPath, customHeaders)
    
    def retrieveEditedImage(self, auth_token, imageUrl, downloadPath, widthPixels, heightPixels, square=False, clockWiseRotationCount=0):
        '''
        Download an edited version of an existing image file
        
        @param imageUrl: url of an existing image file
        @param downloadPath: local directory to download into
        @param widthPixels: edited version width in pixels
        @param heightPixels: edited version height in pixels
        @param square: boolean flag, make image square
        @param clockWiseRotationCount: number of clock wise rotations 0 to 3
        @return: True
        '''
        imageTranscodingHeader = 'image/jpeg; pxmax=%(widthPixels)s;pymax=%(heightPixels)s;sq=(%(square)d);r=(%(clockWiseRotationCount)d);'
        customHeaders = {'Accept' : imageTranscodingHeader%{'widthPixels' : widthPixels, 'heightPixels' : heightPixels, 'square' : 1 if square else 0, 'clockWiseRotationCount' : clockWiseRotationCount%4}}
        return self.retrieveFileData(auth_token, imageUrl, downloadPath, customHeaders)
        

 
