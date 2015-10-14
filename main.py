#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
from google.appengine.api import urlfetch


class MainHandler(webapp2.RequestHandler):
    def get(self):
        if "target_url" not in self.request.headers:
            return self.response

        headers_to_remove = {"Target-Url", "Host"}
        headers = {key: value for key, value in self.request.headers.items() if key not in headers_to_remove}
        if self.request.cookies:
            headers['Cookie'] = ';'.join(["%s=%s" % (key, value) for key, value in self.request.cookies.items()])

        if self.request.method == 'GET':
            r = urlfetch.fetch(self.request.headers["target_url"], headers=headers, follow_redirects=False)
            setup_response_info(r, self.response)
            self.response.body = r.content

        return self.response


def setup_response_info(incoming, outgoing):
    headers_to_keep = {'Content-Encoding', 'Content-Length'}
    for header in incoming.headers:
        if header not in headers_to_keep:
            outgoing.headers[header] = incoming.headers[header]
    outgoing.status = incoming.status_code


app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
