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
from __future__ import absolute_import

from django.test import TestCase
from ..fulcrum_importer import *
import inspect
from ..models import *

class FulcrumImporterTests(TestCase):

    def setUp(self):
        pass

    # def test_unzip(self):
    #     """File should be unzipped to a specified directory"""
    #     test_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    #     unzip_file(os.path.join(test_dir, 'unzipped_file'),
    #                os.path.join(test_dir,
    #                             os.path.join('sample_data','Fulcrum_Export.zip')))
    #     self.assertTrue(os.path.exists(os.path.join(test_dir,
    #                                                 os.path.join('unzipped_file',
    #                                                              'test2'))))

    def test_find_media_keys_from_urls(self):
        """

        Returns:Given a geojson containing a Fulcrum API media url,
        a json should be returned with those keys and types.
        This assumes that 'photos', 'videos', or 'audio' is in the media url.
        The test proves that even if the key is arbitrary the url will prove valid.

        """
        example_layer = Layer.objects.create(layer_name="example", layer_uid="unique")
        expected_keymap = {'pics': 'photos','vids': 'videos','sounds': 'audio'}
        bad_geojson = {'type': 'feature',
                       'properties': {'pics_url': '',
                                      'vids_url': 'https://api.fulcrumapp.com/api/v2/videos',
                                      'sounds_url': ''}}
        good_geojson = {'type': 'feature',
                       'properties': {'pics_url': 'https://api.fulcrumapp.com/api/v2/photos',
                                      'vids_url': 'https://api.fulcrumapp.com/api/v2/videos',
                                      'sounds_url': 'https://api.fulcrumapp.com/api/v2/audio'}}
        self.assertNotEqual(find_media_keys([bad_geojson], example_layer), expected_keymap)
        self.assertEqual(find_media_keys([good_geojson], example_layer), expected_keymap)

    def test_layer_media_keys_update(self):
        example_layer = Layer.objects.create(layer_name="example", layer_uid="unique")
        expected_keymap = {'pics': 'photos','vids': 'videos','sounds': 'audio'}
        bad_geojson = {'type': 'feature',
                       'properties': {'pics_url': '',
                                      'vids_url': 'https://api.fulcrumapp.com/api/v2/videos',
                                      'sounds_url': ''}}
        good_geojson = {'type': 'feature',
                       'properties': {'pics_url': 'https://api.fulcrumapp.com/api/v2/photos',
                                      'vids_url': 'https://api.fulcrumapp.com/api/v2/videos',
                                      'sounds_url': 'https://api.fulcrumapp.com/api/v2/audio'}}
        example_layer.layer_media_keys = find_media_keys([bad_geojson], example_layer)
        example_layer.save()
        self.assertNotEqual(example_layer.layer_media_keys, "{}")
        example_layer.layer_media_keys = find_media_keys([good_geojson], example_layer)
        example_layer.save()
        self.assertEqual(example_layer.layer_media_keys, expected_keymap)