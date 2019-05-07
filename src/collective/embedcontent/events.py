# -*- coding: utf-8 -*-
from plone.app.blob.field import BlobWrapper
from zipfile import  ZipFile
from plone.namedfile.utils import get_contenttype
import os
from BTrees.OOBTree import OOBTree

def generateUniqueIDForPackageFile(fileObj):
    return str(hash(fileObj))

def updateIndexFile(obj):
    top_level_files = [key for key in obj.zipTree.iterkeys() if not isinstance(obj.zipTree[key],OOBTree)]
    if not obj.index_file or obj.index_file not in top_level_files:
        html_files = [filename for filename in top_level_files if filename.endswith('html') or filename.endswith('htm') ]
        if 'index.html' in html_files:
            obj.index_file = 'index.html'
            return
        elif 'index.htm' in html_files:
            obj.index_file = 'index.htm'
            return
        elif html_files:
            obj.index_file = html_files[0]
        elif top_level_files:
            obj.index_file = top_level_files[0]

def afterContentCreated(obj, event):
    if obj.package_content:
        content_hash = generateUniqueIDForPackageFile(obj.package_content)
        setattr(obj,'contentHash',content_hash)
        zipTree = OOBTree()
        extract_package_content(zipTree, obj.package_content)
        setattr(obj, 'zipTree', zipTree)
        updateIndexFile(obj)

def afterContentModified(obj, event):
    if obj.package_content:
        new_hash = generateUniqueIDForPackageFile(obj.package_content)
        old_hash = getattr(obj,'contentHash',None)
        if new_hash == old_hash:
            return
        setattr(obj, 'contentHash', new_hash)
        zipTree = getattr(obj,'zipTree', OOBTree())
        zipTree.clear()
        extract_package_content(zipTree, obj.package_content)
        setattr(obj, 'zipTree', zipTree)
    else:
        setattr(obj, 'zipTree', OOBTree())
    updateIndexFile(obj)

def extract_package_content(root, zip_blob):
    """
        Extract package content into ZOB Tree
    """
    zipfile = ZipFile(zip_blob.open('r'))
    parent_dict = {}
    for path in sorted(zipfile.namelist()):
        if path.endswith('/'):
            # create directory
            path = path[:-1]
            foldername = path.split(os.sep)[-1]
            parent_folder_name = '/'.join(path.split(os.sep)[:-1])
            parent = parent_dict[parent_folder_name] if parent_folder_name in parent_dict else root
            parent.insert(foldername, OOBTree())
            parent_dict[path] = parent[foldername]
        else:
            # create file
            filename = path.split(os.sep)[-1]
            parent_folder_name = '/'.join(path.split(os.sep)[:-1])
            parent = parent_dict[parent_folder_name] if parent_folder_name in parent_dict else root
            data = zipfile.read(path)
            blob = BlobWrapper(get_contenttype(filename=filename))
            file_obj = blob.getBlob().open('w')
            file_obj.write(data)
            file_obj.close()
            blob.setFilename(filename)
            parent.insert(filename, blob)

