# Copyright 2016, RadiantBlue Technologies, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import unicode_literals

from django.db import models
from django.core.files.storage import FileSystemStorage
from django.conf import settings

try:
    fs = FileSystemStorage(location=settings.FILESERVICE_CONFIG.get('store_dir'))
except AttributeError:
    fs = FileSystemStorage(location=settings.MEDIA_ROOT)


def get_asset_name(instance, filename):
    return './{}.{}'.format(instance.asset_uid, get_type_extension(instance.asset_type))


def get_type_extension(type):
    asset_types = {'photos': 'jpg', 'videos': 'mp4', 'audio': 'm4a'}
    if asset_types.get(type):
        return asset_types.get(type)
    else:
        return None


class Asset(models.Model):
    asset_uid = models.CharField(max_length=100, primary_key=True)
    asset_type = models.CharField(max_length=100)
    asset_data = models.FileField(storage=fs, upload_to=get_asset_name)


class Layer(models.Model):
    layer_name = models.CharField(max_length=100)
    layer_uid = models.CharField(max_length=100)
    layer_date = models.IntegerField(default=0)
    layer_media_keys = models.CharField(max_length=2000,default="{}")

    class Meta:
        unique_together = (("layer_name", "layer_uid"),)


class Feature(models.Model):
    feature_uid = models.CharField(max_length=100)
    feature_version = models.IntegerField(default=0)
    layer = models.ForeignKey(Layer,on_delete=models.CASCADE, default="")
    feature_data = models.CharField(max_length=10000)

    class Meta:
        unique_together = (("feature_uid", "feature_version"),)


class Links(models.Model):
    asset = models.ForeignKey(Asset,on_delete=models.CASCADE,default="")
    feature = models.ForeignKey(Feature, on_delete=models.CASCADE, default="")


class S3Sync(models.Model):
    s3_filename = models.CharField(max_length=500, primary_key=True)


class S3Credential(models.Model):
    s3_name = models.CharField(max_length=100)
    s3_key = models.CharField(max_length=100)
    s3_secret = models.CharField(max_length=255)
    s3_gpg = models.CharField(max_length=255)

    class Meta:
        unique_together = (("s3_key", "s3_secret"),)

    def __unicode__(self):
       return "{}({})".format(self.s3_name, self.s3_key)


class S3Bucket(models.Model):
    s3_bucket = models.CharField(max_length=511)
    s3_credential = models.ForeignKey(S3Credential, on_delete=models.CASCADE, default="")

    def __unicode__(self):
       return self.s3_bucket


class FulcrumApi(models.Model):
    fulcrum_api_name = models.CharField(max_length=100)
    fulcrum_api_key = models.CharField(max_length=255, default="", primary_key=True)

    def __unicode__(self):
       return self.fulcrum_api_name

class Filters(models.Model):
    filter_name = models.CharField(max_length=255)
    filter_active = models.BooleanField(default=False)
