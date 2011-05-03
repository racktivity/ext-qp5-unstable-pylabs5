from pylabs import q
import mimetypes
from urllib2 import HTTPError
from SugarsyncObjects import Hook
from SugarsyncObjects import xml2Dic as reformat
from SugarsyncObjects import cleanString
from functools import partial
import SugarsyncClient 



class Sugarsync(object):
    '''
    High level client for Sugarsync APIs
    '''
        
    def listHomeFolders(self):
        '''
        Lists the folder in the webArchive associated with the current workspace
        
        The method lists the subfolders of the webArchive
        @return: list of Folder object containing essential folder attributes e.g. ref, displayName.
        '''
        coll = q.clients.sugarsyncapi.getSubFolders(q.clients.sugarsync.user.webArchive)
        return map(lambda attr: getattr(coll, attr), filter(lambda attr: attr.startswith('collection'), dir(coll)))
    
    
    def listHomeFolderUrls(self):
        '''
        Lists the folder URLs in the webArchive associated with the current workspace
        
        The method lists the subfolders of the webArchive
        @return: list of of URLs
        '''
        coll = self.listHomeFolders()
        return map(lambda x: x.ref, coll)
    
    
    def listHomeFiles(self):
        '''
        Lists the files in the webArchive associated with the current workspace
        
        The method lists the files in the webArchive
        @return: list of File object containing essential folder attributes e.g. ref, displayName, size, presentOnServer and mediaType
        '''        
        coll = q.clients.sugarsyncapi.getFolderContents(q.clients.sugarsync.user.webArchive)
        return map(lambda attr: getattr(coll, attr), filter(lambda attr: attr.startswith('file'), dir(coll)))
    
    
    def listHomeFileUrls(self):
        '''
        Lists the file URLs in the webArchive associated with the current workspace
        
        The method lists the files in the webArchive
        @return: list of of URLs
        '''
        coll = self.listHomeFiles()
        return map(lambda x: x.ref, coll)
    
    
    def _copyMethods(self):
        methodNames = ['copyFile',
 'createFolder',
 'deleteFile',
 'deleteFolder',
 'filePublicLinkCreate',
 'filePublicLinkDestroy',
 'getAlbumContents',
 'getAlbumInfo',
 'getAlbumsCollectionContents',
 'getAlbumsCollectionInfo',
 'getCollectionContents',
 'getFileInfo',
 'getFolderContents',
 'getFolderInfo',
 'getSubFolders',
 'getWorkspaceContents',
 'getWorkspaceInfo',
 'recentFiles',
 'recentFolders',
 'renameFile',
 'renameFolder',
 'retrieveEditedImage',
 'retrieveFileData']
        for name in methodNames:
            setattr(self, name, getattr(q.clients.sugarsyncapi, name))
    
    
    def getConnection(self, email, password=None, accesskeyid=None, privateaccesskey=None, saveCredentials=False):
        return SugarsyncConnection(email, password, accesskeyid, privateaccesskey, saveCredentials)


    
class SugarsyncConnection(object):
    def __init__(self, email, password=None, accesskeyid=None, privateaccesskey=None, saveCredentials=False):
        self.__dict__ = {}
        self._folderInit = False
        self._albumInit = False
        sessionDict = None
        cfgpath = q.system.fs.joinPaths(q.dirs.extensionsDir, 'clients', 'sugarsync', 'sugarsync.cfg')
        cfgfile = q.tools.inifile.open(cfgpath)
        if password and accesskeyid and privateaccesskey:
            try:
                sessionDict = q.clients.sugarsyncapi.authenticate(email, password, accesskeyid, privateaccesskey)
            except HTTPError, ex:
                q.logger.log(ex)
                if ex.code == SugarsyncClient.HTTP_AUTH_REQUIRED:
                    raise RuntimeError('Authorization Error: Wrong credentials, please verify and try again')
            if saveCredentials:
                cfgfile.addSection(email)
                params = {'username':email, 'password':password, 'accessKeyId':accesskeyid, 'privateAccessKey':privateaccesskey}
                for k, v in params.items():
                    cfgfile.addParam(email, k, v)
        else:
            if cfgfile.checkSection(email):
                credentials = cfgfile.getSectionAsDict(email)
                sessionDict = q.clients.sugarsyncapi.authenticate(**credentials)
            else:
                raise RuntimeError('Credentials not stored, please enter full credentials')    
        self._initConnection(sessionDict)
        
                    
    def __dir__(self):
        attrs = object.__getattribute__(self, '__dict__').keys()
        attrs.extend(['folders', 'albums'])
        return attrs
                    
    def _initConnection(self, sessionDict):                
        self._auth_token_expiration = sessionDict['auth_token_expiration']
        self._auth_token = sessionDict['auth_token']
        self._user_session = q.clients.sugarsyncapi.getUserInfo(self._auth_token)
        self.user = self._user_session.username
        
    
    def __getattribute__(self, name):
        if name == 'folders' and not object.__getattribute__(self, '_folderInit'):# and object.__getattribute__(self, 'folders') == None:
            q.logger.log('getting attribute folders for connection')
            self.folders = Folders(self, self._user_session.webArchive)
            self.__setattr__('_folderInit', True)
            return object.__getattribute__(self, 'folders')
        elif name == 'albums' and not object.__getattribute__(self, '_albumInit'):# and object.__getattribute__(self, 'albums') == None:
            q.logger.log('getting attribute albums for connection',5)
            self.albums = Albums(self, self._user_session.albums, 'albums')
            self.__setattr__('_albumInit', True)
            return object.__getattribute__(self, 'albums')
        elif name in object.__getattribute__(self, '__dict__'):
            return object.__getattribute__(self, '__dict__')[name]
        else:
            return object.__getattribute__(self, name)


    def __setattr__(self, name, value):
        object.__setattr__(self, name, value)


    def reset(self):
        self.folders = Folders(self, self._user_session.webArchive)
        self.albums = Albums(self, self._user_session.albums, 'albums')  
          
          
    def __iter__(self):
        return SugarsyncIterator(self.__dict__)
        
        
    def __getitem__(self, key):
        key = cleanString(key)
        return self.__getattribute__(key)
            
    
        
class Folder(object):
    def __init__(self, conn, baseurl, displayName, hasChildren=True):
        self._subFolders = None
        self._conn = conn
        self.baseurl = baseurl
        self.displayName = displayName
        self.files = Files(object.__getattribute__(self, '_conn'), object.__getattribute__(self, 'baseurl'))
        self.folders = folders = Folders(object.__getattribute__(self, '_conn'), object.__getattribute__(self, 'baseurl'))
        self._hasChildren = hasChildren
        
    def delete(self):
        q.clients.sugarsyncapi.deleteFolder(self._conn._auth_token, self.baseurl)
        
    def __iter__(self):
        return SugarsyncIterator(self.__dict__)
    
    
    def __setattr__(self, name, value):
        object.__setattr__(self, name, value)
        
        
    def __getitem__(self, key):
        key = cleanString(key)
        try:
            return self.files[key]
        except:
            q.logger.log('%s is not a file'%key)
        try:
            return self.folders[key]
        except:
            q.logger.log('%s is not a folder'%key)
        return self.__dict__[key]
    
    def new(self, displayName):
        newfolderUrl = q.clients.sugarsyncapi.createFolder(self._conn._auth_token, self.baseurl, displayName)

    def _putFile(self, localFilePath, parentFolderUrl, displayName=None, mediaType='application/octet-stream'):
        '''Puts a new file from local path to sugarsync
        
        This scenario method creates the file metadata entry and then puts the file data if successful
        the new file url is set as an attribute of the q.clients.sugarsync.recentFiles with the displayName as attribute name
        @param localFilePath: a valid system path to the local file
        @type: path
        @param parentFolderUrl: a valid sugarsync folder url owned by the current user e.g. webArchive and sub folders
        @type: url
        @param displayName: an alias for the file on the server, if None the local file name would be used
        @type: string
        @param mediaType: a valid mime type describing the file content, if not specified the file extension would be used to guess a valid mimetype
        '''
        displayName = displayName or q.system.fs.getBaseName(localFilePath)
        mediaType = mimetypes.guess_type(localFilePath)[0] or mediaType 
        resp = q.clients.sugarsyncapi.createFile(self._conn._auth_token, parentFolderUrl, displayName, mediaType)
        #simple check for successful file metadata creation
        if not (isinstance(resp, str) and resp.startswith('https://api.sugarsync.com/file')): raise Exception('Error while creating file')
        q.clients.sugarsyncapi.putFileData(self._conn._auth_token, resp, localFilePath)
        setattr(self, cleanString(displayName), File(self._conn, resp, cleanString(displayName)))

    def newFile(self, localFilePath, displayName=None, mediaType='application/octet-stream'):
        self._putFile(localFilePath, self.baseurl, displayName, mediaType)
    
    def __repr__(self):
        return '<Folder "%s" for user "%s" on Sugarsync>'%(self.displayName, self._conn._user_session.username)
    
    
    
class Folders(object):
    def __init__(self, conn, baseurl):
        self._conn = conn
        self._baseurl = baseurl
        self._subFolders = {}
        self.__setattr__('new', partial(self._new, self._baseurl))
        self._initialized = False
        
    def __dir__(self):
        attrs = object.__getattribute__(self, '__dict__').keys()
        if not object.__getattribute__(self, '_initialized'):
            object.__getattribute__(self, '_getChildren').__call__()
            attrs.extend(object.__getattribute__(self, '_subFolders').keys())
        return attrs
    
    def _getChildren(self):
        self.__setattr__('_children', q.clients.sugarsyncapi.getSubFolders(self._conn._auth_token, self._baseurl))
        self._subFolders = dict(zip(
                                    map(lambda attr: cleanString(getattr(attr, 'displayName')),
                                        filter(lambda child: hasattr(child, 'displayName'), self._children.__dict__.values())),
                                            map(lambda attr: getattr(attr, 'ref'),
                                                filter(lambda child: hasattr(child, 'displayName'), self._children.__dict__.values()))))
        map(lambda folderObj: self.__setattr__(folderObj, Folder(self._conn, self._subFolders[folderObj], folderObj)), self._subFolders.keys())
        self._initialized = True
        
        
    def __getattribute__(self, name):
        if not name.startswith('_') and not object.__getattribute__(self, '_initialized'):
            object.__getattribute__(self, '_getChildren').__call__()
        if name in object.__getattribute__(self, '__dict__'):
            return object.__getattribute__(self, '__dict__')[name]
        else:
            return object.__getattribute__(self, name)
        
        
    def __setattr__(self, name, value):
        object.__setattr__(self, name, value)
    
    
    def __iter__(self):
        if not object.__getattribute__(self, '_initialized'):
            object.__getattribute__(self, '_getChildren').__call__()        
        return SugarsyncIterator(self.__dict__)
            
            
    def _new(self, parentUrl, displayName):
        newfolderUrl = q.clients.sugarsyncapi.createFolder(self._conn._auth_token, parentUrl, displayName)
        self.__setattr__(cleanString(displayName), Folder(self._conn, newfolderUrl, displayName, False))
        
        
    def __getitem__(self, key):
        if not object.__getattribute__(self, '_initialized'):
            object.__getattribute__(self, '_getChildren').__call__()
        key = cleanString(key)
        return self.__dict__[key]
        
            
              
class Files(object):
    def __init__(self, conn, parentUrl):
        self._conn = conn
        self._parentUrl = parentUrl
        self._files = {}
        self._initialized = False
        
        
    def __dir__(self):
        q.logger.log('initialized is %s'%object.__getattribute__(self, '_initialized'))
        attrs = object.__getattribute__(self, '__dict__').keys()
        if not object.__getattribute__(self, '_initialized'):
            object.__getattribute__(self, '_getChildren').__call__()
            attrs.extend(object.__getattribute__(self, '_files').keys())
        q.logger.log('initialized is %s'%object.__getattribute__(self, '_initialized'))
        return attrs

    
    def _getChildren(self):
        self._initialized = True
        self._children = q.clients.sugarsyncapi.getFolderContents(self._conn._auth_token, self._parentUrl)
        self._files = dict(zip(
                                map(lambda attr: cleanString(getattr(attr, 'displayName')),
                                    filter(lambda child: hasattr(child, 'displayName'), self._children.__dict__.values())),
                                        map(lambda attr: getattr(attr, 'ref'),
                                            filter(lambda child: hasattr(child, 'mediaType'), self._children.__dict__.values()))))
        map(lambda fileObj: self.__setattr__(fileObj, File(self._conn, self._files[fileObj], fileObj)), self._files.keys())
        
        
        
    def __getattribute__(self, name):
        if not name.startswith('_') and not object.__getattribute__(self, '_initialized'):
            object.__getattribute__(self, '_getChildren').__call__()
        if name in object.__getattribute__(self, '__dict__'):
            return object.__getattribute__(self, '__dict__')[name]
        else:
            return object.__getattribute__(self, name)

    
    def __setattr__(self, name, value):
        object.__setattr__(self, name, value)
        
        
    def new(self, localFilePath, displayName=None, mediaType='application/octet-stream'):
        self._putFile(localFilePath, self._parentUrl, displayName, mediaType)
        
        
    def _putFile(self, localFilePath, parentFolderUrl, displayName=None, mediaType='application/octet-stream'):
        '''Puts a new file from local path to sugarsync
        
        This scenario method creates the file metadata entry and then puts the file data if successful
        the new file url is set as an attribute of the q.clients.sugarsync.recentFiles with the displayName as attribute name
        @param localFilePath: a valid system path to the local file
        @type: path
        @param parentFolderUrl: a valid sugarsync folder url owned by the current user e.g. webArchive and sub folders
        @type: url
        @param displayName: an alias for the file on the server, if None the local file name would be used
        @type: string
        @param mediaType: a valid mime type describing the file content, if not specified the file extension would be used to guess a valid mimetype
        '''
        displayName = displayName or q.system.fs.getBaseName(localFilePath)
        mediaType = mimetypes.guess_type(localFilePath)[0] or mediaType 
        resp = q.clients.sugarsyncapi.createFile(self._conn._auth_token, parentFolderUrl, displayName, mediaType)
        #simple check for successful file metadata creation
        if not (isinstance(resp, str) and resp.startswith('https://api.sugarsync.com/file')): raise Exception('Error while creating file')
        q.clients.sugarsyncapi.putFileData(self._conn._auth_token, resp, localFilePath)
        setattr(self, cleanString(displayName), File(self._conn, resp, cleanString(displayName)))
    
    
    def __iter__(self):
        if not object.__getattribute__(self, '_initialized'):
            object.__getattribute__(self, '_getChildren').__call__()
        return SugarsyncIterator(self.__dict__)
    
    
    def __getitem__(self, key):
        if not object.__getattribute__(self, '_initialized'):
            object.__getattribute__(self, '_getChildren').__call__()
        key = cleanString(key)
        return self.__dict__[key]       



class File(object):
    def __init__(self, conn, baseurl, displayName):
        self._conn = conn
        self.baseurl = baseurl
        self.displayName = displayName
        self.__dict__.update(q.clients.sugarsyncapi.getFileInfo(self._conn._auth_token, self.baseurl).__dict__)
        
        
    def __iter__(self):
        return SugarsyncIterator(self.__dict__)


    def upload(self, localFilePath):
        q.clients.sugarsyncapi.putFileData(self._conn._auth_token, self.fileData, localFilePath)
        self.__dict__.update(q.clients.sugarsyncapi.getFileInfo(self._conn._auth_token, self.baseurl).__dict__)


    def download(self, localFilePath):
        """
        download the selected file to a local location.
        You can enter a folder path for the file to be downloaded in or a file path to rename the file manually.
        """
        q.logger.log('downloading file %s to path %s'%(self.displayName, localFilePath))
        if self.presentOnServer:
            try:
                q.clients.sugarsyncapi.retrieveFileData(self._conn._auth_token, self.fileData, localFilePath)
                q.logger.log('file %s downloaded succesfully to path %s'%(self.displayName, localFilePath))
            except IOError:
                localFilePath = localFilePath+'/%s'%self.displayName
                q.clients.sugarsyncapi.retrieveFileData(self._conn._auth_token, self.fileData, localFilePath)
                q.logger.log('file %s downloaded succesfully to path %s'%(self.displayName, localFilePath))
            except AttributeError:
                q.logger.log('file %s has no attribute FileData'%self.displayName)
        else:
            return False
        
        
    def __getitem__(self, key):
        key = cleanString(key)
        return self.__dict__[key]
    
    
    def __repr__(self):
        return '<File "%s" for user "%s" on Sugarsync>'%(self.displayName, self._conn._user_session.username)
       
       
       
class Albums(object):
    def __init__(self, conn, baseurl, displayName):
        self._albums = {}
        self._conn = conn
        self._baseurl = baseurl
        self._displayName = displayName
        self._initialized = False
        
    def __dir__(self):
        attrs = object.__getattribute__(self, '__dict__').keys()
        if not object.__getattribute__(self, '_initialized'):
            object.__getattribute__(self, '_getChildren').__call__()
            attrs.extend(object.__getattribute__(self, '_albums').keys())
        return attrs
        
        
    def _getChildren(self):
        self._children = q.clients.sugarsyncapi.getAlbumsCollectionContents(self._conn._auth_token, self._baseurl)
       
        map(lambda fileObj: self.__setattr__(cleanString(fileObj.displayName), None),
             filter(lambda attr: hasattr(attr, 'displayName'), self._children.__dict__.values()))

        self._albums = dict(zip(
                                 map(lambda attr: cleanString(getattr(attr, 'displayName')),
                                     filter(lambda child: hasattr(child, 'displayName'), self._children.__dict__.values())),
                                         map(lambda attr: getattr(attr, 'ref'),
                                             filter(lambda child: hasattr(child, 'displayName'), self._children.__dict__.values()))))
        
        map(lambda albumObj: self.__setattr__(albumObj, Album(self._conn, self._albums[albumObj], albumObj)), self._albums.keys())
        self._initialized = True
       
    
    def __getattribute__(self, name):
        if not name.startswith('_') and not object.__getattribute__(self, '_initialized'):
            object.__getattribute__(self, '_getChildren').__call__()
        if name in object.__getattribute__(self, '__dict__'):
            return object.__getattribute__(self, '__dict__')[name]
        else:
            return object.__getattribute__(self, name)
           
           
    def __iter__(self):
        if not object.__getattribute__(self, '_initialized'):
            object.__getattribute__(self, '_getChildren').__call__()
        return SugarsyncIterator(self.__dict__)
           
           
    def __setattr__(self, name, value):
        object.__setattr__(self, name, value)
       
       
    def __getitem__(self, key):
        if not object.__getattribute__(self, '_initialized'):
            object.__getattribute__(self, '_getChildren').__call__()
        key = cleanString(key)
        return self.__dict__[key]
        
        
        
class Album(object):
    def __init__(self, conn, baseurl, displayName):
        self._conn = conn
        self._baseurl = baseurl
        self.displayName = displayName
        self.photos = Photos(object.__getattribute__(self, '_conn'), object.__getattribute__(self, '_baseurl'))
        
    def __iter__(self):
        return SugarsyncIterator(self.__dict__)
        
        
    def __getitem__(self, key):
        key = cleanString(key)
        try:
            return self.photos[key]
        except KeyError:
            return self.__dict__[key]
    
    
    def __repr__(self):
        return '<Album "%s" for user "%s" on Sugarsync>'%(self.displayName, self._conn._user_session.username)



class Photos(object):
    def __init__(self, conn, parentUrl):
       self._conn = conn
       self._photos = {}
       self._parentUrl = parentUrl
       self._initialized = False
       
    def __dir__(self):
        attrs = object.__getattribute__(self, '__dict__').keys()
        if not object.__getattribute__(self, '_initialized'):
            object.__getattribute__(self, '_getChildren').__call__()
            attrs.extend(object.__getattribute__(self, '_photos').keys())
        return attrs
       
       
    def _getChildren(self):
        self._initialized = True
        self._children = q.clients.sugarsyncapi.getAlbumContents(self._conn._auth_token, self._parentUrl)
        self._photos = dict(zip(
                                 map(lambda attr: cleanString(getattr(attr, 'displayName')),
                                     filter(lambda child: hasattr(child, 'displayName'), self._children.__dict__.values())),
                                         map(lambda attr: getattr(attr, 'ref'),
                                             filter(lambda child: hasattr(child, 'mediaType'), self._children.__dict__.values()))))
        
        map(lambda photoObj: self.__setattr__(photoObj, Photo(self._conn, self._photos[photoObj], photoObj)), self._photos.keys())
           
    def __getattribute__(self, name):
        if not name.startswith('_') and not object.__getattribute__(self, '_initialized'):
            object.__getattribute__(self, '_getChildren').__call__()
            self._initialized = True
        if name in object.__getattribute__(self, '__dict__'):
            return object.__getattribute__(self, '__dict__')[name]
        else:
            return object.__getattribute__(self, name)

    
    def __setattr__(self, name, value):
        object.__setattr__(self, name, value)
       
       
    def __iter__(self):
        if not object.__getattribute__(self, '_initialized'):
            object.__getattribute__(self, '_getChildren').__call__()
        return SugarsyncIterator(self.__dict__)
    
    
    def __getitem__(self, key):
        if not object.__getattribute__(self, '_initialized'):
            object.__getattribute__(self, '_getChildren').__call__()
        key = cleanString(key)
        return self.__dict__[key]



class Photo(object):
    def __init__(self, conn, baseurl, displayName):
        self._conn = conn
        self._baseurl = baseurl
        self.displayName = displayName
        self.__dict__.update(q.clients.sugarsyncapi.getFileInfo(self._conn._auth_token, self._baseurl).__dict__)
        
        
    def __iter__(self):
        return SugarsyncIterator(self.__dict__)


    def download(self, localFilePath):
        """
        download the selected photo to a local location.
        You can enter a folder path for the file to be downloaded in or a file path to rename the photo manually.
        """
        q.logger.log('downloading file %s to path %s'%(self.displayName, localFilePath))
        if self.presentOnServer:
            try:
                q.clients.sugarsyncapi.retrieveFileData(self._conn._auth_token, self.fileData, localFilePath)
                q.logger.log('file %s downloaded succesfully to path %s'%(self.displayName, localFilePath))
            except IOError:
                localFilePath = localFilePath+'/%s'%self.displayName
                q.clients.sugarsyncapi.retrieveFileData(self._conn._auth_token, self.fileData, localFilePath)
                q.logger.log('file %s downloaded succesfully to path %s'%(self.displayName, localFilePath))
            except AttributeError:
                q.logger.log('photo %s has no attribute FileData'%self.displayName)
        else:
            q.logger.log('file %s not downloaded to path %s'%(self.displayName, localFilePath))
            return False
        
        
    def __getitem__(self, key):
        key = cleanString(key)
        return self.__dict__[key]
    
    
    def __repr__(self):
        return '<Photo "%s" for user "%s" on Sugarsync>'%(self.displayName, self._conn._user_session.username)
    
    
    
class SugarsyncIterator(object):
    def __init__(self, dict):
        self.inputDict = dict
        self.attributes = map(lambda attr: self.inputDict[attr], filter(lambda attr: attr not in ['new', 'files', 'folders', 'albums', 'delete', None], filter(lambda attr: not attr.startswith('_'), self.inputDict.keys())))
        self.index = 0

    
    def __iter__(self):
        return self
    
    
    def next(self):
        if self.index == len(self.attributes):
            raise StopIteration()
        attr = self.attributes[self.index]
        self.index += 1
        return attr
