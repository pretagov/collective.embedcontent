# -*- coding: utf-8 -*-
from plone.app.blob.field import BlobWrapper
from zipfile import  ZipFile
from plone.namedfile.utils import get_contenttype
import os
from BTrees.OOBTree import OOBTree

def afterContentCreated(obj, event):
    if obj.package_content:
        content_hash = str(hash(obj.package_content))
        setattr(obj,'contentHash',content_hash)
        zipTree = OOBTree()
        extract_package_content(zipTree, obj.package_content)
        setattr(obj, 'zipTree', zipTree)

def afterContentModified(obj, event):
    if obj.package_content:
        new_hash = str(hash(obj.package_content))
        old_hash = getattr(obj,'contentHash',None)
        if new_hash == old_hash:
            return
        setattr(obj, 'contentHash', new_hash)
        zipTree = getattr(obj,'zipTree', OOBTree())
        zipTree.clear()
        extract_package_content(zipTree, obj.package_content)
        setattr(obj, 'zipTree', zipTree)

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

