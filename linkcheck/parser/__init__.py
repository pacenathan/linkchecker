# Copyright (C) 2000-2014 Bastian Kleineidam
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
"""
Main functions for link parsing
"""
from .. import strformat, url as urlutil
from ..htmlutil import linkparse
from ..bookmarks import firefox


def parse_url(url_data):
    """Parse a URL."""

    url_no_anchor = url_data.url_without_anchor()
    found = url_data.aggregate.anchor_cache.get(url_no_anchor, 'url')
    if found is not None:
        return

    url_data.aggregate.anchor_cache.put(url_no_anchor, 'url', url_no_anchor)

    if url_data.is_directory():
        # both ftp and file links represent directories as HTML data
        key = "html"
    elif (
        url_data.is_file()
        and firefox.has_sqlite
        and firefox.extension.search(url_data.url)
    ):
        key = "firefox"
    elif url_data.scheme == "itms-services":
        key = "itms_services"
    else:
        # determine parse routine according to content types
        mime = url_data.content_type
        key = url_data.ContentMimetypes[mime]
    funcname = "parse_" + key
    if funcname in globals():
        globals()[funcname](url_data)
    else:
        url_data.aggregate.plugin_manager.run_parser_plugins(url_data, pagetype=key)


def parse_html(url_data):
    """Parse into HTML content and search for URLs to check.
    Found URLs are added to the URL queue.
    """
    linkparse.find_links(url_data.get_soup(), url_data.add_url, linkparse.LinkTags)


def parse_opera(url_data):
    """Parse an opera bookmark file."""
    from ..bookmarks.opera import parse_bookmark_data

    for url, name, lineno in parse_bookmark_data(url_data.get_content()):
        url_data.add_url(url, line=lineno, name=name)


def parse_chromium(url_data):
    """Parse a Chromium or Google Chrome bookmark file."""
    from ..bookmarks.chromium import parse_bookmark_data

    for url, name in parse_bookmark_data(url_data.get_content()):
        url_data.add_url(url, name=name)


def parse_safari(url_data):
    """Parse a Safari bookmark file."""
    from ..bookmarks.safari import parse_bookmark_data

    for url, name in parse_bookmark_data(url_data.get_raw_content()):
        url_data.add_url(url, name=name)


def parse_text(url_data):
    """Parse a text file with one url per line; comment and blank
    lines are ignored."""
    lineno = 0
    for line in url_data.get_content().splitlines():
        lineno += 1
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        url_data.add_url(line, line=lineno)


def parse_css(url_data):
    """
    Parse a CSS file for url() patterns.
    """
    lineno = 0
    linkfinder = linkparse.css_url_re.finditer
    strip_comments = linkparse.strip_c_comments
    for line in strip_comments(url_data.get_content()).splitlines():
        lineno += 1
        for mo in linkfinder(line):
            column = mo.start("url")
            url = strformat.unquote(mo.group("url").strip())
            url_data.add_url(url, line=lineno, column=column)


def parse_swf(url_data):
    """Parse a SWF file for URLs."""
    linkfinder = linkparse.swf_url_re.finditer
    for mo in linkfinder(url_data.get_raw_content()):
        # We're scraping binary data for anything that looks like an URL using
        # a regex that matches only ASCII characters.  Any non-ASCII characters
        # in the URL are expected to be %-encoded.
        url = mo.group().decode('ascii')
        url_data.add_url(url)


def parse_wml(url_data):
    """Parse into WML content and search for URLs to check.
    Found URLs are added to the URL queue.
    """
    linkparse.find_links(url_data.get_soup(), url_data.add_url, linkparse.WmlTags)


def parse_firefox(url_data):
    """Parse a Firefox3 bookmark file."""
    filename = url_data.get_os_filename()
    for url, name in firefox.parse_bookmark_file(filename):
        url_data.add_url(url, name=name)


def parse_itms_services(url_data):
    """Get "url" CGI parameter value as child URL."""
    query = url_data.urlparts[3]
    for k, v, sep in urlutil.parse_qsl(
        query, encoding=url_data.encoding, keep_blank_values=True
    ):
        if k == "url":
            url_data.add_url(v)
            break


from .sitemap import parse_sitemap, parse_sitemapindex  # noqa: F401
