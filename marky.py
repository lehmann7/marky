#!/usr/bin/env python3
# -*- coding: utf-8 -*-

########################################################################
# marky Markdown Preprocessor ###########################################
########################################################################

# Quick Make Example Project
############################
#
#  > mkdir project
#  > cp /path/to/marky.py project
#  > cd project
#  > chmod +x marky.py
#  > ./marky.py --init
#  > make scan html-all pdf-all httpd
#
# Open: project/pdf/*.pdf
# Goto: http://localhost:8000/

########################################################################

import sys
import argparse
import glob
import os
import base64
import yaml

########################################################################

if not sys.version_info.major == 3 and sys.version_info.minor >= 6:
	try:
		raise ValueError("marky requires Python 3.6 or higher.")
	except Exception as ex:
		print("# ERROR", type(ex), str(ex))
		sys.exit(1)

########################################################################

_MARKY_VERSION = (0, 9)

########################################################################
# SECTION IS AUTO-PACKAGED USING ./marky.py --pack --force
########################################################################
###!!!:::marky_pack_data:::!!!###
pack_Makefile = '''
IyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMj
IyMjIyMjIyMjIyMjIyMjIyMjCgouUEhPTlk6IGhlbHAKaGVscDoKCSMgbWFya3kgREVQRU5E
RU5DSUVTCgkjIyMjIyMjIyMjIyMjIyMjIyMjIwoJIyAqIHBhbmRvYyA+PSAyLjEwCgkjICog
cGlwIGluc3RhbGwgcGFuZG9jLWZpZ25vcwoJIyAqIHBpcCBpbnN0YWxsIHBhbmRvYy1lcW5v
cwoJIyAqIHBpcCBpbnN0YWxsIHBhbmRvYy1zZWNub3MKCSMgKiBwaXAgaW5zdGFsbCBwYW5k
b2MtdGFibGVub3MKCSMgKiBwaXAgaW5zdGFsbCBwYW5kb2MteG5vcwoJIyAqIHBpcCBpbnN0
YWxsIHB5eWFtbAoJIwoJIyBBVFRFTlRJT04KCSMjIyMjIyMjIyMjCgkjIEFsbCBmaWxlcyBp
biBgYnVpbGQvKi5tZGAgYW5kIGBodG1sLyouaHRtbGAgYXJlIGF1dG8tZ2VuZXJhdGVkIQoJ
IyBVc2VyIGZpbGVzIGAqLm1kYCBoYXZlIHRvIGJlIHBsYWNlZCBpbiBgbWQvKi5tZGAhCgkj
IGBtYWtlIGNsZWFuYCBkZWxldGVzIGFsbCBmaWxlcyBpbiBgYnVpbGQvYCwgYGh0bWwvYCBh
bmQgYHBkZi9gLgoJIwoJIyBtYXJreSBVVElMUwoJIyMjIyMjIyMjIyMjIwoJIyAqIG1ha2Ug
aGVscCAgICAgICAgICAgIC0gc2hvdyB0aGlzICpIZWxwIE1lc3NhZ2UqCgkjICogbWFrZSB0
cmVlICAgICAgICAgICAgLSBzaG93IHRoZSAqUHJvamVjdCBUcmVlKgoJIyAqIG1ha2UgaHR0
cGQgICAgICAgICAgIC0gcnVuIHB5dGhvbiAtbSBodHRwZC5zZXJ2ZXIgaW4gYGh0bWwvYAoJ
IyAqIG1ha2UgY2xlYW4gICAgICAgICAgIC0gZGVsZXRlOiBgYnVpbGQvKmAsIGBodG1sLypg
LCBgcGRmLypgCgkjICogbWFrZSBzY2FuICAgICAgICAgICAgLSBidWlsZCBtYWtlIGRlcHM6
IGBidWlsZC8qLm1ha2VgCgkjICogbWFrZSBsaXN0ICAgICAgICAgICAgLSBsaXN0IGFsbCBz
Y2FubmVkIGZpbGVzIGFuZCB0YXJnZXRzCgkjCgkjIG1hcmt5IEJVSUxEIEFMTAoJIyMjIyMj
IyMjIyMjIyMjIyMKCSMgKiBtYWtlIGJ1aWxkICAgICAgICAgICAtPiBgYnVpbGQvKi57aHRt
bCxwZGZ9Lm1kYAoJIyAqIG1ha2UgdGV4ICAgICAgICAgICAgIC0+IGBidWlsZC8qLnRleGAK
CSMgKiBtYWtlIGh0bWwgICAgICAgICAgICAtPiBgaHRtbC8qLmh0bWxgCgkjICogbWFrZSBw
ZGYgICAgICAgICAgICAgLT4gYHBkZi8qLnBkZmAKCSMgKiBtYWtlIGFsbCAgICAgICAgICAg
ICAtPiBgaHRtbC8qLmh0bWxgLCBgcGRmLyoucGRmYAoJIwoJIyBtYXJreSBCVUlMRCBGSUxF
CgkjIyMjIyMjIyMjIyMjIyMjIyMKCSMgKiBtYWtlIGJ1aWxkL2ZpbGUgICAgICAtPiBgYnVp
bGQvZmlsZS57aHRtbCxwZGZ9Lm1kYAoJIyAqIG1ha2UgYnVpbGQvZmlsZS50ZXggIC0+IGBi
dWlsZC9maWxlLnRleGAKCSMgKiBtYWtlIGh0bWwvZmlsZSAgICAgICAtPiBgaHRtbC9maWxl
Lmh0bWxgCgkjICogbWFrZSBwZGYvZmlsZSAgICAgICAgLT4gYHBkZi9wZGYuaHRtbGAKCSMK
CSMgRVhBTVBMRQoJIyMjIyMjIyMjCgkjIDEuIHJ1biBgbWFrZSBzY2FuIGh0bWwvZmlsZS5o
dG1sIGh0dHBkYDoKCSMgICAgKiBnZW5lcmF0ZSBgYnVpbGQvZmlsZS5tYWtlYAoJIyAgICAq
IHRyYW5zZm9ybSBgbWQvZmlsZS5tZGAgLT4gYGh0bWwvZmlsZS5odG1sYAoJIyAgICAqIHN0
YXJ0IGEgcHl0aG9uIGh0dHBkIHNlcnZlciBpbiBgaHRtbGAKCSMgMi4gcnVuIGBtYWtlIHNj
YW4gcGRmL2ZpbGUucGRmYAoJIyAgICAqIGdlbmVyYXRlIGBidWlsZC9maWxlLm1ha2VgCgkj
ICAgICogdHJhbnNmb3JtIGBtZC9maWxlLm1kYCAtPiBgcGRmL2ZpbGUucGRmYAoJIwoKLlBI
T05ZOiB0cmVlCnRyZWU6CgkjIFBST0pFQ1QgVFJFRQoJIyMjIyMjIyMjIyMjIyMKCSMgPHdv
cmtpbmdfZGlyPgoJIyB8LSBtYXJreS5weSAgICAgICAgICAgIC0gbWFya3kgZXhlY3V0YWJs
ZQoJIyB8LSBNYWtlZmlsZSAgICAgICAgKCopIC0gbWFya3kgTWFrZWZpbGUKCSMgfC0gcGFu
ZG9jLXJ1biAgICAgICgqKSAtIHBhbmRvYyB3cmFwcGVyCgkjIHwtIG1kLyAgICAgICAgICAg
ICAoKikgLSB1c2VyIE1hcmtkb3duIGRpcgoJIyB8ICB8LSAqLm1kICAgICAgICAgKCopIC0g
dXNlciBNYXJrZG93biB0ZXh0CgkjIHwtIGRhdGEvICAgICAgICAgICAoKikgLSB1c2VyIGRh
dGEgZGlyCgkjIHwgIHwtICouKiAgICAgICAgICAgICAgICB1c2VyIGRhdGEgZmlsZXMKCSMg
fC0gYnVpbGQvICAgICAgICAgICgqKSAtIGJ1aWxkIE1hcmtkb3duIGRpcgoJIyB8ICB8LSAq
LnB5ICAgICAgICAgKCopIC0gTWFya2Rvd24gbWFya3kgY29kZQoJIyB8ICB8LSAqLm1ha2Ug
ICAgICAgKCopIC0gTWFrZWZpbGUgcnVsZXMKCSMgfCAgfC0gKi5odG1sLm1kICAgICgqKSAt
IE1hcmtkb3duIGZvciBodG1sIGZvcm1hdAoJIyB8ICB8LSAqLnBkZi5tZCAgICAgKCopIC0g
TWFya2Rvd24gZm9yIHBkZiBmb3JtYXQKCSMgfC0gaHRtbC8qLmh0bWwgICAgICgqKSAtIHJl
bmRlcmVkIGh0bWwgZGlyCgkjIHwtIHBkZi8qLnBkZiAgICAgICAoKikgLSByZW5kZXJlZCBw
ZGYgZGlyCgkjCgkjICgqKSBkaXJlY3Rvcmllcy9maWxlcyBhcmUgYXV0by1nZW5lcmF0ZWQg
dXNpbmcKCSMgICAgYC4vbWFya3kucHkgLS1pbml0YCBhbmQgYG1ha2Ugc2NhbsK0CgkjCgou
UEhPTlk6IGNsZWFuCmNsZWFuOgoJcm0gLXJmIC4vYnVpbGQvKiAuL2h0bWwvKiAuL3BkZi8q
CgouUEhPTlk6IGh0dHBkCmh0dHBkOgoJY2QgaHRtbCAmJiBweXRob24gLW0gaHR0cC5zZXJ2
ZXIKCi5QSE9OWTogc2NhbgpzY2FuOgoJLi9tYXJreS5weSAtLXNjYW4KCiMjIyMjIyMjIyMj
IyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMj
IyMjIyMjIwoKYWxsX21kOj0KYWxsX2J1aWxkOj0KYWxsX2h0bWw6PQphbGxfcGRmOj0KYWxs
X3RleDo9CgotaW5jbHVkZSBidWlsZC8qLm1ha2UgYnVpbGQvKiovKi5tYWtlCgojIyMjIyMj
IyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMj
IyMjIyMjIyMjIyMKCi5QSE9OWTogbGluawpidWlsZDogJChhbGxfYnVpbGQpCgouUEhPTlk6
IGh0bWwKaHRtbDogJChhbGxfaHRtbCkKCi5QSE9OWTogcGRmCnBkZjogJChhbGxfcGRmKQoK
LlBIT05ZOiB0ZXgKdGV4OiAkKGFsbF90ZXgpCgouUEhPTlk6IGFsbAphbGw6IGh0bWwgcGRm
CgouUEhPTlk6IGxpc3QKbGlzdDoKCSMgbWFya3kgVEFSR0VUUwoJIyMjIyMjIyMjIyMjIyMj
CgkjICogYG1ha2Ugc2NhbmAgLS0gRklMRVM6JChhbGxfbWQpCgkjICogYG1ha2UgYnVpbGRg
IC0tIGBtYWtlJChhbGxfYnVpbGQpYAoJIyAqIGBtYWtlIGh0bWxgIC0tIGBtYWtlJChhbGxf
aHRtbClgCgkjICogYG1ha2UgcGRmYCAtLSBgbWFrZSQoYWxsX3BkZilgCgkjICogYG1ha2Ug
dGV4YCAtLSBgbWFrZSQoYWxsX3RleClgCgkjCg==
'''
pack_pandoc_run = '''
IyEvYmluL2Jhc2gKClsgJCMgPT0gMCBdICYmIGVjaG8gIiIiCiMgVXNhZ2U6ICQwOiA8Rk9S
TUFUPiA8SU5GSUxFPiA8T1VURklMRT4KIyBFeGFtcGxlOgojICQwIGh0bWwgYnVpbGQvZmls
ZS5odG1sLm1kIGh0bWwvZmlsZS5odG1sCiMgJDAgcGRmIGJ1aWxkL2ZpbGUucGRmLm1kIHBk
Zi9maWxlLnBkZgoiIiIgJiYgZXhpdCAxCgpQQU5ET0M9cGFuZG9jCgpNREVYVD1cCmFsbF9z
eW1ib2xzX2VzY2FwYWJsZStcCmludHJhd29yZF91bmRlcnNjb3JlcytcCmVzY2FwZWRfbGlu
ZV9icmVha3MrXApzcGFjZV9pbl9hdHhfaGVhZGVyK1wKbGlzdHNfd2l0aG91dF9wcmVjZWRp
bmdfYmxhbmtsaW5lK1wKaW5saW5lX2NvZGVfYXR0cmlidXRlcytcCnN0cmlrZW91dCtcCnlh
bWxfbWV0YWRhdGFfYmxvY2srXApwaXBlX3RhYmxlcytcCmxpbmVfYmxvY2tzK1wKaW1wbGlj
aXRfZmlndXJlcytcCmFiYnJldmlhdGlvbnMrXAppbmxpbmVfbm90ZXMKClBET1BUPSIiIgot
LXRhYmxlLW9mLWNvbnRlbnRzCi0tbnVtYmVyLXNlY3Rpb25zCiIiIgoKaWYgWyAkMSA9PSBo
dG1sIF0gOyB0aGVuCiRQQU5ET0MgIiQyIiBcCi0tZmlsdGVyIHBhbmRvYy14bm9zIFwKLS1j
aXRlcHJvYyBcCi0tZnJvbT1tYXJrZG93bityYXdfaHRtbCskTURFWFQgXAotLXRvPWh0bWw1
IFwKLS1zZWxmLWNvbnRhaW5lZCBcCi0tb3V0cHV0PSIkMyIgXAotLXJlc291cmNlLXBhdGg9
Ii4vYnVpbGQvIiBcCiRQRE9QVApmaQoKaWYgWyAkMSA9PSBwZGYgXSA7IHRoZW4KJFBBTkRP
QyAiJDIiIFwKLS1maWx0ZXIgcGFuZG9jLXhub3MgXAotLWNpdGVwcm9jIFwKLS1mcm9tPW1h
cmtkb3duK3Jhd190ZXgrJE1ERVhUIFwKLS10bz1sYXRleCBcCi0tb3V0cHV0PSIkMyIgXAot
LXJlc291cmNlLXBhdGg9Ii4vYnVpbGQvIiBcCi0tcGRmLWVuZ2luZT14ZWxhdGV4IFwKJFBE
T1BUCmZpCgppZiBbICQxID09IHRleCBdIDsgdGhlbgokUEFORE9DICIkMiIgXAotLWZpbHRl
ciBwYW5kb2MteG5vcyBcCi0tY2l0ZXByb2MgXAotLWZyb209bWFya2Rvd24rcmF3X3RleCsk
TURFWFQgXAotLXRvPWxhdGV4IFwKLS1vdXRwdXQ9IiQzIiBcCi0tcmVzb3VyY2UtcGF0aD0i
Li9idWlsZC8iIFwKJFBET1BUCmZpCg==
'''
pack_marky_md = '''
LS0tCnRpdGxlOiAiYG1hcmt5YCBEb2N1bWVudGF0aW9uICIKdGl0bGUtLXBkZjogIi0tIGBw
ZGZgIgp0aXRsZS0taHRtbDogIi0tIGBodG1sYCIKYmlibGlvZ3JhcGh5OiBkYXRhL21hcmt5
LmJpYgpoZWFkZXItaW5jbHVkZXMtLXBkZjogPgogICBcaHlwZXJzZXR1cHtjb2xvcmxpbmtz
PWZhbHNlLAogICBhbGxib3JkZXJjb2xvcnM9ezAgMCAwfSwKICAgcGRmYm9yZGVyc3R5bGU9
ey9TL1UvVyAxfX0KaGVhZGVyLWluY2x1ZGVzLS1odG1sOiA+CiAgIDxzdHlsZT4qIHsgYm94
LXNpemluZzogYm9yZGVyLWJveDsgfTwvc3R5bGU+Cnhub3MtY2xldmVyZWY6IHRydWUKeG5v
cy1jYXBpdGFsaXNlOiB0cnVlCmZvbnRzaXplOiAxMXB0CgotLS0KPD8KY29sID0gZm10Y29k
ZShodG1sPSI8c3BhbiBzdHlsZT0nY29sb3I6e2N9Jz57dH08L3NwYW4+IiwgcGRmPSJ7dH0i
KQpkZWYgdGV4dF9wcm9jKGNtZCwgY3JvcD1UcnVlKToKCWltcG9ydCBzdWJwcm9jZXNzIGFz
IHNwCgl0ZXh0ID0gIiIKCWZvciBpIGluIHNwLmNoZWNrX291dHB1dChjbWQuc3BsaXQoKSku
ZGVjb2RlKCJ1dGYtOCIpLnNwbGl0KCJcbiIpOgoJCWlmIG5vdCBjcm9wOgoJCQl0ZXh0ICs9
IGkgKyAiXG4iCgkJZWxpZiBpLnN0YXJ0c3dpdGgoIiMgIik6CgkJCXRleHQgKz0gaVsyOl0g
KyAiXG4iCgkJZWxpZiBpID09ICIjIjoKCQkJdGV4dCArPSAiXG4iCgkJZWxpZiBpLnN0YXJ0
c3dpdGgoIiMiKToKCQkJdGV4dCArPSBpICsgIlxuIgoJcmV0dXJuIHRleHQKdmVyc2lvbiA9
IHRleHRfcHJvYygicHl0aG9uIG1hcmt5LnB5IC0tdmVyc2lvbiIsIGNyb3A9RmFsc2UpLnN0
cmlwKCkKPz4KLS0tCgo+ICoqQWJzdHJhY3QqKiAtLSBgbWFya3lgIGlzIGEgcHJlcHJvY2Vz
c29yIHdpdGggYW4gZWFzeSBhbmQgaW50dWl0aXZlCj4gc3ludGF4IGZvciBleGVjdXRpb24g
b2YgZW1iZWRkZWQge3tjb2wodD0icHlob24iLGM9ImJsdWUiKX19IGNvZGUgZHVyaW5nIHJl
bmRlcmluZwo+IGBodG1sYCBhbmQgYHBkZmAgZG9jdW1lbnRzIGZyb20gTWFya2Rvd24gdGV4
dC4KPiBUaGlzIGRvY3VtZW50IGlzIGNyZWF0ZWQgdXNpbmcgYG1hcmt5YCwgdmVyc2lvbiAq
e3t2ZXJzaW9ufX0qLgo+IEZvciBtb3JlIGluZm9ybWF0aW9uIHBsZWFzZSByZWZlciB0byB0
aGUKPiBbYG1hcmt5YCByZXBvc2l0b3J5XShodHRwczovL2dpdGh1Yi5jb20vbGVobWFubjcv
bWFya3kpLgoKLS0tCgojIGBtYXJreWAgRHluYW1pYyBNYXJrZG93bgoKYG1hcmt5YCBpcyBh
IE1hcmtkb3duIHByZXByb2Nlc3NvciB3aGljaCB0cmFuc2Zvcm1zIGEgTWFya2Rvd24gZG9j
dW1lbnQKdXNpbmcgcHl0aG9uLiBgbWFya3lgIGltcGxlbWVudHMgdGhyZWUgc3RhdGVtZW50
cyB3aXRoIGV4dHJlbWVseSBlYXN5CmFuZCBpbnR1aXRpdmUgc3ludGF4LCB3aGljaCBhcmUg
ZW1iZWRkZWQgZGlyZWN0bHkgaW4gdGhlIE1hcmtkb3duIHRleHQ6CgoxLiBgPFw/Li4uP1w+
YDogUHl0aG9uIGNvZGUgYmxvY2suCjIuIGB7XHsuLi59XH1gOiBgZmAtc3RyaW5nIG91dHB1
dCBpbnRvIE1hcmtkb3duLgozLiBgX19fKClgOiBGdW5jdGlvbiBmb3Igb3V0cHV0IGludG8g
TWFya2Rvd24uCgpVc2luZyBgPFw/Li4uP1w+YCBhbmQgYHtcey4uLn1cfWAgcHl0aG9uIHBy
b2Nlc3NpbmcgYW5kIGBmYC1zdHJpbmcgb3V0cHV0CmlzIGVtYmVkZGVkIGRpcmVjdGx5IGlu
c2lkZSB0aGUgTWFya2Rvd24gdGV4dC4gVXNpbmcgdGhlIGBfX18oKWAKZnVuY3Rpb24gdGV4
dCBpcyBnZW5lcmF0ZWQgZnJvbSBweXRob24gYWxnb3JpdGhtcyBhbmQKZHluYW1pY2FsbHkg
aW5zZXJ0ZWQgaW50byB0aGUgcmVzdWx0aW5nIE1hcmtkb3duLgoKIyBIb3cgZG9lcyBgbWFy
a3lgIHdvcmsgaW50ZXJuYWxseT8KCmBtYXJreWAgdXNlcyBhbiBleHRyZW1lbHkgc2ltcGxl
IG1lY2hhbmlzbSBmb3IgZ2VuZXJhdGluZyBhIHB5dGhvbiBwcm9ncmFtbQpmcm9tIHRoZSBN
YXJrZG93biB0ZXh0LiBVc2luZyB0aGUgYDxcPy4uLj9cPmAgYW5kIGB7XHsuLi59XH1gIHN0
YXRlbWVudCwKUHl0aG9uIGNvZGUgaXMgZW1iZWRkZWQgaW50byB0aGUgTWFya2Rvd24gdGV4
dCBhbmQgdHJhbnNsYXRlZCBpbnRvIGEgc2VyaWVzCm9mIGNhbGxzIHRvIHRoZSBgX19fKClg
IGZ1bmN0aW9uIHVzaW5nIGBmYC1zdHJpbmdzIGFzIGFyZ3VtZW50cywgd2hlcmUKcHl0aG9u
IHZhcmlhYmxlcyBhcmUgcmVmZXJlbmNlZC4gVGhpcyByZXN1bHRzIGludG8gYSBweXRob24g
cHJvZ3JhbQp3aGljaCBjYW4gZ2VuZXJhdGUgTWFya2Rvd24gdGV4dCBhbGdvcml0aG1pY2Fs
bHkuCgojIyMjIEV4YW1wbGU6IGBtZC9maWxlLm1kYCB7LX0KYGBgcGhwCiogVGhpcyBpcyB7
Zmlyc3R9LiA8XD8KeCA9IDEgIyB0aGlzIGlzIGNvZGUKZm9yIGkgaW4gcmFuZ2UoMyk6Cglp
ZiB4OgoJCT9cPgp7XHtpKzF9XH0uIFRoZSB2YWx1ZSBpcyB7XHtce3h9XH1cfS4KPFw/Cgll
bHNlOgoJCT9cPntce2krMX1cfS4gVGhlIHZhbHVlIGlzIHplcm8uCjxcPwoJeCA9IDAKP1w+
KiBUaGlzIGlzIGxhc3QuCmBgYApUaGUgZmlsZSBwcm9kdWNlcyB0aGUgZm9sbG93aW5nIE1h
cmtkb3duIG91dHB1dC4KCiMjIyMgT3V0cHV0OiBNYXJrZG93biB7LX0KYGBgYmFzaAoqIFRo
aXMgaXMge2ZpcnN0fS4KMS4gVGhlIHZhbHVlIGlzIHsxfS4KMi4gVGhlIHZhbHVlIGlzIHpl
cm8uCjMuIFRoZSB2YWx1ZSBpcyB6ZXJvLgoqIFRoaXMgaXMgbGFzdC4KYGBgCgpgbWFya3lg
IHRyYW5zZm9ybXMgdGhlIE1hcmtkb3duIGludG8gUHl0aG9uIHNvdXJjZSBjb2RlLgpFeGVj
dXRpb24gb2YgdGhlIFB5dGhvbiBzb3VyY2UgY29kZSB5aWVsZHMgdGhlIG5ldyBNYXJrZG93
biB0ZXh0LgoKIyMjIyBPdXRwdXQ6IGBidWlsZC9maWxlLnB5YCB7LX0KYGBgcHl0aG9uCl9f
XyhyZiIiIiogVGhpcyBpcyB7XHtmaXJzdH1cfS4gIiIiLCBfX18pOwp4ID0gMSAjIHRoaXMg
aXMgY29kZQpmb3IgaSBpbiByYW5nZSgzKToKCWlmIHg6CgkJX19fKHJmIiIiCntpKzF9LiBU
aGUgdmFsdWUgaXMge1x7XHt4fVx9XH0uCiIiIiwgX19fKTsKCWVsc2U6CgkJX19fKHJmIiIi
e2krMX0uIFRoZSB2YWx1ZSBpcyB6ZXJvLgoiIiIsIF9fXyk7Cgl4ID0gMApfX18ocmYiIiIq
IFRoaXMgaXMgbGFzdC4KIiIiLCBfX18pOwpgYGAKCiMgUXVpY2sgU3RhcnQKCiMjIGBtYXJr
eWAgRGVwZW5kZW5jaWVzCgpgbWFya3lgIHVzZXMgW3BhbmRvY10oaHR0cHM6Ly93d3cucGFu
ZG9jLm9yZy8pIGZvciByZW5kZXJpbmcgYGh0bWxgIGFuZCBgcGRmYC4KCmBtYXJreWAgZGVw
ZW5kcyBvbiBgcGFuZG9jYCBhbmQgYHB5eWFtbGAuIGBwYW5kb2NgIGlzIHVzZWQgZm9yIHJl
bmRlcmluZwp0aGUgTWFya2Rvd24gaW50byBgaHRtbGAgYW5kIGBwZGZgLiBgcGFuZG9jYCBz
dXBwb3J0cyB2YXJpb3VzIE1hcmtkb3duCmV4dGVuc2lvbnMgYWxsb3dpbmcgZm9yIHNjaWVu
dGlmaWMgd3JpdGluZyB1c2luZyBlcXVhdGlvbnMsIGZpZ3VyZXMsCnRhYmxlcywgY2l0YXRp
b25zIGFuZCBjb3JyZXNwb25kaW5nIHJlZmVyZW5jaW5nIG1lY2hhbmlzbSBmb3IgdGhlIGxh
dHRlci4KYHB5eWFtbGAgaXMgdXNlZCBmb3IgcGFyc2luZyBtZXRhIGRhdGEgaW4gdGhlIGZy
b250IG1hdHRlciBvZiB0aGUKTWFya2Rvd24gdGV4dC4KCmBtYXJreWAgcmVuZGVycyB0aGUg
ZG9jdW1lbnRhdGlvbiB1c2luZyBgcGFuZG9jYCBpbnRvIGBodG1sYCBhbmQKYHBkZmAgYnkg
aW52b2tpbmcgYG1ha2UgYWxsYC4gYG1hcmt5YCByZXF1aXJlcwppbnN0YWxsaW5nIHRoZSBk
ZXBlbmRlbmNpZXMgYHB5dGhvbi1weXlhbWxgLCBgcGFuZG9jYCBhbmQgYHBhbmRvYy14bm9z
YAooYHBhbmRvYy1maWdub3NgLCBgcGFuZG9jLXNlY25vc2AsIGBwYW5kb2MtZXFub3NgLCBg
cGFuZG9jLXRhYmxlbm9zYCkuClRoZSBkZXRhaWxzIGFyZSBzaG93biBpbiB0aGUgTWFrZWZp
bGUgaGVscCBtZXNzYWdlLgoKIyMgYG1hcmt5YCBXb3JrZmxvdwoKV29ya2Zsb3cgZm9yIGNy
ZWF0aW5nIGBodG1sYCBvciBgcGRmYCB1c2luZyBgbWFya3lgCgoxLiB1c2VyIHdyaXRlcyBh
IE1hcmtkb3duIHRleHQgZmlsZSBhbmQgcGxhY2VzIGl0IGluIGBtZC8qLm1kYApkaXJlY3Rv
cnkgd2l0aCB0aGUgZXh0ZW5zaW9uIGAubWRgLgoyLiBgbWFya3lgIHRyYW5zZm9ybXMgdGhl
IGZpbGVzIGluIGBtZC8qLm1kYCBpbnRvIHJlZ3VsYXIgTWFya2Rvd24gdGV4dAphbmQgcGxh
Y2VzIHRoZSB0cmFuc2Zvcm1lZCBmaWxlcyBpbiBgYnVpbGQvYC4KMy4gdGhlIHJlZ3VsYXIg
TWFya2Rvd24gdGV4dCBpbiB0aGUgZmlsZXMgYGJ1aWxkLyoubWRgIGlzIHJlbmRlcmVkIGlu
dG8KYGh0bWxgIGFuZCBgcGRmYCB1c2luZyBgcGFuZG9jYC4KClRoZSB0aHJlZSBzdGVwcyBh
cmUgaW1wbGVtZW50ZWQgaW4gYSBNYWtlZmlsZS4KCiMjIERvd25sb2FkIGFuZCBJbml0aWFs
aXplCgpgbWFya3lgIGlzIHN1cHBsaWVkIGFzIGEgc2luZ2xlLWZpbGUgc2NyaXB0IHdoaWNo
IGF1dG9tYXRpY2FsbHkKc2V0cyB1cCB0aGUgcHJvamVjdCBzdHJ1Y3R1cmUgY29udGFpbmlu
ZyBhbGwgc2NyaXB0cwpyZXF1aXJlZCBmb3IgcHJvY2Vzc2luZyBhbmQgcmVuZGVyaW5nIE1h
cmtkb3duLgoKRm9yIGV4YW1wbGUsIGRvd25sb2FkIGBtYXJreWAgZnJvbSBnaXRodWIuCmBg
YGJhc2gKZ2l0IGNsb25lIGh0dHBzOi8vbGVobWFubjcuZ2l0aHViLmNvbS9tYXJreS5naXQK
Y2QgbWFya3kKYGBgCgpBZnRlciBkb3dubG9hZCwgdGhlIGBtYXJreWAgZW52aXJvbm1lbnQg
aXMgaW5pdGlhbGl6ZWQgdXNpbmcgYG1hcmt5YC4KYGBgYmFzaAouL21hcmt5LnB5IC0taW5p
dAojIG1rZGlyIGJ1aWxkLwojIG1rZGlyIGRhdGEKIyBta2RpciBtZC8KIyBXUklURSBNYWtl
ZmlsZQojIFdSSVRFIHBhbmRvYy1ydW4KIyBXUklURSBtZC9tYXJreS5tZAojIFdSSVRFIC5n
aXRpZ25vcmUKIyBVU0FHRQptYWtlIGhlbHAKYGBgCgojIyBgbWFya3lgIEVudmlyb25tZW50
CgpEdXJpbmcgaW5pdGlhbGl6YXRpb24sIGBtYXJreWAgY3JlYXRlcyBkaXJlY3RvcmllcyBh
bmQgZmlsZXMuCkFmdGVyIGluaXRpYWxpemF0aW9uLCB0aGUgZm9sbG93aW5nIHN0cnVjdHVy
ZSBpcyBhdXRvLWdlbmVyYXRlZAppbiB0aGUgcHJvamVjdCBkaXJlY3RvcnkuCmBgYGJhc2gK
bWFrZSBoZWxwCjw/Cl9fXyh0ZXh0X3Byb2MoIm1ha2UgdHJlZSIpKQo/PgpgYGAKClRoZSBz
Y3JpcHQgYHBhbmRvYy1ydW5gIGNhbiBiZSBhZGp1c3RlZCBpbiBjYXNlIHNwZWNpZmljCmBw
YW5kb2NgIG9wdGlvbnMgYXJlIHJlcXVpcmVkIGZvciByZW5kZXJpbmcgdGhlIGBodG1sYCBh
bmQgYHBkZmAgZG9jdW1lbnRzLgoKIyMgRG9jdW1lbnQgUmVuZGVyaW5nCgpCeSBpbnZva2lu
ZyBgbWFrZSBhbGxgIGFsbCBmaWxlcyBgbWQvKi5tZGAgYXJlIHRyYW5zZm9ybWVkCmludG8g
Y29ycmVzcG9uZGluZyBgaHRtbC8qLmh0bWxgIGFuZCBgcGRmLyoucGRmYCBmaWxlcy4gQnkK
aW52b2tpbmcgYG1ha2UgaHR0cGRgIGEgcHl0aG9uIHdlYiBzZXJ2ZXIgaXMgc3RhcnRlZCBp
biBgaHRtbC9gLgoKQWxsIHVzZXItZ2VuZXJhdGVkIE1hcmtkb3duIGNvbnRlbnQgZ29lcyBp
bnRvIGBtZC8qYCB1c2VyLWdlbmVyYXRlZApkYXRhIGZpbGVzIGdvIGludG8gYGRhdGEvKmAu
CgoqKkFUVEVOVElPTjoqKiBUaGUgZmlsZXMgaW4gdGhlIGRpcmVjdG9yaWVzIGBidWlsZC8q
YCBhcmUKKiphdXRvLWdlbmVyYXRlZCoqLiBBbGwgdXNlciBmaWxlcyBoYXZlIHRvIGJlIHBs
YWNlZCBpbnNpZGUgdGhlCmRpcmVjdG9yeSBgbWQvKmAuIEludm9raW5nIGBtYWtlIGNsZWFu
YCB3aWxsICoqZGVsZXRlIGFsbCBmaWxlcyoqCmluIGBodG1sL2AsIGBidWlsZC9gIGFuZCBg
cGRmL2AuCgojIyBJbnRlZ3JhdGVkIERvY3VtZW50YXRpb24KCmBtYXJreWAgaGFzIGFuIGlu
dGVncmF0ZWQgZW52aXJvbm1lbnQuIFVzaW5nIGBtYWtlIGhlbHBgIGRpc3BsYXlzCmEgc2hv
cnQgaW5mbyBhYm91dCB0aGUgYG1hcmt5YCBkZXBlbmRlbmNpZXMsIG1ha2UgdGFyZ2V0cyBh
bmQKZXhhbXBsZXMuCmBgYGJhc2gKbWFrZSBoZWxwCjw/Cl9fXyh0ZXh0X3Byb2MoIm1ha2Ug
aGVscCIpKQo/PgpgYGAKCiMgYG1hcmt5YCBGZWF0dXJlcwoKUGxhY2UgYSBuZXcgZmlsZSBp
biBgbWQvZmlsZS5tZGAgYW5kIHJ1biB0aGUgZm9sbG93aW5nIGNvbW1hbmRzLgpgYGBiYXNo
CnRvdWNoIG1kL2ZpbGUubWQKYGBgCgpgbWFya3lgIGRpc2NvdmVycyB0aGUgbmV3IGRvY3Vt
ZW50IHdoZW4gaW52b2tpbmcgYG1ha2Ugc2NhbmAuCmBgYGJhc2gKbWFrZSBzY2FuCiMgV1JJ
VEUgYnVpbGQvZmlsZS5tYWtlCmBgYAoKYG1hcmt5YCByZW5kZXJzIGBodG1sYCBhbmQgYHBk
ZmAgdXNpbmcgbWFrZSB0YXJnZXRzLgpgYGBiYXNoCm1ha2UgaHRtbC9maWxlCm1ha2UgcGRm
L2ZpbGUKYGBgCgojIyBNZXRhIERhdGEgaW4gRnJvbnQgTWF0dGVyCgpJZiBkb2N1bWVudCBz
dGFydHMgd2l0aCBgLS0tYCwgeWFtbCBpcyB1c2VkIHRvIHBhcnNlCnRoZSBmcm9udCBtYXR0
ZXIgYmxvY2sgZGVsaW1pdGVkIGJ5IGAtLS1gLgpBbGwgbWV0YSBkYXRhIGtleXMgd2lsbCBi
ZSBleHBvc2VkIGludG8gdGhlIHB5dGhvbiBzY29wZSBhcyBhIGxvY2FsCnZhcmlhYmxlLCB1
bmxlc3MgdGhlIHZhcmlhYmxlIGFscmVhZHkgZXhpc3RzLgoKYGBgbWQKLS0tCnRpdGxlOiAi
TXkgRG9jdW1ldCIKYXV0aG9yOiAuLi4KZGF0ZTogMjAyMi0wMS0wMQotLS0KVGhlIHRpdGxl
IG9mIHRoaXMgZG9jdW1lbnQgaXMge1x7dGl0bGV9XH0uCmBgYAoKIyMgRW1iZWRkaW5nIFB5
dGhvbiBDb2RlCgpQeXRob24gY29kZSBibG9ja3MgYXJlIGVtYmVkZGVkIGludG8gTWFya2Rv
d24gdXNpbmcgYDxcPy4uLj9cPmAgYW5kIGB7XHsuLi59XH1gLgpBbGwgY29kZSBibG9ja3Mg
c3BhbiBvbmUgbGFyZ2Ugc2NvcGUgc2hhcmluZyBmdW5jdGlvbnMgYW5kIGxvY2FsCnZhcmlh
Ymxlcy4gTWV0YSBkYXRhIGlzIGltcG9ydGVkIGZyb20gTWFya2Rvd24gZnJvbnQgbWF0dGVy
IGFzIGxvY2FsCnZhcmlhYmxlcyBpbiB0aGUgcHl0aG9uIHNjb3BlLiBUaGUgYGltcG9ydGAg
c3RhdGVtZW50IGNhbiBiZSB1c2VkIGluCnB5dGhvbiBjb2RlIGluIG9yZGVyIHRvIGFjY2Vz
cyBpbnN0YWxsZWQgcHl0aG9uIHBhY2thZ2VzIGFzIHVzdWFsLgoKIyMjIFZpc2libGUgQ29k
ZQoKVXNpbmcgYDxcPyEuLi4/XD5gIGNvZGUgaXMgZXhlY3V0ZWQgYW5kIGFsc28gc2hvd24g
aW4gTWFya2Rvd24uCgojIyMjIEV4YW1wbGUgey19CmBgYHB5dGhvbgo8XD8hCnggPSA0MiAj
IHZpc2libGUgY29kZQpwcmludCgiSGVsbG8gY29uc29sZSEiKQo/XD4KYGBgCgojIyMjIFJ1
biBhbmQgT3V0cHV0IHstfQpgYGBweXRob248PyEKeCA9IDQyICMgdmlzaWJsZSBjb2RlCj8+
CmBgYAoKKipBdHRlbnRpb246KiogVXNpbmcgdGhlIGBwcmludCgpYCBmdW5jdGlvbiB0aGUg
dGV4dCB3aWxsIGJlIHByaW50ZWQKdG8gdGhlIGNvbnNvbGUgYW5kICoqbm90KiogaW5zaWRl
IHRoZSByZXN1bHRpbmcgTWFya2Rvd24gdGV4dC4KCiMjIyBIaWRkZW4gQ29kZQoKVXNpbmcg
YDxcPy4uLj9cPmAgY29kZSBpcyBleGVjdXRlZCBidXQgbm90IHNob3duIGluIE1hcmtkb3du
LgoKIyMjIyBFeGFtcGxlIHstfQpgYGBweXRob24KPFw/CnggPSA0MSAjIGhpZGRlbiBjb2Rl
Cl9fXyhmIk91dHB1dCB0byBNYXJrZG93bi4geCA9IHt4fSEiKQo/XD4KYGBgCiMjIyMgUnVu
IGFuZCBPdXRwdXQgey19CmBgYHB5dGhvbgo8Pwp4ID0gNDEgIyBoaWRkZW4gY29kZQpfX18o
ZiJPdXRwdXQgdG8gTWFya2Rvd24uIHggPSB7eH0hIikKPz4KYGBgCgoqKkF0dGVudGlvbjoq
KiBVc2luZyB0aGUgYF9fXygpYCBmdW5jdGlvbiB0aGUgdGV4dCB3aWxsIGJlIHByaW50ZWQK
aW5zaWRlIHRoZSByZXN1bHRpbmcgTWFya2Rvd24gdGV4dCAqKmFuZCBub3QqKiBvbiB0aGUg
Y29uc29sZS4KCiMjIFRoZSBgX19fKClgIEZ1bmN0aW9uCgpVc2luZyB0aGUgYHByaW50KClg
IHN0YXRlbWVudCB0aGUgdGV4dCB3aWxsIGJlIHByaW50ZWQgdG8gdGhlIGNvbnNvbGUuCldo
ZW4gdXNpbmcgdGhlIGBfX18oKWAgc3RhdGVtZW50IG5ldyBNYXJrZG93biB0ZXh0IGlzCmlu
c2VydGVkIGR5bmFtaWNhbGx5IGludG8gdGhlIGRvY3VtZW50IGR1cmluZyBwcmVwcm9jZXNz
aW5nLgoKIyMjIyBFeGFtcGxlOiBMaW5lIEJyZWFrIHstfQpgYGBweXRob24KPFw/CnggPSA0
MCAjIGhpZGRlbiBjb2RlCl9fXygiT3V0cHV0IGluIiwgX19fKQpfX18oInNpbmdsZSBsaW5l
ISAiLCBfX18pCl9fXyhmInggPSB7eH0iKQo/XD4KYGBgCiMjIyMgUnVuIGFuZCBPdXRwdXQg
ey19CmBgYGJhc2gKPD8KeCA9IDQwICMgaGlkZGVuIGNvZGUKX19fKCJPdXRwdXQgaW4gIiwg
X19fKQpfX18oInNpbmdsZSBsaW5lISAiLCBfX18pCl9fXyhmInggPSB7eH0iKQo/PgpgYGAK
CiMjIyMgRXhhbXBsZTogU2hpZnQsIENyb3AsIFJldHVybiB7LX0KYGBgcHl0aG9uCjxcPwpy
ZXN1bHQgPSBfX18oIiIiCiAgICogdGV4dCBpcyBjcm9wcGVkIGFuZCBzaGlmdGVkCiAgICAg
ICAgICogc2hpZnQgYW5kIGNyb3AKICAgICAgICAgICAgKiBjYW4gYmUgY29tYmluZWQKICAg
ICAgICAgICogcmV0dXJuaW5nIHRoZSByZXN1bHQKIiIiLCBzaGlmdD0iIyMjIyMjIyMiLCBj
cm9wPVRydWUsIHJldD1UcnVlKQpfX18ocmVzdWx0KQo/XD4KYGBgCiMjIyMgUnVuIGFuZCBP
dXRwdXQgey19CmBgYGJhc2gKPD8KcmVzdWx0ID0gX19fKCIiIgogICAqIHRleHQgaXMgY3Jv
cHBlZCBhbmQgc2hpZnRlZAogICAgICAgICAqIHNoaWZ0IGFuZCBjcm9wCiAgICAgICAgICAg
ICogY2FuIGJlIGNvbWJpbmVkCiAgICAgICAgICAqIHJldHVybmluZyB0aGUgcmVzdWx0CiIi
Iiwgc2hpZnQ9IiMjIyMjIyMjIiwgY3JvcD1UcnVlLCByZXQ9VHJ1ZSkKX19fKHJlc3VsdCkK
Pz4KYGBgCgojIyBBbGdvcml0aG1pYyBUYWJsZSBFeGFtcGxlCgpAdGJsOmFsZ3QgaXMgZ2Vu
ZXJhdGVkIHVzaW5nIHRoZSBmb2xsb3dpbmcgcHl0aG9uIGNsb2RlIGJsb2NrLgoKYGBgcHl0
aG9uPD8hCm4gPSA1CnRhYmxlID0gIiIKZGVjID0gWyIqJXMqIiwgIioqJXMqKiIsICJ+fiVz
fn4iLCAiYCVzYCIsCiAgICAgICByIiRcdGltZXNeJXMkIiwgIiRcaW5mdHlfJXMkIl0KdGFi
bGUgKz0gInwiLmpvaW4oIlgiKm4pICsgIlxuIiArICJ8Ii5qb2luKCItIipuKSArICJcbiIK
Zm9yIGkgaW4gcmFuZ2Uobik6CglmaWxsID0gW2NocihvcmQoIkEiKSsoMippKzMqayklMjYp
IGZvciBrIGluIHJhbmdlKGkrMSldCglmaWxsID0gW2RlY1sobCtpKSVsZW4oZGVjKV0layBm
b3IgbCwgayBpbiBlbnVtZXJhdGUoZmlsbCldCgl0ZXh0ID0gbGlzdCgiMCIpKm4KCXRleHRb
KG4+PjEpLShpPj4xKToobj4+MSkrKGk+PjEpXSA9IGZpbGwKCXRhYmxlICs9ICJ8Ii5qb2lu
KHRleHQpICsgIlxuIgo/PgpgYGAKCnt7dGFibGV9fQoKVGFibGU6IFRhYmxlIGlzIGdlbmVy
YXRlZCB1c2luZyBjb2RlIGFuZCB0aGUgYF9fXygpYCBzdGF0ZW1lbnQuIHsjdGJsOmFsZ3R9
CgojIyBJbmxpbmUgRm9ybWF0dGVkIE91dHB1dAoKVGhlIGB7XHsuLi59XH1gIHN0YXRlbWVu
dCB1c2VzIHNudGF4IHNpbWlsYXIgdG8gcHl0aG9uIGBmYC1zdHJpbmdzIGZvcgpmb3JtYXR0
ZWQgb3V0cHV0IG9mIHZhcmlhYmxlcyBhbmQgcmVzdWx0cyBvZiBleHByZXNzaW9ucyBpbnRv
IE1hcmtkb3duCnRleHQuIFRoZSBgbWFya3lgIG9wZXJhdG9yIGB7XHs8ZXhwcmVzc2lvbj5b
Ojxmb3JtYXQ+XX1cfWAgdXNlcyB0aGUKc3ludGF4IG9mIFtgZmAtc3RyaW5nc10oaHR0cHM6
Ly9kb2NzLnB5dGhvbi5vcmcvMy9yZWZlcmVuY2UvbGV4aWNhbF9hbmFseXNpcy5odG1sI2Yt
c3RyaW5ncykuCgojIyMjIEV4YW1wbGUgMSB7LX0KYGBgYmFzaApUZXh0IHRleHQge1x7eH1c
fSBhbmQge1x7IiwiLmpvaW4oW3N0cihpKSBmb3IgaSBpbiByYW5nZSh4LTEwLHgpXSl9XH0u
CmBgYAojIyMjIE91dHB1dCB7LX0KPiBUZXh0IHRleHQge3t4fX0gYW5kIHt7IiwiLmpvaW4o
W3N0cihpKSBmb3IgaSBpbiByYW5nZSh4LTEwLHgpXSl9fS4KCiMjIyMgRXhhbXBsZSAyIHst
fQpgYGBweXRob248PyEKeCA9IGludCgxKQp5ID0gZmxvYXQoMi4zKQp6ID0gMAphID0gWzEs
IDIsIDNdCmIgPSAoNCwgNSkKPz4KYGBgCmBgYG1hcmtkb3duClRoaXMgaXMgYSBwYXJhZ3Jh
cGggYW5kIHggaXMge1x7eDowM2R9XH0gYW5kIHkgaXMge1x7eTouMmZ9XH0uCk90aGVyIGNv
bnRlbnQgaXM6IGEgPSB7XHthfVx9LCBiID0ge1x7Yn1cfS4KYGBgCiMjIyMgT3V0cHV0IHst
fQo+IFRoaXMgaXMgYSBwYXJhZ3JhcGggYW5kIHggaXMge3t4OjAzZH19IGFuZCB5IGlzIHt7
eTouMmZ9fS4KPiBPdGhlciBjb250ZW50IGlzOiBhID0ge3thfX0sIGIgPSB7e2J9fS4KCiMj
IEZvcm1hdCBMaW5rIEV4dGVuc2lvbgoKV2hlbiB3cml0aW5nIG11bHRpcGxlIGRvY3VtZW50
cywgb2Z0ZW4gZG9jdW1lbnRzIGFyZSByZWZlcmVuY2VkCmJldHdlZW4gZWFjaCBvdGhlciB1
c2luZyBsaW5rcy4gSW4gb3JkZXIgdG8gcmVmZXIgdG8gZXh0ZXJuYWwKYGh0bWxgIGFuZCBg
cGRmYCBkb2N1bWVudHMgdGhlIE1hcmtkb3duIGxpbmsgc3RhdGVtZW50IGlzIHVzZWQuCmBg
YG1kCltMaW5rIENhcHRpb25dKHBhdGgvdG8vZmlsZS5odG1sKQpbTGluayBDYXB0aW9uXShw
YXRoL3RvL2ZpbGUucGRmKQpgYGAKT25lIGxpbmsgc3RhdGVtZW50IGNhbm5vdCBiZSB1c2Vk
IGZvciByZW5kZXJpbmcgYGh0bWxgIGFuZCBgcGRmYAp3aXRoIGNvbnNpc3RlbnQgcGF0aHMu
IFVzaW5nIHRoZSBgbWFya3lgIGZvcm1hdCBsaW5rCiBgLlw/Pz9gIGZpbGUgZXh0ZW5zaW9u
IHJlc3VsdHMgaW4gY29uc2lzdGVudCBsaW5rcyBmb3IgYGh0bWxgIGFuZApgcGRmYCBkb2N1
bWVudHMuCgojIyMjIEV4YW1wbGUgey19CmBgYG1kCltMaW5rIHRvIHRoaXMgRG9jdW1lbnRd
KG1hcmt5Llw/Pz8pCmBgYAojIyMjIE91dHB1dCB7LX0KPiBbTGluayB0byB0aGlzIERvY3Vt
ZW50XShtYXJreS4/Pz8pCgojIyBGb3JtYXQgQ29kZXMKCk9mdGVuIHdoZW4gd3JpdGluZyBt
YXJrZG93biBmb3IgYGh0bWxgIGFuZCBgcGRmYCBkb2N1bWVudHMsIHRoZQpvdXRwdXQgbmVl
ZHMgdG8gYmUgdHdlYWtlZCBhY2NvcmRpbmdseS4KYG1hcmt5YCBzdXBwb3J0cyBmb3JtYXQg
c3BlY2lmaWMgdHdlYWtpbmcgYnkgaW5qZWN0aW5nCnJhdyBgaHRtbGAgb3IgYHRleGAgY29k
ZSBpbnRvIE1hcmtkb3duIHVzaW5nIGZvcm1hdCBjb2Rlcy4KCkluIG9yZGVyIHRvIGluamVj
dCBmb3JtYXQgc3BlY2lmaWMgY29kZSB0aGUgYGZtdGNvZGVgIGNsYXNzIGlzIHVzZWQuClRo
ZSBgZm10Y29kZWAgY2xhc3MgbWFuYWdlcyBpbmplY3Rpb24gb2YgYGh0bWxgIGFuZCBgdGV4
YCBjb2RlCmRlcGVuZGluZyBvbiB0aGUgb3V0cHV0IGZvcm1hdC4KCioqQVRURU5USU9OOioq
IGB0ZXhgIHBhY2thZ2VzIGhhdmUgdG8gYmUgaW5jbHVkZWQgZm9yIGBwZGZgIGFzIHdlbGwg
YXMKSmF2YVNjcmlwdCBhbmQgc3R5bGUgc2hlZXRzIGZvciBgaHRtbGAgdXNpbmcgdGhlIG1l
dGEgZGF0YSBmaWVsZHMKYGhlYWRlci1pbmNsdWRlcy0tcGRmYCBhbmQgYGhlYWRlci1pbmNs
dWRlcy0taHRtbGAgcmVzcGVjdGl2ZWx5LgoKIyMjIyBFeGFtcGxlOiBgZm10Y29kZWAgey19
CmBgYHB5dGhvbjw/IQpGID0gZm10Y29kZShodG1sPSJIPHN1cD5UPC9zdXA+PHN1Yj5NPC9z
dWI+TCIsIHBkZj1yIlxMYVRlWCIpCj8+CmBgYApgYGBtYXJrZG93bgpJbnZvY2F0aW9uIG9m
IGZvcm1hdCBjb2RlIHJlc3VsdHMgaW46IHtce0YoKX1cfS4KYGBgCiMjIyMgT3V0cHV0IHst
fQo+IEludm9jYXRpb24gb2YgZm9ybWF0IGNvZGUgcmVzdWx0cyBpbjoge3tGKCl9fS4KCiMj
IyMgRXhhbXBsZTogQ29sb3Igey19CmBgYHB5dGhvbjw/IQpDID0gbGFtYmRhIGNvbG9yOiBm
bXRjb2RlKAoJaHRtbD0iPHNwYW4gc3R5bGU9J2NvbG9yOiVzOyc+ezB9PC9zcGFuPiIgJSBj
b2xvciwKCXBkZj1yIlx0ZXh0Y29sb3J7eyVzfX17e3swfX19IiAlIGNvbG9yCikKQiA9IEMo
ImJsdWUiKQpSID0gQygicmVkIikKPz4KYGBgCmBgYG1hcmtkb3duClRleHQgd2l0aCB7XHtC
KCJibHVlIil9XH0gYW5kIHtce1IoIlJFRCIpfVx9LgpgYGAKIyMjIyBPdXRwdXQgey19Cj4g
VGV4dCB3aXRoIHt7QigiYmx1ZSIpfX0gYW5kIHt7UigiUkVEIil9fS4KCgojIyMjIEV4YW1w
bGU6IENsYXNzZXMgey19CmBgYHB5dGhvbjw/IQpjbGFzcyBjb2xvcjoKCWRlZiBfX2luaXRf
XyhzZWxmLCBjb2xvcik6CgkJc2VsZi5jb2xvciA9IGNvbG9yCglkZWYgdXBwZXIoc2VsZiwg
eCk6CgkJcmV0dXJuIHNlbGYudGV4dCh4LnVwcGVyKCkpCglkZWYgbG93ZXIoc2VsZiwgeCk6
CgkJcmV0dXJuIHNlbGYudGV4dCh4Lmxvd2VyKCkpCgpjbGFzcyBodG1sKGNvbG9yKToKCWRl
ZiB0ZXh0KHNlbGYsIHgpOgoJCXJldHVybiBmIjxzcGFuIHN0eWxlPSdjb2xvcjp7c2VsZi5j
b2xvcn07Jz57eH08L3NwYW4+IgoKY2xhc3MgcGRmKGNvbG9yKToKCWRlZiB0ZXh0KHNlbGYs
IHgpOgoJCXJldHVybiByZiJcdGV4dGNvbG9ye3t7c2VsZi5jb2xvcn19fXt7e3h9fX0iCgpD
QyA9IGxhbWJkYSB4OiBmbXRjb2RlKGh0bWw9aHRtbCh4KSwgcGRmPXBkZih4KSkKQkIgPSBD
QygiYmx1ZSIpClJSID0gQ0MoInJlZCIpCj8+CmBgYApgYGBtYXJrZG93bgpUZXh0IHdpdGgg
e1x7QkIudXBwZXIoImJsdWUiKX1cfSBhbmQge1x7UlIubG93ZXIoIlJFRCIpfVx9LgpgYGAK
IyMjIyBPdXRwdXQgey19Cj4gVGV4dCB3aXRoIHt7QkIudXBwZXIoImJsdWUiKX19IGFuZCB7
e1JSLmxvd2VyKCJSRUQiKX19LgoKIyBNZXRhIERhdGEgaW4gRnJvbnQgTWF0dGVyCgpNZXRh
IGRhdGEgaXMgYW5ub3RhdGVkIGluIHRoZSBmcm9udCBtYXR0ZXIgb2YgYSAJTWFya2Rvd24g
dGV4dCBkb2N1bWVudC4KVGhlIGZyb250IG1hdHRlciBtdXN0IHN0YXJ0IGluIHRoZSBmaXJz
dCBsaW5lIHdpdGggYC0tLWAgYW5kIHByZWNlZGVzIGFsbApvdGhlciB0ZXh0IGJlaW5nIGZl
bmNlZCBieSBgLS0tYC4gVGhlIG1ldGEgZGF0YSBpcyBpbiBgeWFtbGAgZm9ybWF0LgpUaGUg
YHlhbWxgIGJsb2NrIGlzIHBhcnNlZCB1c2luZyBgcHl0aG9uLXB5eWFtbGAuIEFsbCBtZXRh
CmRhdGEgaXMgaW1wb3J0ZWQgaW50byB0aGUgcHJlcHJvY2Vzc2VkIGRvY3VtZW50LgoKIyMg
UGFuZG9jIEZyb250IE1hdHRlcgoKIyMjIyBFeGFtcGxlIHstfQpgYGB5YW1sCi0tLQp0aXRs
ZToKZGF0ZToKYXV0aG9yOgpsaW5rLWNpdGF0aW9uczoKYmlibGlvZ3JhcGh5OgpoZWFkZXIt
aW5jbHVkZXM6Cnhub3MtY2xldmVyZWY6Cnhub3MtY2FwaXRhbGlzZToKZm9udHNpemU6Ci0t
LQpgYGAKVGhlIG1ldGEgZGF0YSBmaWVsZHMKW2B0aXRsZWAsIGBkYXRlYCwgYGF1dGhvcmBd
KGh0dHBzOi8vcGFuZG9jLm9yZy9NQU5VQUwuaHRtbCNtZXRhZGF0YS12YXJpYWJsZXMpLApb
YGxpbmstY2l0YXRpb25zYF0oaHR0cHM6Ly9wYW5kb2Mub3JnL01BTlVBTC5odG1sI290aGVy
LXJlbGV2YW50LW1ldGFkYXRhLWZpZWxkcyksCltgYmlibGlvZ3JhcGh5YF0oaHR0cHM6Ly9w
YW5kb2Mub3JnL01BTlVBTC5odG1sI2NpdGF0aW9uLXJlbmRlcmluZykgYW5kCltgaGVhZGVy
LWluY2x1ZGVzYF0oaHR0cHM6Ly9wYW5kb2Mub3JnL01BTlVBTC5odG1sI3ZhcmlhYmxlcy1z
ZXQtYXV0b21hdGljYWxseSkKYXJlIHByb2Nlc3NlZCBieSBgcGFuZG9jYCBkdXJpbmcgZG9j
dW1lbnQgcmVuZGVyaW5nLiBgZm9udHNpemVgIGFkanVzdHMgdGhlCmZvbnQgc2l6ZSBpbiBb
YGh0bWxgXShodHRwczovL3BhbmRvYy5vcmcvTUFOVUFMLmh0bWwjdmFyaWFibGVzLWZvci1o
dG1sKQphbmQgW2BwZGZgXShodHRwczovL3BhbmRvYy5vcmcvTUFOVUFMLmh0bWwjdmFyaWFi
bGVzLWZvci1sYXRleCkgZG9jdW1lbnRzLgpUaGUgYHhub3MtY2xldmVyZWZgIGFuZCBgeG5v
cy1jYXBpdGFsaXNlYApmaWVsZHMgYXJlIHVzZWQgYnkgdGhlIFtgcGFuZG9jLXhub3NgXSho
dHRwczovL2dpdGh1Yi5jb20vdG9tZHVjay9wYW5kb2MteG5vcykKZXh0ZW5zaW9ucyBmb3Ig
cmVmZXJlbmNpbmcKW2ZpZ3VyZXNdKGh0dHBzOi8vZ2l0aHViLmNvbS90b21kdWNrL3BhbmRv
Yy1maWdub3MjY3VzdG9taXphdGlvbiksClt0YWJsZXNdKGh0dHBzOi8vZ2l0aHViLmNvbS90
b21kdWNrL3BhbmRvYy10YWJsZW5vcyNjdXN0b21pemF0aW9uKSwKW3NlY3Rpb25zXShodHRw
czovL2dpdGh1Yi5jb20vdG9tZHVjay9wYW5kb2Mtc2Vjbm9zI2N1c3RvbWl6YXRpb24pIGFu
ZApbZXF1YXRpb25zXShodHRwczovL2dpdGh1Yi5jb20vdG9tZHVjay9wYW5kb2MtZXFub3Mj
Y3VzdG9taXphdGlvbikuCgojIyBgbWFya3lgIEZvcm1hdCBGaWVsZHMKCioqRXhhbXBsZSoq
CmBgYHlhbWwKLS0tCmhlYWRlci1pbmNsdWRlcy0tcGRmOiA+CiAgXGh5cGVyc2V0dXB7CiAg
Y29sb3JsaW5rcz1mYWxzZSwKICBhbGxib3JkZXJjb2xvcnM9ezAgMCAwfSwKICBwZGZib3Jk
ZXJzdHlsZT17L1MvVS9XIDF9XH0KaGVhZGVyLWluY2x1ZGVzLS1odG1sOiA+CiAgPHN0eWxl
PiogeyBib3gtc2l6aW5nOiBib3JkZXItYm94OyB9PC9zdHlsZT4KLS0tCmBgYAoKVGhlIHBh
bmRvYyBgaGVhZGVyLWluY2x1ZGVzYCBmaWVsZCBpcyB1c2VkIGZvciBgcGRmYCBhbmQgYGh0
bWxgIGRvY3VtZW50cywKdGhlcmVmb3JlIGl0IG11c3QgY29udGFpbiBjb3JyZXNwb25kaW5n
IHRleCBhbmQgYGh0bWxgIGNvZGUuCgpUaGUgZmllbGQgYGhlYWRlci1pbmNsdWRlc2AgZW5k
aW5nIHdpdGggYC0tcGRmYCBvciBgLS1odG1sYApzcGVjaWZpZXMgY29ycmVzcG9uZGluZyBv
cHRpb25zIGZvciB0aGUgZ2VuZXJhdGlvbiBvZiBgcGRmYCBhbmQgYGh0bWxgCmRvY3VtZW50
cy4gRHVyaW5nIG1ha2UsIGBtYXJreWAgc2NhbnMgYWxsIG1ldGEgZGF0YSBmaWVsZHMsIGFu
ZApmaWVsZHMgd2hpY2ggZW5kIHdpdGggYC0tcGRmYCBhbmQgYC0taHRtbGAgYXJlIHNlbGVj
dGVkIGFuZCBmb3J3YXJkZWQKdG8gYHBhbmRvY2AgYmFzZWQgb24gdGhlIGZvcm1hdCB0byBi
ZSByZW5kZXJlZC4KCiMgU2NpZW50aWZpYyBXcml0aW5nIGluIE1hcmtkb3duIHsjc2VjOnBh
bm1kfQoKW01hcmtkb3duXShodHRwczovL3BhbmRvYy5vcmcvTUFOVUFMLmh0bWwjcGFuZG9j
cy1tYXJrZG93bikgaXMgYSBtYXJrdXAKbGFuZ3VhZ2UgZm9yIHRlY2huaWNhbCB3cml0aW5n
LCB3aXRoIGVtcGhhc2lzIG9uIHJlYWRhYmlsaXR5LiBNYXJrZG93bgpjYW4gYmUgcmVuZGVy
ZWQgaW4gbWFueSBmb3JtYXRzIGluY2x1ZGluZyBgaHRtbGAgYW5kIGBwZGZgIGJ5IHVzaW5n
CltgcGFuZG9jYF0oaHR0cHM6Ly9wYW5kb2Mub3JnLykgZm9yIGV4YW1wbGUuCgpVc2luZyB2
YXJpb3VzIE1hcmtkb3duIGV4dGVuc2lvbnMgb2YgYHBhbmRvY2AgYSBzdWZmaWNpZW50IHN0
cnVjdHVyZSBmb3IKd3JpdGluZyBzY2llbnRpZmljIGRvY3VtZW50cyBpcyByZWZsZWN0ZWQg
dXNpbmcgTWFya2Rvd24gc3ludGF4LgpgbWFya3lgIGJ5IGRlZmF1bHQgdXNlcyB0aGUgZm9s
bG93aW5nIGBwYW5kb2NgIE1hcmtkb3duIGV4dGVuc2lvbnMuCiogcGFyc2luZyBleHRlbnNp
b25zCgkqIFthbGxfc3ltYm9sc19lc2NhcGFibGVdKGh0dHBzOi8vcGFuZG9jLm9yZy9NQU5V
QUwuaHRtbCNleHRlbnNpb24tYWxsX3N5bWJvbHNfZXNjYXBhYmxlKQoJKiBbaW50cmF3b3Jk
X3VuZGVyc2NvcmVzXShodHRwczovL3BhbmRvYy5vcmcvTUFOVUFMLmh0bWwjZXh0ZW5zaW9u
LWludHJhd29yZF91bmRlcnNjb3JlcykKCSogW2VzY2FwZWRfbGluZV9icmVha3NdKGh0dHBz
Oi8vcGFuZG9jLm9yZy9NQU5VQUwuaHRtbCNleHRlbnNpb24tZXNjYXBlZF9saW5lX2JyZWFr
cykKCSogW3NwYWNlX2luX2F0eF9oZWFkZXJdKGh0dHBzOi8vcGFuZG9jLm9yZy9NQU5VQUwu
aHRtbCNleHRlbnNpb24tc3BhY2VfaW5fYXR4X2hlYWRlcikKCSogW2xpc3RzX3dpdGhvdXRf
cHJlY2VkaW5nX2JsYW5rbGluZV0oaHR0cHM6Ly9wYW5kb2Mub3JnL01BTlVBTC5odG1sI2V4
dGVuc2lvbi1saXN0c193aXRob3V0X3ByZWNlZGluZ19ibGFua2xpbmUpCiogc3R5bGluZyBl
eHRlbnNpb25zCgkqIFtpbmxpbmVfY29kZV9hdHRyaWJ1dGVzXShodHRwczovL3BhbmRvYy5v
cmcvTUFOVUFMLmh0bWwjZXh0ZW5zaW9uLWlubGluZV9jb2RlX2F0dHJpYnV0ZXMpCgkqIFtz
dHJpa2VvdXRdKGh0dHBzOi8vcGFuZG9jLm9yZy9NQU5VQUwuaHRtbCNleHRlbnNpb24tc3Ry
aWtlb3V0KQoqIHN0cnVjdHVyaW5nIGV4dGVuc2lvbnMKCSogW3lhbWxfbWV0YWRhdGFfYmxv
Y2tdKGh0dHBzOi8vcGFuZG9jLm9yZy9NQU5VQUwuaHRtbCNleHRlbnNpb24teWFtbF9tZXRh
ZGF0YV9ibG9jaykKCSogW3BpcGVfdGFibGVzXShodHRwczovL3BhbmRvYy5vcmcvTUFOVUFM
Lmh0bWwjZXh0ZW5zaW9uLXBpcGVfdGFibGVzKQoJKiBbbGluZV9ibG9ja3NdKGh0dHBzOi8v
cGFuZG9jLm9yZy9NQU5VQUwuaHRtbCNleHRlbnNpb24tbGluZV9ibG9ja3MpCgkqIFtpbXBs
aWNpdF9maWd1cmVzXShodHRwczovL3BhbmRvYy5vcmcvTUFOVUFMLmh0bWwjZXh0ZW5zaW9u
LWltcGxpY2l0X2ZpZ3VyZXMpCgkqIFthYmJyZXZpYXRpb25zXShodHRwczovL3BhbmRvYy5v
cmcvTUFOVUFMLmh0bWwjZXh0ZW5zaW9uLWFiYnJldmlhdGlvbnMpCgkqIFtpbmxpbmVfbm90
ZXNdKGh0dHBzOi8vcGFuZG9jLm9yZy9NQU5VQUwuaHRtbCNleHRlbnNpb24taW5saW5lX25v
dGVzKQoqIGNvZGUgaW5qZWN0aW9uCgkqIFtyYXdfaHRtbF0oaHR0cHM6Ly9wYW5kb2Mub3Jn
L01BTlVBTC5odG1sI2V4dGVuc2lvbi1yYXdfaHRtbCkKCSogW3Jhd190ZXhdKGh0dHBzOi8v
cGFuZG9jLm9yZy9NQU5VQUwuaHRtbCNleHRlbnNpb24tcmF3X3RleCkKCmBwYW5kb2NgIHN1
cHBvcnRzCltlcXVhdGlvbnNdKGh0dHBzOi8vcGFuZG9jLm9yZy9NQU5VQUwuaHRtbCNleHRl
bnNpb24tdGV4X21hdGhfZG9sbGFycykKcmVuZGVyZWQgaW5saW5lIGFuZCBzaW5nbGUtbGlu
ZSBpbiB0ZXgtc3R5bGUgdXNpbmcgYCQuLi4kYCBhbmQgYCQkLi4uJCRgLApbYmlibGlvZ3Jh
cGh5XShodHRwczovL3BhbmRvYy5vcmcvTUFOVUFMLmh0bWwjY2l0YXRpb25zKQp1c2luZyB0
aGUgYC0tY2l0ZXByb2NgIG9wdGlvbiwKW3NlY3Rpb24gbnVtYmVyaW5nXShodHRwczovL3Bh
bmRvYy5vcmcvTUFOVUFMLmh0bWwjZXh0ZW5zaW9uLWhlYWRlcl9hdHRyaWJ1dGVzKQp1c2lu
ZyB0aGUgYC0tbnVtYmVyLXNlY3Rpb25zYCBvcHRpb24gYW5kClt0YWJsZSBvZiBjb250ZW50
c10oaHR0cHM6Ly9wYW5kb2Mub3JnL01BTlVBTC5odG1sI29wdGlvbi0tdG9jKQp1c2luZyB0
aGUgYC0tdGFibGUtb2YtY29udGVudHNgIG9wdGlvbi4KCmBwYW5kb2NgIHN1cHBvcnRzIFtg
eG5vc2BdKGh0dHBzOi8vZ2l0aHViLmNvbS90b21kdWNrL3BhbmRvYy14bm9zKSBmaWx0ZXJz
CmZvciByZWZlcmVuY2luZyBkb2N1bWVudCBjb250ZW50IGxpa2UKW2ZpZ3VyZXNdKGh0dHBz
Oi8vZ2l0aHViLmNvbS90b21kdWNrL3BhbmRvYy1maWdub3MjdXNhZ2UpLApbZXF1YXRpb25z
XShodHRwczovL2dpdGh1Yi5jb20vdG9tZHVjay9wYW5kb2MtZXFub3MjdXNhZ2UpLApbdGFi
bGVzXShodHRwczovL2dpdGh1Yi5jb20vdG9tZHVjay9wYW5kb2MtdGFibGVub3MjdXNhZ2Up
LApbc2VjdGlvbnNdKGh0dHBzOi8vZ2l0aHViLmNvbS90b21kdWNrL3BhbmRvYy1zZWNub3Mj
dXNhZ2UpCmJ5IHVzaW5nIHRoZSBgLS1maWx0ZXIgcGFuZG9jLXhub3NgIG9wdGlvbi4KYHhu
b3NgIGludGVncmF0ZXMgY2xldmVyIHJlZmVyZW5jZXMsIHdoaWNoIG1lYW5zICJGaWcuIiwg
IlNlYy4iLCAiRXEuIgphbmQgIlRhYi4iIGFyZSBhZGRlZCBhdXRvbWF0aWNhbGx5IHRvIHRo
ZSBjb3JyZXNwb25kaW5nIGVsZW1lbnQuCklmIHRoZSBwcmVmaXggaXMgdG8gYmUgb21pdHRl
ZCwgdGhlIHJlZmVyZW5jZSBpcyB3cml0dGVuIGFzCmBcIUByZWY6bGFiZWxgLgoKIyMjIyBF
eGFtcGxlIHstfQpgYGBtZAojIyBSZWZlcmVuY2VkIFNlY3Rpb24geyNzZWM6bGFiZWx9CgpU
aGlzIGlzIGEgcmVmZXJlbmNlIHRvIEBzZWM6bGFiZWwuCgohW1RoaXMgaXMgdGhlIGNhcHRp
b25dKGRhdGE6aW1hZ2UvcG5nO2Jhc2U2NCxpVkJPUncwS0dnb0FBQUFOUwpVaEVVZ0FBQUFV
QUFBQUZDQVlBQUFDTmJ5YmxBQUFBSEVsRVFWUUkxMlA0Ly84L3czOEdJQVhESUJLRTBESAp4
Z2xqTkJBQU85VFhMMFk0T0h3QUFBQUJKUlU1RXJrSmdnZz09KXsjZmlnOmxhYmVsfQoKVGhp
cyBpcyBhIHJlZmVyZW5jZSB0byBAZmlnOmxhYmVsLgoKQSAgfEIgIHxDICB8RAotLS18LS0t
fC0tLXwtLS0KMDAwfDExMXw0NDR8NTU1CjIyMnwzMzN8NjY2fDc3NwoKVGFibGU6IFRoaXMg
aXMgdGhlIGNhcHRpb24geyN0Ymw6bGFiZWx9CgpUaGlzIGlzIGEgcmVmZXJlbmNlIHRvIEB0
Ymw6bGFiZWwuCgokJFxtYm94e2V9XntcbWJveHtpfVxwaX0rMT0wJCR7I2VxOmxhYmVsfQoK
VGhpcyBpcyBhIHJlZmVyZW5jZSB0byBAZXE6bGFiZWwuCgpUaGlzIGlzIGEgY2l0YXRpb24g
W0BNdWxsZXIxOTkzXS4KYGBgCgpUaGUgZmlsZSBgbWFya3kuYmliYCBpcyBzcGVjaWZpZWQg
aW4gdGhlIG1ldGEgZGF0YSBpbiB0aGUgZnJvbnQKbWF0dGVyIG9mIHRoZSBNYXJrZG93biB0
ZXh0LgoKIyMgUmVmZXJlbmNlZCBTZWN0aW9uIHsjc2VjOmxhYmVsfQoKVGhpcyBpcyBhIHJl
ZmVyZW5jZSB0byBAc2VjOmxhYmVsLgoKIVtUaGlzIGlzIHRoZSBjYXB0aW9uXShkYXRhOmlt
YWdlL3BuZztiYXNlNjQsaVZCT1J3MEtHZ29BQUFBTlNVaEVVZ0FBQUFVQUFBQUZDQVlBQUFD
TmJ5YmxBQUFBSEVsRVFWUUkxMlA0Ly84L3czOEdJQVhESUJLRTBESHhnbGpOQkFBTzlUWEww
WTRPSHdBQUFBQkpSVTVFcmtKZ2dnPT0peyNmaWc6bGFiZWx9CgpUaGlzIGlzIGEgcmVmZXJl
bmNlIHRvIEBmaWc6bGFiZWwuCgpBICB8QiAgfEMgIHxECi0tLXwtLS18LS0tfC0tLQowMDB8
MTExfDQ0NHw1NTUKMjIyfDMzM3w2NjZ8Nzc3CgpUYWJsZTogVGhpcyBpcyB0aGUgY2FwdGlv
bi4geyN0Ymw6bGFiZWx9CgpUaGlzIGlzIGEgcmVmZXJlbmNlIHRvIEB0Ymw6bGFiZWwuCgok
JFxtYm94e2V9XntpXHBpfSsxPTAkJHsjZXE6bGFiZWx9CgpUaGlzIGlzIGEgcmVmZXJlbmNl
IHRvIEBlcTpsYWJlbC4KClRoaXMgaXMgYSBjaXRhdGlvbiBbQE11bGxlcjE5OTNdLgoKIyBS
ZWZlcmVuY2VzCg==
'''
pack_marky_bib = '''
QGFydGljbGV7TXVsbGVyMTk5MywKICAgIGF1dGhvciAgPSB7UGV0ZXIgTXVsbGVyfSwKICAg
IHRpdGxlICAgPSB7VGhlIHRpdGxlIG9mIHRoZSB3b3JrfSwKICAgIGpvdXJuYWwgPSB7VGhl
IG5hbWUgb2YgdGhlIGpvdXJuYWx9LAogICAgeWVhciAgICA9IHsxOTkzfSwKICAgIG51bWJl
ciAgPSB7Mn0sCiAgICBwYWdlcyAgID0gezIwMS0yMTN9LAogICAgbW9udGggICA9IHs3fSwK
ICAgIG5vdGUgICAgPSB7QW4gb3B0aW9uYWwgbm90ZX0sCiAgICB2b2x1bWUgID0gezR9Cn0K
'''
pack__gitignore = '''
YnVpbGQvCmh0bWwvCg==
'''

###!!!:::marky_pack_data:::!!!###
########################################################################
# SECTION IS AUTO-PACKAGED USING ./marky.py --pack --force
########################################################################

########################################################################

def _marky_front_join(y, text):
	return """---\n%s\n---\n%s""" % (
		yaml.dump(y, allow_unicode=True, default_flow_style=False),
		text
	)

def _marky_front_split(t):
	global _MARKY_EXEC_DICT
	if not t.startswith("---\n"):
		return dict(), mark, 0
	y = t.split("---\n")[1]
	meta_lines = len(y.split("\n")) + 2
	mark = "---\n".join(t.split("---\n")[2:])
	print("---\n" + y + "---", flush=True)
	data = dict()
	try:
		data = yaml.safe_load(y)
	except Exception as ex:
		print("# YAML ERROR", type(ex), str(ex))
		sys.exit(1)
	return data, mark, meta_lines

########################################################################

def _marky_mdtext_print(*args, sep=" ", shift="", crop=False, ret=False):
	global _MARKY_EXEC_QUIET
	global _MARKY_EXEC_TEXT
	global _MARKY_EXEC_APPEND
	if len(args) == 0:
		if _MARKY_EXEC_APPEND == False: _MARKY_EXEC_TEXT.append("")
		_MARKY_EXEC_APPEND = False
	else:
		if ret: return _marky_mdtext_ret(args[0], shift, crop)
		if crop or shift != "":
			_marky_mdtext_crop(args[0], shift, crop)
			if args[-1] == _marky_mdtext_print:
				_MARKY_EXEC_APPEND = True
			return
		exec_append_new = False
		if args[-1] == _marky_mdtext_print:
			exec_append_new = True
			args = args[0:-1]
		text = sep.join([str(i) for i in args])
		if _MARKY_EXEC_APPEND and len(_MARKY_EXEC_TEXT) > 0:
			_MARKY_EXEC_TEXT[-1] += text
		else:
			_MARKY_EXEC_TEXT.append(text)
		_MARKY_EXEC_APPEND = exec_append_new
		if not _MARKY_EXEC_QUIET: print(text, end="" if _MARKY_EXEC_APPEND else "\n", flush=True)

def _marky_mdtext_crop(arg, shift, crop):
	global _MARKY_EXEC_TEXT
	global _MARKY_EXEC_APPEND
	if not type(arg) is str:
		arg = str(arg)
	arg = arg.split("\n")
	if crop:
		if len(arg[0].strip()) == 0:
			arg = arg[1:]
		if len(arg[-1].strip()) == 0:
			arg = arg[:-1]
	n = len(arg[0]) - len(arg[0].lstrip())
	for i in arg:
		if crop and len(i[0:n].lstrip()) == 0:
			i = i[n:]
		_MARKY_EXEC_TEXT.append(shift + i)

def _marky_mdtext_ret(arg, shift="", crop=True):
	if not type(arg) is str:
		arg = str(arg)
	text = []
	arg = arg.split("\n")
	if crop:
		if len(arg[0].strip()) == 0:
			arg = arg[1:]
		if len(arg[-1].strip()) == 0:
			arg = arg[:-1]
	n = len(arg[0]) - len(arg[0].lstrip())
	for i in arg:
		if crop and len(i[0:n].lstrip()) == 0:
			i = i[n:]
		text.append(shift + i)
	return "\n".join(text)

########################################################################

class _marky_fmtcall:
	def __init__(self, name, fmtc):
		self.name = name
		self.fmtc = fmtc
	def __call__(self, *args, **kwargs):
		text = "<<?html "
		f = getattr(self.fmtc.html, self.name)
		if callable(f):
			v = f(*args, **kwargs)
			if type(v) is str: text += v
		elif type(f) is str:
			text += f.format(*args, **kwargs)
		text += " html?>>"
		text += "<<?pdf "
		f = getattr(self.fmtc.pdf, self.name)
		if callable(f):
			v = f(*args, **kwargs)
			if type(v) is str: text += v
		elif type(f) is str:
			text += f.format(*args, **kwargs)
		text += " pdf?>>"
		return text

class _marky_fmtcode:
	def __init__(self, pdf=None, html=None):
		if not html is None: self.html = html
		if not pdf is None: self.pdf = pdf
	def __call__(self, *args, **kwargs):
		text = "<<?html "
		f = self.html
		if callable(f):
			v = f(*args, **kwargs)
			if type(v) is str: text += v
		elif type(f) is str:
			text += f.format(*args, **kwargs)
		text += " html?>>"
		text += "<<?pdf "
		f = self.pdf
		if callable(f):
			v = f(*args, **kwargs)
			if type(v) is str: text += v
		elif type(f) is str:
			text += f.format(*args, **kwargs)
		text += " pdf?>>"
		return text
	def __getattr__(self, name):
		return _marky_fmtcall(name, self)

########################################################################

def _marky_rebrace(t):
	t = t.replace("{{", "<<brace?")
	t = t.replace("}}", "?brace>>")
	t = t.replace("{", "{{")
	t = t.replace("}", "}}")
	t = t.replace("<<brace?", "{")
	t = t.replace("?brace>>", "}")
	return t

def _marky_code_text(t, fstring=True):
	if fstring:
		if not '"""' in t and not t.endswith('"'):
			return '___(rf"""' + _marky_rebrace(t) + '""", ___); '
		elif not "'''" in t and not t.endswith("'"):
			return "___(rf'''" + _marky_rebrace(t) + "''', ___); "
		else:
			print("# ERROR", "python code contains \"\"\" as well as '''.")
			sys.exit(1)
	else:
		if not '"""' in t and not t.endswith('"'):
			return '___(r"""' + t + '""", ___); '
		elif not "'''" in t and not t.endswith("'"):
			return "___(r'''" + t + "''', ___); "
		else:
			print("# ERROR", "python code contains \"\"\" as well as '''.")
			sys.exit(1)

def _marky_paste_code(t):
	show_code = False
	if t.startswith("!"):
		t = t[1:]
		show_code = True
	if show_code:
		return _marky_code_text(t, fstring=False) + t
	return t

def _marky_meta_merge(old, front):
	meta = {}
	meta.update(old)
	try:
		for k, v in front.items():
			if k in meta:
				print("<!-- field exists, skip yaml %s --!>" % k)
			else:
				meta[k] = v
	except Exception as ex:
		print("# META MERGE ERROR", type(ex), str(ex))
		sys.exit(1)
	return meta

def _marky_run(fname, meta, inbase):
	global _MARKY_EXEC_DICT
	with open(fname, "r") as h:
		front, t, meta_lines = _marky_front_split(h.read())
	meta = _marky_meta_merge(meta, front)
	p = 0
	r = ""
	while True:
		p0 = t.find("<?", p)
		if p0 > -1:
			if p0 > 0: r += _marky_code_text(t[p:p0])
			p1 = t.find("?>", p0)
			if p1 > -1:
				code = t[p0+2:p1]
				r += _marky_paste_code(code)
				p = p1 + 2
			else:
				print("# ERROR", "missing ?>")
				sys.exit(1)
		else:
			r += _marky_code_text(t[p:])
			break
	for a, b, c, count in [
		("", "<%s?", "", 1),
		("", "?%s>", "", 1),
		("", "{%s", "{", 3),
		("}", "%s}", "", 3)
	]:
		for j in reversed(range(1, count+1)):
			for i in range(3):
				X = "\\"*(i + 1)
				Y = "\\"*(i + 0)
				r = r.replace(a + (b % X)*j + c, a + (b % Y)*j + c)
	open(_MARKY_BUILD_DIR + inbase + ".py", "w").write(r)
	try:
		exec(r, _MARKY_EXEC_DICT, None)
	except Exception as ex:
		_marky_print_trace(ex, meta_lines, t)
		sys.exit(1)
	return meta

def _marky_print_trace(ex, mlines, code):
	print("# TRACEBACK")
	import traceback
	traceback.print_tb(ex.__traceback__)
	print("# PYTHON ERROR")
	print(type(ex), str(ex))
	if ex.filename == "<string>":
		print("# ERROR LOCATION")
		code = code.split("\n")
		for i in range(max(0, ex.lineno-5), min(len(code), ex.lineno+5)):
			print("*" if i + 1 == ex.lineno else " ", "%03d" % i, code[i])

########################################################################

def _marky_meta_link(front, link):
	flink = {}
	try:
		for k, v in front.items():
			if "--" in k: continue
			if not k in flink:
				flink[k] = v
			else:
				print("<!-- field exists, skip yaml %s --!>" % k)
		for k, v in front.items():
			if not "--" in k: continue
			x = k.split("--")
			if x[-1] in _MARKY_FORMAT:
				if x[-1] == link:
					k = "--".join(x[0:-1])
					if k in flink:
						print("<!-- field link, merge yaml %s --!>" % k)
						if type(v) is list: flink[k].extend(v)
						if type(v) is dict: flink[k].update(v)
						if type(v) is str: flink[k] += " " + v
						else: flink[k] = v
					else:
						print("<!-- field link, set yaml %s --!>" % k)
						flink[k] = v
	except Exception as ex:
		print("# META LINK ERROR", type(ex), str(ex))
		sys.exit(1)
	return flink

def _marky_link(front, md_text, link):
	md_text = md_text.replace(".???", "." + link)
	md_text = md_text.replace(r".\???", r".???")
	md_text = md_text.replace(r".\\???", r".\???")
	lsep = 3
	len_args = len(link) + 1
	c = 0
	newtext = ""
	p = md_text.find("<<?")
	while p >= 0:
		q = md_text.find("?>>", p + lsep)
		if q > 0:
			newtext += md_text[c:p]
			expr = md_text[p+lsep:q]
			if expr.startswith(link) and expr.endswith(link):
				newtext += expr[len_args:-len_args]
			c = q + lsep
			p = md_text.find("<<?", c)
		else:
			p = md_text.find("<<?", p + lsep)
	newtext += md_text[c:]
	flink = _marky_meta_link(front, link)
	return _marky_front_join(flink, newtext)

def _marky_write_build(inbase, outdir, front, mark):
	os.makedirs(_MARKY_BUILD_DIR + outdir, exist_ok=True)
	if not mark is None:
		open(_MARKY_BUILD_DIR + inbase + ".md", "w").write(_marky_front_join(front, mark))
		for fmt in _MARKY_FORMAT:
			open(_MARKY_BUILD_DIR + inbase + "." + fmt + ".md", "w").write(_marky_link(front, mark, fmt))

	with open(_MARKY_BUILD_DIR + inbase + ".make", "w") as fhnd:
		fhnd.write(f"""# auto-generated
all_md:=$(all_md) {_MARKY_MD_DIR+inbase}.md

{_MARKY_BUILD_DIR+inbase}.md: {_MARKY_MD_DIR+inbase}.md
	mkdir -p "{_MARKY_BUILD_DIR+outdir}"
	ln -snf ../{_MARKY_DATA_DIR} {_MARKY_BUILD_DIR+_MARKY_DATA_DIR}
	./marky.py --base="{inbase}.md"

.PHONY: build/{inbase}
build/{inbase}: {_MARKY_BUILD_DIR+inbase}.md

all_build:=$(all_build) build/{inbase}
"""
		)
		if "pdf" in _MARKY_FORMAT:
			fhnd.write(f"""
{_MARKY_BUILD_DIR+inbase}.tex: {_MARKY_BUILD_DIR+inbase}.pdf.md {_MARKY_MD_DIR+inbase}.md
	mkdir -p "{_MARKY_BUILD_DIR+outdir}"
	./pandoc-run tex {_MARKY_BUILD_DIR+inbase}.pdf.md {_MARKY_BUILD_DIR+inbase}.tex

all_tex:=$(all_tex) {_MARKY_BUILD_DIR+inbase}.tex
"""
			)
		for fmt in _MARKY_FORMAT:
			fhnd.write(f"""
{_MARKY_BUILD_DIR+inbase}.{fmt}.md: {_MARKY_BUILD_DIR+inbase}.md

{fmt}/{inbase}.{fmt}: {_MARKY_BUILD_DIR+inbase}.{fmt}.md {_MARKY_MD_DIR+inbase}.md
	mkdir -p "{fmt}/{outdir}"
	./pandoc-run {fmt} {_MARKY_BUILD_DIR+inbase}.{fmt}.md {fmt}/{inbase}.{fmt}

.PHONY: {fmt}/{inbase}
{fmt}/{inbase}: {fmt}/{inbase}.{fmt}

all_{fmt}:=$(all_{fmt}) {fmt}/{inbase}.{fmt}
"""
			)

########################################################################

def _marky_pack_b64enc(x, n=72):
	x = base64.b64encode(bytes(x, "utf-8")).decode("ascii")
	return "\n".join([x[i:i+n] for i in range(0, len(x), n)])

def _marky_pack_b64dec(x):
	return base64.b64decode(bytes(x.replace("\n", ""), "ascii")).decode("utf-8")

def _marky_load_pack(i):
	return _marky_pack_b64dec(eval("pack_" + i.split("/")[-1].replace(".", "_").replace("-", "_")))

def _marky_pack_write_file(fname, force=False):
	if not os.path.exists(fname) or force:
		print("# WRITE", fname)
		open(fname, "w").write(_marky_load_pack("./" + fname))
	else:
		print("# EXISTS", fname)

def _marky_store_pack(i, ftext):
	return "pack_%s = '''\n%s\n'''\n" % (i.split("/")[-1].replace(".", "_").replace("-", "_"), _marky_pack_b64enc(ftext))

def _marky_pack_read_file(fname):
	return _marky_store_pack("./" + fname, open(fname, "r").read())

########################################################################

_MARKY_FORMAT = ["html", "pdf"]
_MARKY_BUILD_DIR = "build/"  #< WITH trailing /
_MARKY_MD_DIR = "md/"  #< WITH trailing /
_MARKY_DATA_DIR = "data" #< no trailing /
_MARKY_PACK_DIRS = [
	_MARKY_BUILD_DIR,
	_MARKY_DATA_DIR,
	_MARKY_MD_DIR
]
_MARKY_PACK_FILES = [
	"Makefile",
	"pandoc-run",
	"md/marky.md",
	"data/marky.bib",
	".gitignore"
]
_MARKY_EXEC_QUIET = False
_MARKY_EXEC_DICT = dict()
_MARKY_EXEC_TEXT = list()
_MARKY_EXEC_APPEND = False
_MARKY_EXEC_DICT["___"] = _marky_mdtext_print
_MARKY_EXEC_DICT["fmtcode"] = _marky_fmtcode

########################################################################

if __name__ == "__main__":

	parser = argparse.ArgumentParser(add_help=False)

	parser.add_argument("--version", action='store_true', help="version is v" + ".".join([str(i) for i in _MARKY_VERSION]))
	parser.add_argument("--help", action='store_true', help="show this help message")
	parser.add_argument("--base", type=str, default="", help="path to input markdown text")
	parser.add_argument("--init", action='store_true', help="create dirs (" + ", ".join(_MARKY_PACK_DIRS) + ") and files (" + ", ".join(_MARKY_PACK_FILES) + ")")
	parser.add_argument("--force", action='store_true', help="force overwrite of files for --init/--pack")
	parser.add_argument("--pack", action='store_true', help="pack files (" + ", ".join(_MARKY_PACK_FILES) + ") into marky.py.pack source")
	parser.add_argument("--scan", action='store_true', help="create build/*.make from md/*.md")
	parser.add_argument("--quiet", action='store_true', help="do not show Markdown output")

	# ~ args, uargs = parser.parse_known_args()
	args = parser.parse_args()

	sys.path.append(".")

########################################################################

	if args.version:
		print(".".join([str(i) for i in _MARKY_VERSION]))
		sys.exit(0)
	elif args.help or len(sys.argv) == 1:
		parser.print_help()
		sys.exit(0)
	elif args.init:
		for i in _MARKY_PACK_DIRS:
			if not os.path.exists(i):
				print("# MKDIR", i)
				os.mkdir(i)
			else:
				print("# EXISTS", i)
		for i in _MARKY_PACK_FILES:
			_marky_pack_write_file(i, args.force)
		print("# USAGE")
		print("make help")
		sys.exit(0)
	elif args.pack:
		print("# PACK", ", ".join(_MARKY_PACK_FILES))
		marky_text = open(sys.argv[0], "r").read()
		head, src, tail = tuple(marky_text.split("\n###!!!:::marky_pack_data:::!!!###\n"))
		src = "".join([_marky_pack_read_file(i) for i in _MARKY_PACK_FILES])
		marky_text = "\n###!!!:::marky_pack_data:::!!!###\n".join([head, src, tail])
		open(sys.argv[0] + ".pack", "w").write(marky_text)
		if args.force:
			print("# UPDATE OF `marky` FORCED")
			print("# -----------------------")
			print("# mv marky.py.pack marky.py")
			print("# chmod 775 marky.py")
			os.replace("marky.py.pack", "marky.py")
			os.chmod("marky.py", 0o775)
		else:
			print("# MANUAL UPDATE NEEDED")
			print("# --------------------")
			print("mv marky.py.pack marky.py")
			print("chmod +x marky.py")
		sys.exit(0)
	elif args.scan:
		for i in glob.glob("md/**/*.md", recursive=True):
			inbase = i[3:-3]
			outdir = "/".join(inbase.split("/")[0:-1])
			print("# WRITE", _MARKY_BUILD_DIR + inbase + ".make")
			_marky_write_build(inbase, outdir, None, None)
		sys.exit(0)
		pass
	elif args.force:
		print("# ERROR", "--force can only be used with --pack/--init")
		sys.exit(1)
	elif args.quiet:
		_MARKY_EXEC_QUIET = True

########################################################################

	infile = _MARKY_MD_DIR + args.base
	if len(args.base) == 0:
		print("# ERROR", "empty base: use --base file.md")
		sys.exit(1)
	if not os.path.exists(infile):
		print("# ERROR", "wrong base %s: file not found %s" % (args.base, infile))
		sys.exit(1)
	inbase = args.base if not "." in args.base.split("/")[-1] else ".".join(args.base.split(".")[0:-1])
	outdir = "/".join(inbase.split("/")[0:-1])

	if os.path.exists(_MARKY_BUILD_DIR):
		front = _marky_run(infile, {}, inbase)
		mark = "\n".join(_MARKY_EXEC_TEXT)
		_marky_write_build(inbase, outdir, front, mark)
	else:
		print("# ERROR", "no build dir: mkdir build")
		sys.sys.exit(1)
