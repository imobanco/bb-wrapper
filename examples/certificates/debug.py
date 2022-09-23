import os
import ssl
import certifi
from urllib.request import urlopen

openssl_dir, openssl_cafile = os.path.split(
    ssl.get_default_verify_paths().openssl_cafile
)
# no content in this folder
os.listdir(openssl_dir)
# non existent file
print(os.path.exists(os.path.join(openssl_dir, openssl_cafile)))


cafile = certifi.where()
context = ssl.create_default_context(cafile=cafile)

request = "https://example.com"
urlopen(request, context=context)
