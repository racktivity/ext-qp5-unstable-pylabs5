from xml.dom import minidom
from SugarsyncObjects import xml2Dic as reformat
from SugarsyncObjects import *


class SugarsyncStub(object):
    def __init__(self):
        pass
    
    
    def authenticate(self, *args, **kwargs):
        auth_dict = {'auth_token_expiration':'token_expiration','user':'user_url', 'auth_token':'token'}
        return auth_dict
    
    def getUserInfo(self, *args, **kwargs):
        user_response = self.responses['getUserInfo']
        return User(user_response)
    
    
    def getSubFolders(self, auth_token, folderUrl, start=0, max_=500):
        sub_folder_reponse = self.responses['getSubFolders-%s'%folderUrl]
        return CollectionContents(sub_folder_reponse)
    
    def createFolder(self):
        pass
    
    
    def getFolderContents(self, auth_token, folderUrl, start=0, max_=500):
        folder_contents_response = self.responses['getFolderContents-%s'%folderUrl]
        return CollectionContents(folder_contents_response)
    
    
    def createFile(self):
        pass
    
    
    def putFileData(self):
        pass
    
    
    def getFileInfo(self, auth_token, fileUrl):
        file_info_response = self.responses['getFileInfo-%s'%fileUrl]
        return File(file_info_response)
    
    
    def retrieveFileData(self):
        pass
    
    
    def getAlbumContents(self, auth_token, albumUrl, *args, **kwargs):
        album_contents_response = self.responses['getAlbumContents-%s'%albumUrl]
        return CollectionContents(album_contents_response)
    
    def getAlbumsCollectionContents(self, auth_token, albumUrl, *args, **kargs):
        album_collection_contents_response = self.responses['getAlbumsCollectionContents-%s'%albumUrl]
        return CollectionContents(album_collection_contents_response)
    
    
        
    responses = {'getUserInfo':'''<?xml version="1.0" encoding="utf-8"?>
                            <user>
                              <username>username@company.com</username>
                              <nickname>user</nickname>
                              <salt>fPqrZw==</salt>
                              <quota>
                                <limit>2147483648</limit>
                                <usage>28487442</usage>
                              </quota>
                              <workspaces>userWorkspace</workspaces>
                              <syncfolders>userSyncfolders</syncfolders>
                              <deleted>userDeleted</deleted>
                              <magicBriefcase>userMagicBriefcase</magicBriefcase>
                              <webArchive>home</webArchive>
                              <mobilePhotos>userMobilePhotos</mobilePhotos>
                              <albums>userAlbums</albums>
                              <recentActivities>userRecentActivities</recentActivities>
                              <receivedShares>userReceivedShares</receivedShares>
                              <publicLinks>userPublicLinks</publicLinks>
                            </user>''',
                 'getSubFolders-home':'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
                     <collectionContents start="0" hasMore="false" end="1">
                         <collection type="folder">
                             <displayName>folder1</displayName>
                             <ref>folder1</ref>
                             <contents>folder1/contents</contents>
                         </collection>
                         <collection type="folder">
                             <displayName>folder2</displayName>
                             <ref>folder2</ref>
                             <contents>folder2/contents</contents>
                        </collection>
                     </collectionContents>''',
                 'getSubFolders-folder1':'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
                 <collectionContents start="0" hasMore="false" end="1">
                     <collection type="folder">
                         <displayName>folder1-1</displayName>
                         <ref>folder1-1</ref>
                         <contents>folder1-1/contents</contents>
                     </collection>
                 </collectionContents>''',
                 'getSubFolders-folder1-1':'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
                         <collectionContents start="0" hasMore="false" end="0"/>''',
                 'getSubFolders-folder2':'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
                         <collectionContents start="0" hasMore="false" end="0"/>''',
                 'getFolderContents-home':'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
                 <collectionContents start="0" hasMore="false" end="0"/>''',
                 'getFolderContents-folder1':'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
                         <collectionContents start="0" hasMore="false" end="0">
                             <file>
                                 <displayName>file1-1</displayName>
                                 <ref>file1-1</ref>
                                 <size>48601</size>
                                 <lastModified>2011-03-15T02:56:35.000-07:00</lastModified>
                                 <mediaType>application/octet-stream</mediaType>
                                 <presentOnServer>true</presentOnServer>
                                 <fileData>file1-1/data</fileData>
                             </file>
                         </collectionContents>''',
                 'getFolderContents-folder1-1':'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
                 <collectionContents start="0" hasMore="false" end="0"/>''',
                 'getFolderContents-folder2':'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
                 <collectionContents start="0" hasMore="false" end="0"/>''',
                 'getFileInfo-file1-1':'''<?xml version="1.0" encoding="UTF-8"?><file>
                                 <displayName>file1-1</displayName>
                                 <ref>file1-1</ref>
                                 <size>48601</size>
                                 <lastModified>2011-03-15T02:56:35.000-07:00</lastModified>
                                 <mediaType>application/octet-stream</mediaType>
                                 <presentOnServer>true</presentOnServer>
                                 <fileData>file1-1/data</fileData>
                             </file>''',
                 'getFileInfo-image1':'''<?xml version="1.0" encoding="UTF-8"?><file>
                                 <displayName>image1</displayName>
                                 <ref>image1</ref>
                                 <size>48601</size>
                                 <lastModified>2011-03-15T02:56:35.000-07:00</lastModified>
                                 <mediaType>image/jpeg</mediaType>
                                 <presentOnServer>true</presentOnServer>
                                 <fileData>image1/data</fileData>
                             </file>''',
                 'getAlbumsCollectionContents-userAlbums':'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?><collectionContents start="0" hasMore="false" end="1"><collection type="album"><displayName>album1</displayName><ref>album1</ref><contents>album1/contents</contents></collection></collectionContents>''',
                 'getAlbumContents-album1':'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?><collectionContents start="0" hasMore="false" end="0"><file><displayName>image1.jpg</displayName><ref>image1</ref><size>3942294</size><lastModified>2010-09-18T10:19:16.000-07:00</lastModified><mediaType>image/jpeg</mediaType><presentOnServer>true</presentOnServer><fileData>image1/data</fileData></file></collectionContents>'''}