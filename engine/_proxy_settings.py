# coding: utf-8

import os
import re
import zipfile
import sys


CUSTOM_CHROME_PROXY_EXTENSIONS_DIR = '/tmp/chrome-proxy-extensions'

manifest = """

{
    "version": "1.0.0",
    "manifest_version": 2,
    "name": "Chrome Proxy",
    "permissions": [
        "proxy",
        "tabs",
        "unlimitedStorage",
        "storage",
        "<all_urls>",
        "webRequest",
        "webRequestBlocking"
    ],
    "background": {
        "scripts": ["background.js"]
    },
    "minimum_chrome_version":"22.0.0"
}

"""

background = """

var config = {
        mode: "fixed_servers",
        rules: {
          singleProxy: {
            scheme: "http",
            host: "%proxy_host",
            port: parseInt(%proxy_port)
          },
          bypassList: ["foobar.com"]
        }
      };

chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

function callbackFn(details) {
    return {
        authCredentials: {
            username: "%username",
            password: "%password"
        }
    };
}

chrome.webRequest.onAuthRequired.addListener(
            callbackFn,
            {urls: ["<all_urls>"]},
            ['blocking']
);

"""


def get_chrome_proxy_extension(proxy):
    m = re.compile('([^:]+):([^\@]+)\@([\d\.]+):(\d+)').search(proxy)
    if m:
        # 提取代理的各项参数
        username = m.groups()[0]
        password = m.groups()[1]
        ip = m.groups()[2]
        port = m.groups()[3]
        # 创建一个定制Chrome代理扩展(zip文件)
        if not os.path.exists(CUSTOM_CHROME_PROXY_EXTENSIONS_DIR):
            os.mkdir(CUSTOM_CHROME_PROXY_EXTENSIONS_DIR)
        extension_file_path = os.path.join(CUSTOM_CHROME_PROXY_EXTENSIONS_DIR, '{}.zip'.format(proxy.replace(':', '_')))
        if not os.path.exists(extension_file_path):
            try:
                zf = zipfile.ZipFile(extension_file_path, mode='w')
                zf.writestr('manifest.json', manifest)
                background_content = background
                background_content = background_content.replace('%proxy_host', ip)
                background_content = background_content.replace('%proxy_port', port)
                background_content = background_content.replace('%username', username)
                background_content = background_content.replace('%password', password)
                zf.writestr('background.js', background_content)
                zf.close()
            except:
                print(sys.exc_info()[0])

        return extension_file_path
    else:
        raise Exception('Invalid proxy format. Should be username:password@ip:port')

