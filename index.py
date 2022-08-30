from wrappers.google_wrapper import CreateService
from googleapiclient.http import MediaFileUpload
from wrappers.google_wrapper import uploadModelToGoogleDrive

fileName = "sample.png"
mimeType = "image/png"

uploadModelToGoogleDrive(
    fileName = fileName,
    mimeType = mimeType
)