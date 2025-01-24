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

## Authoring website content

The FRX Challenge platform is built on top of the [Django](https://djangoproject.com/) framework. You can author content for your challenge website using Markdown and HTML.

### Django Admin

If your website user account has admin permissions, then the Django Admin interface is available at `https://<challenge-website-name>/admin`. Please contact your Django administrator if you require access.

Under the `Web > Pages` section, you can create and edit multiple pages using the Django Admin interface.

:::{image} images/admin-pages.png
:alt: Django Admin interface
:::

**Pages**
: The `Pages` section contains the necessary fields to author pages on the website.

    title _(string)_
    : The title of the page.

    slug _(string)_
    : Slug used to refer to the page's URL.

    Navbar order _(integer)_:
    : Ordering of this page on the navbar. Leave unset to hide from navbar

    Is home _(boolean)_
    : Use current page as the home page. Only one page can have this enabled at any given time.

    Mimetype _(TextChoices)_
    : Mimetype used to render the page.

        HTML _(text/html)_
        : HTML content.

        Markdown _(text/markdown)_
        : Markdown content.

    Content _(text)_
    : The content of the page.

    Header content _(text)_
    : Content to be displayed in the header of the page.

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
