---
abbreviations:
  GCP: Google Cloud Platform
  GCS: Google Cloud Storage
  IAM: Identity and Access Management
---

# Administrator's Guide

This page describes how to administer a Frictionless Research Exchange (FRX) Challenge.

:::{tip} Work in progress!
This guide is currently under active development and presently resembles more of a collection of stubs and notes. If you would like to contribute to improving the documentation, then please see the [Contribution Guide](CONTRIBUTING.md).
:::

## Uploading data to a storage bucket

If your challenge requires access to a large dataset, then you can upload your dataset directly to a cloud storage bucket. The FRX Challenge platform supports using [Google Cloud Storage](https://cloud.google.com/storage/docs) for this purpose.

For a brief overview of cloud object storage, see the [2i2c docs – Cloud Object Storage](https://docs.2i2c.org/user/topics/data/object-storage/).

### Identity and Access Management (IAM)

You must have a Google account to authenticate with and the necessary permissions to access the bucket. Please contact your GCP project administrator to request access.

If you are using the [gcloud command-line tool](https://cloud.google.com/sdk/gcloud), authenticate with your Google account using the following command:

```bash
gcloud auth login
```

### Uploading data

The bucket name is provided by your GCP project administrator and is of the form

```bash
gs://my-bucket-name
```

You can upload data to the bucket using the [Google Cloud Console](https://console.cloud.google.com/storage/browser) or the [gcloud command-line](https://cloud.google.com/storage/docs/discover-object-storage-gcloud#upload_an_object_into_your_bucket) tool.

#### Using the gcloud command-line tool

Use the following command to synchronize a local directory with a bucket:

```bash
gcloud storage rsync -r /path/to/local/directory gs://my-bucket-name
```
