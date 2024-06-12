from google.cloud import storage

def upload_to_gcs(file, bucket_name, destination_blob_name, content_type):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_file(file, content_type=content_type)
    blob.make_public()
    return blob.public_url

