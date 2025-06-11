import os
import re
import sys
import time
import base64
import requests
from concurrent.futures import ThreadPoolExecutor

CHANNELS_URL = 'https://josh9456-myproxy.hf.space/playlist/channels'
PROXY_PREFIX = 'https://josh9456-myproxy.hf.space/watch/'
PREMIUM = re.compile(r'premium(\d+)/mono\.m3u8')

URL_TEMPLATES = [
    "https://nfsnew.newkso.ru/nfs/premium{num}/mono.m3u8",
    "https://windnew.newkso.ru/wind/premium{num}/mono.m3u8",
    "https://zekonew.newkso.ru/zeko/premium{num}/mono.m3u8",
    "https://dokko1new.newkso.ru/dokko1/premium{num}/mono.m3u8",
    "https://ddy6new.newkso.ru/ddy6/premium{num}/mono.m3u8"
]

# 1. Download channels.m3u8

def fetch_channels(dest='channels.m3u8'):
    r = requests.get(CHANNELS_URL, timeout=10)
    r.raise_for_status()
    with open(dest, 'wb') as f:
        f.write(r.content)
    print("✅ channels.m3u8 downloaded")

# 2. Decode all base64 URLs from tivimate and validate their {num} links

def validate_links(src='tivimate_playlist.m3u8', out='links.m3u8'):
    decoded = []
    with open(src) as f:
        for line in f:
            if line.strip().startswith(PROXY_PREFIX):
                try:
                    b64 = line.strip().split('/watch/')[1].split('.m3u8')[0]
                    url = base64.b64decode(b64).decode().strip()
                    decoded.append(url)
                except:
                    continue

    ids = {m.group(1) for u in decoded if (m := PREMIUM.search(u))}
    candidates = [t.format(num=i) for i in ids for t in URL_TEMPLATES]

    def check(url):
        headers = {'User-Agent': 'Mozilla/5.0'}
        for _ in range(3):
            try:
                r = requests.head(url, headers=headers, timeout=10)
                if r.status_code == 200:
                    return url
                if r.status_code == 429:
                    time.sleep(5)
                if r.status_code == 404:
                    return None
                r = requests.get(url, headers=headers, timeout=10)
                if r.status_code == 200:
                    return url
            except:
                return None
        return None

    valid = []
    with ThreadPoolExecutor(10) as pool:
        for result in pool.map(check, candidates):
            if result:
                valid.append(result)

    with open(out, 'w') as f:
        f.write('\n'.join(valid))
    print(f"✅ {len(valid)} validated URLs written to {out}")

# 3. Create a mapping from original stream → proxy link (no EXTINF)

def build_proxy_map(channels='channels.m3u8', valid_file='links.m3u8'):
    valid_links = set(open(valid_file).read().splitlines())
    lines = open(channels).read().splitlines()

    proxy_map = {}  # decoded original → proxy stream only
    for i in range(len(lines) - 1):
        if lines[i].startswith('#EXTINF'):
            proxy = lines[i + 1].strip()
            if '/watch/' in proxy:
                try:
                    b64 = proxy.split('/watch/')[1].split('.m3u8')[0]
                    decoded = base64.b64decode(b64).decode().strip()
                    if decoded in valid_links:
                        proxy_map[decoded] = proxy
                except:
                    continue
    print(f"✅ Proxy map built with {len(proxy_map)} entries")
    return proxy_map

# 4. Replace only the stream lines, keep #EXTINF as-is

def rewrite_streams_only(src='tivimate_playlist.m3u8', proxy_map=None):
    lines = open(src).read().splitlines()
    out = []
    i = 0
    replaced = 0
    while i < len(lines):
        line = lines[i]
        if line.startswith('#EXTINF') and i + 1 < len(lines):
            out.append(line)
            stream_line = lines[i + 1].strip()
            decoded = None
            if stream_line.startswith(PROXY_PREFIX):
                try:
                    b64 = stream_line.split('/watch/')[1].split('.m3u8')[0]
                    decoded = base64.b64decode(b64).decode().strip()
                except:
                    pass
            if decoded and decoded in proxy_map:
                out.append(proxy_map[decoded])
                replaced += 1
            else:
                out.append(stream_line)
            i += 2
        else:
            out.append(line)
            i += 1

    with open(src, 'w') as f:
        f.write('\n'.join(out) + '\n')
    print(f"✅ Updated {replaced} stream URLs with valid proxies")

if __name__ == '__main__':
    fetch_channels()
    validate_links()
    proxy_map = build_proxy_map()
    rewrite_streams_only(proxy_map=proxy_map)
    print("✅ Done.")
