#!/usr/bin/env python
# -*- coding: utf-8 -*-
import dropbox
import ffmpegWebcam
import time


class TransferData:
    def __init__(self, access_token):
        self.access_token = access_token

    def upload_file(self, file_from=None, file_to=None):
        """upload a file to Dropbox using API v2
        """
        dbx = dropbox.Dropbox(self.access_token)
        # files_upload(f, path, mode=WriteMode('add', None), autorename=False, client_modified=None, mute=False)

        with open(file_from, 'rb') as f:
            dbx.files_upload(f, file_to)


def upload():
    access_token = 'icphewd7JfAAAAAAAAAAFmisq8oRnWgZxL3y_FVU9XE_Ytee-BhRNyqe6Uo96vz4'
    transferData = TransferData(access_token)
    filenamedrop = ffmpegWebcam.recordfromwebcam()
    today = time.strftime('%d-%m-%Y')
    file_from = 'videos/' + today + '/' + filenamedrop
    file_to = '/Recordings/' + filenamedrop  # The full path to upload the file to, including the file name
    # API v2
    transferData.upload_file(file_from, file_to)
