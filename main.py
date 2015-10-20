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
import re
from google.appengine.api import urlfetch


class MainHandler(webapp2.RequestHandler):
    def get_general(self, method):
        headers = self.setup_headers()
        r = urlfetch.fetch(self.request.headers["target_url"], headers=headers, method=method,
                           follow_redirects=False)
        self.setup_response_info(r, self.response)

        return r

    def get(self):
        r = self.get_general(urlfetch.GET)
        self.response.body = r.content
        return self.response

    def head(self):
        r = self.get_general(urlfetch.HEAD)
        if 'content-length' in r.headers:
            self.response.headers['source-content-length'] = r.headers['content-length']
        return self.response

    def post_general(self, method):
        headers = self.setup_headers()
        form_data = self.request.body
        r = urlfetch.fetch(self.request.headers["target_url"], headers=headers, method=method,
                           payload=form_data, follow_redirects=False)
        self.setup_response_info(r, self.response)
        self.response.body = r.content

    def post(self):
        self.post_general(urlfetch.POST)
        return self.response

    def put(self):
        self.post_general(urlfetch.PUT)
        return self.response

    def delete(self):
        r = self.get_general(urlfetch.DELETE)
        self.response.body = r.content

    def setup_headers(self):
        headers_to_remove = {"Target-Url", "Host", 'Content-Length'}
        headers = {key: value for key, value in self.request.headers.items() if key not in headers_to_remove}
        if self.request.cookies:
            headers['Cookie'] = ';'.join(["%s=%s" % (key, value) for key, value in self.request.cookies.items()])

        return headers

    def setup_response_info(self, incoming, outgoing):
        headers_to_keep = {'content-encoding', 'content-length'}
        for header in incoming.headers:
            if header not in headers_to_keep:
                if header == 'set-cookie':
                    for index, value in enumerate(incoming.header_msg.getheaders(header)):
                        cookie_header = header + '-' + str(index)
                        outgoing.headers[cookie_header] = value
                else:
                    outgoing.headers[header] = incoming.headers[header]

        outgoing.status = incoming.status_code

        if 'location' in outgoing.headers and not outgoing.headers['location'].startswith('http'):
            location = outgoing.headers['location']
            target_url = self.request.headers['Target-Url']
            try:
                if location.startswith('/'):
                    outgoing.headers['location'] = re.search(r'https?://[^/]*', target_url).group() + location
                else:
                    outgoing.headers['location'] = re.search(r'https?://.*/', target_url).group() + location
            except AttributeError:
                pass


class HomeHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write("Hope cannot be blocked")

app = webapp2.WSGIApplication([
    ('/', HomeHandler),
    ('/hope/', MainHandler)
], debug=True)
