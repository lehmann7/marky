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
aW5zZXJ0ZWQgaW50byB0aGUgcmVzdWx0aW5nIE1hcmtkb3duLgoKIyBRdWljayBTdGFydAoK
IyMgYG1hcmt5YCBEZXBlbmRlbmNpZXMKCmBtYXJreWAgdXNlcyBbcGFuZG9jXShodHRwczov
L3d3dy5wYW5kb2Mub3JnLykgZm9yIHJlbmRlcmluZyBgaHRtbGAgYW5kIGBwZGZgLgoKYG1h
cmt5YCBkZXBlbmRzIG9uIGBwYW5kb2NgIGFuZCBgcHl5YW1sYC4gYHBhbmRvY2AgaXMgdXNl
ZCBmb3IgcmVuZGVyaW5nCnRoZSBNYXJrZG93biBpbnRvIGBodG1sYCBhbmQgYHBkZmAuIGBw
YW5kb2NgIHN1cHBvcnRzIHZhcmlvdXMgTWFya2Rvd24KZXh0ZW5zaW9ucyBhbGxvd2luZyBm
b3Igc2NpZW50aWZpYyB3cml0aW5nIHVzaW5nIGVxdWF0aW9ucywgZmlndXJlcywKdGFibGVz
LCBjaXRhdGlvbnMgYW5kIGNvcnJlc3BvbmRpbmcgcmVmZXJlbmNpbmcgbWVjaGFuaXNtIGZv
ciB0aGUgbGF0dGVyLgpgcHl5YW1sYCBpcyB1c2VkIGZvciBwYXJzaW5nIG1ldGEgZGF0YSBp
biB0aGUgZnJvbnQgbWF0dGVyIG9mIHRoZQpNYXJrZG93biB0ZXh0LgoKYG1hcmt5YCByZW5k
ZXJzIHRoZSBkb2N1bWVudGF0aW9uIHVzaW5nIGBwYW5kb2NgIGludG8gYGh0bWxgIGFuZApg
cGRmYCBieSBpbnZva2luZyBgbWFrZSBhbGxgLiBgbWFya3lgIHJlcXVpcmVzCmluc3RhbGxp
bmcgdGhlIGRlcGVuZGVuY2llcyBgcHl0aG9uLXB5eWFtbGAsIGBwYW5kb2NgIGFuZCBgcGFu
ZG9jLXhub3NgCihgcGFuZG9jLWZpZ25vc2AsIGBwYW5kb2Mtc2Vjbm9zYCwgYHBhbmRvYy1l
cW5vc2AsIGBwYW5kb2MtdGFibGVub3NgKS4KVGhlIGRldGFpbHMgYXJlIHNob3duIGluIHRo
ZSBNYWtlZmlsZSBoZWxwIG1lc3NhZ2UuCgojIyBgbWFya3lgIFdvcmtmbG93CgpXb3JrZmxv
dyBmb3IgY3JlYXRpbmcgYGh0bWxgIG9yIGBwZGZgIHVzaW5nIGBtYXJreWAKCjEuIHVzZXIg
d3JpdGVzIGEgTWFya2Rvd24gdGV4dCBmaWxlIGFuZCBwbGFjZXMgaXQgaW4gYG1kLyoubWRg
CmRpcmVjdG9yeSB3aXRoIHRoZSBleHRlbnNpb24gYC5tZGAuCjIuIGBtYXJreWAgdHJhbnNm
b3JtcyB0aGUgZmlsZXMgaW4gYG1kLyoubWRgIGludG8gcmVndWxhciBNYXJrZG93biB0ZXh0
CmFuZCBwbGFjZXMgdGhlIHRyYW5zZm9ybWVkIGZpbGVzIGluIGBidWlsZC9gLgozLiB0aGUg
cmVndWxhciBNYXJrZG93biB0ZXh0IGluIHRoZSBmaWxlcyBgYnVpbGQvKi5tZGAgaXMgcmVu
ZGVyZWQgaW50bwpgaHRtbGAgYW5kIGBwZGZgIHVzaW5nIGBwYW5kb2NgLgoKVGhlIHRocmVl
IHN0ZXBzIGFyZSBpbXBsZW1lbnRlZCBpbiBhIE1ha2VmaWxlLgoKIyMgRG93bmxvYWQgYW5k
IEluaXRpYWxpemUKCmBtYXJreWAgaXMgc3VwcGxpZWQgYXMgYSBzaW5nbGUtZmlsZSBzY3Jp
cHQgd2hpY2ggYXV0b21hdGljYWxseQpzZXRzIHVwIHRoZSBwcm9qZWN0IHN0cnVjdHVyZSBj
b250YWluaW5nIGFsbCBzY3JpcHRzCnJlcXVpcmVkIGZvciBwcm9jZXNzaW5nIGFuZCByZW5k
ZXJpbmcgTWFya2Rvd24uCgpGb3IgZXhhbXBsZSwgZG93bmxvYWQgYG1hcmt5YCBmcm9tIGdp
dGh1Yi4KYGBgYmFzaApnaXQgY2xvbmUgaHR0cHM6Ly9sZWhtYW5uNy5naXRodWIuY29tL21h
cmt5LmdpdApjZCBtYXJreQpgYGAKCkFmdGVyIGRvd25sb2FkLCB0aGUgYG1hcmt5YCBlbnZp
cm9ubWVudCBpcyBpbml0aWFsaXplZCB1c2luZyBgbWFya3lgLgpgYGBiYXNoCi4vbWFya3ku
cHkgLS1pbml0CiMgbWtkaXIgYnVpbGQvCiMgbWtkaXIgZGF0YQojIG1rZGlyIG1kLwojIFdS
SVRFIE1ha2VmaWxlCiMgV1JJVEUgcGFuZG9jLXJ1bgojIFdSSVRFIG1kL21hcmt5Lm1kCiMg
V1JJVEUgLmdpdGlnbm9yZQojIFVTQUdFCm1ha2UgaGVscApgYGAKCiMjIGBtYXJreWAgRW52
aXJvbm1lbnQKCkR1cmluZyBpbml0aWFsaXphdGlvbiwgYG1hcmt5YCBjcmVhdGVzIGRpcmVj
dG9yaWVzIGFuZCBmaWxlcy4KQWZ0ZXIgaW5pdGlhbGl6YXRpb24sIHRoZSBmb2xsb3dpbmcg
c3RydWN0dXJlIGlzIGF1dG8tZ2VuZXJhdGVkCmluIHRoZSBwcm9qZWN0IGRpcmVjdG9yeS4K
YGBgYmFzaAptYWtlIGhlbHAKPD8KX19fKHRleHRfcHJvYygibWFrZSB0cmVlIikpCj8+CmBg
YAoKVGhlIHNjcmlwdCBgcGFuZG9jLXJ1bmAgY2FuIGJlIGFkanVzdGVkIGluIGNhc2Ugc3Bl
Y2lmaWMKYHBhbmRvY2Agb3B0aW9ucyBhcmUgcmVxdWlyZWQgZm9yIHJlbmRlcmluZyB0aGUg
YGh0bWxgIGFuZCBgcGRmYCBkb2N1bWVudHMuCgojIyBEb2N1bWVudCBSZW5kZXJpbmcKCkJ5
IGludm9raW5nIGBtYWtlIGFsbGAgYWxsIGZpbGVzIGBtZC8qLm1kYCBhcmUgdHJhbnNmb3Jt
ZWQKaW50byBjb3JyZXNwb25kaW5nIGBodG1sLyouaHRtbGAgYW5kIGBwZGYvKi5wZGZgIGZp
bGVzLiBCeQppbnZva2luZyBgbWFrZSBodHRwZGAgYSBweXRob24gd2ViIHNlcnZlciBpcyBz
dGFydGVkIGluIGBodG1sL2AuCgpBbGwgdXNlci1nZW5lcmF0ZWQgTWFya2Rvd24gY29udGVu
dCBnb2VzIGludG8gYG1kLypgIHVzZXItZ2VuZXJhdGVkCmRhdGEgZmlsZXMgZ28gaW50byBg
ZGF0YS8qYC4KCioqQVRURU5USU9OOioqIFRoZSBmaWxlcyBpbiB0aGUgZGlyZWN0b3JpZXMg
YGJ1aWxkLypgIGFyZQoqKmF1dG8tZ2VuZXJhdGVkKiouIEFsbCB1c2VyIGZpbGVzIGhhdmUg
dG8gYmUgcGxhY2VkIGluc2lkZSB0aGUKZGlyZWN0b3J5IGBtZC8qYC4gSW52b2tpbmcgYG1h
a2UgY2xlYW5gIHdpbGwgKipkZWxldGUgYWxsIGZpbGVzKioKaW4gYGh0bWwvYCwgYGJ1aWxk
L2AgYW5kIGBwZGYvYC4KCiMjIEludGVncmF0ZWQgRG9jdW1lbnRhdGlvbgoKYG1hcmt5YCBo
YXMgYW4gaW50ZWdyYXRlZCBlbnZpcm9ubWVudC4gVXNpbmcgYG1ha2UgaGVscGAgZGlzcGxh
eXMKYSBzaG9ydCBpbmZvIGFib3V0IHRoZSBgbWFya3lgIGRlcGVuZGVuY2llcywgbWFrZSB0
YXJnZXRzIGFuZApleGFtcGxlcy4KYGBgYmFzaAptYWtlIGhlbHAKPD8KX19fKHRleHRfcHJv
YygibWFrZSBoZWxwIikpCj8+CmBgYAoKIyBgbWFya3lgIEZlYXR1cmVzCgpQbGFjZSBhIG5l
dyBmaWxlIGluIGBtZC9maWxlLm1kYCBhbmQgcnVuIHRoZSBmb2xsb3dpbmcgY29tbWFuZHMu
CmBgYGJhc2gKdG91Y2ggbWQvZmlsZS5tZApgYGAKCmBtYXJreWAgZGlzY292ZXJzIHRoZSBu
ZXcgZG9jdW1lbnQgd2hlbiBpbnZva2luZyBgbWFrZSBzY2FuYC4KYGBgYmFzaAptYWtlIHNj
YW4KIyBXUklURSBidWlsZC9maWxlLm1ha2UKYGBgCgpgbWFya3lgIHJlbmRlcnMgYGh0bWxg
IGFuZCBgcGRmYCB1c2luZyBtYWtlIHRhcmdldHMuCmBgYGJhc2gKbWFrZSBodG1sL2ZpbGUK
bWFrZSBwZGYvZmlsZQpgYGAKCiMjIE1ldGEgRGF0YSBpbiBGcm9udCBNYXR0ZXIKCklmIGRv
Y3VtZW50IHN0YXJ0cyB3aXRoIGAtLS1gLCB5YW1sIGlzIHVzZWQgdG8gcGFyc2UKdGhlIGZy
b250IG1hdHRlciBibG9jayBkZWxpbWl0ZWQgYnkgYC0tLWAuCkFsbCBtZXRhIGRhdGEga2V5
cyB3aWxsIGJlIGV4cG9zZWQgaW50byB0aGUgcHl0aG9uIHNjb3BlIGFzIGEgbG9jYWwKdmFy
aWFibGUsIHVubGVzcyB0aGUgdmFyaWFibGUgYWxyZWFkeSBleGlzdHMuCgpgYGBtZAotLS0K
dGl0bGU6ICJNeSBEb2N1bWV0IgphdXRob3I6IC4uLgpkYXRlOiAyMDIyLTAxLTAxCi0tLQpU
aGUgdGl0bGUgb2YgdGhpcyBkb2N1bWVudCBpcyB7XHt0aXRsZX1cfS4KYGBgCgojIyBFbWJl
ZGRpbmcgUHl0aG9uIENvZGUKClB5dGhvbiBjb2RlIGJsb2NrcyBhcmUgZW1iZWRkZWQgaW50
byBNYXJrZG93biB1c2luZyBgPFw/Li4uP1w+YCBhbmQgYHtcey4uLn1cfWAuCkFsbCBjb2Rl
IGJsb2NrcyBzcGFuIG9uZSBsYXJnZSBzY29wZSBzaGFyaW5nIGZ1bmN0aW9ucyBhbmQgbG9j
YWwKdmFyaWFibGVzLiBNZXRhIGRhdGEgaXMgaW1wb3J0ZWQgZnJvbSBNYXJrZG93biBmcm9u
dCBtYXR0ZXIgYXMgbG9jYWwKdmFyaWFibGVzIGluIHRoZSBweXRob24gc2NvcGUuIFRoZSBg
aW1wb3J0YCBzdGF0ZW1lbnQgY2FuIGJlIHVzZWQgaW4KcHl0aG9uIGNvZGUgaW4gb3JkZXIg
dG8gYWNjZXNzIGluc3RhbGxlZCBweXRob24gcGFja2FnZXMgYXMgdXN1YWwuCgojIyMgVmlz
aWJsZSBDb2RlCgpVc2luZyBgPFw/IS4uLj9cPmAgY29kZSBpcyBleGVjdXRlZCBhbmQgYWxz
byBzaG93biBpbiBNYXJrZG93bi4KCiMjIyMgRXhhbXBsZSB7LX0KYGBgcHl0aG9uCjxcPyEK
eCA9IDQyICMgdmlzaWJsZSBjb2RlCnByaW50KCJIZWxsbyBjb25zb2xlISIpCj9cPgpgYGAK
CiMjIyMgUnVuIGFuZCBPdXRwdXQgey19CmBgYHB5dGhvbjw/IQp4ID0gNDIgIyB2aXNpYmxl
IGNvZGUKPz4KYGBgCgoqKkF0dGVudGlvbjoqKiBVc2luZyB0aGUgYHByaW50KClgIGZ1bmN0
aW9uIHRoZSB0ZXh0IHdpbGwgYmUgcHJpbnRlZAp0byB0aGUgY29uc29sZSBhbmQgKipub3Qq
KiBpbnNpZGUgdGhlIHJlc3VsdGluZyBNYXJrZG93biB0ZXh0LgoKIyMjIEhpZGRlbiBDb2Rl
CgpVc2luZyBgPFw/Li4uP1w+YCBjb2RlIGlzIGV4ZWN1dGVkIGJ1dCBub3Qgc2hvd24gaW4g
TWFya2Rvd24uCgojIyMjIEV4YW1wbGUgey19CmBgYHB5dGhvbgo8XD8KeCA9IDQxICMgaGlk
ZGVuIGNvZGUKX19fKGYiT3V0cHV0IHRvIE1hcmtkb3duLiB4ID0ge3h9ISIpCj9cPgpgYGAK
IyMjIyBSdW4gYW5kIE91dHB1dCB7LX0KYGBgcHl0aG9uCjw/CnggPSA0MSAjIGhpZGRlbiBj
b2RlCl9fXyhmIk91dHB1dCB0byBNYXJrZG93bi4geCA9IHt4fSEiKQo/PgpgYGAKCioqQXR0
ZW50aW9uOioqIFVzaW5nIHRoZSBgX19fKClgIGZ1bmN0aW9uIHRoZSB0ZXh0IHdpbGwgYmUg
cHJpbnRlZAppbnNpZGUgdGhlIHJlc3VsdGluZyBNYXJrZG93biB0ZXh0ICoqYW5kIG5vdCoq
IG9uIHRoZSBjb25zb2xlLgoKIyMgVGhlIGBfX18oKWAgRnVuY3Rpb24KClVzaW5nIHRoZSBg
cHJpbnQoKWAgc3RhdGVtZW50IHRoZSB0ZXh0IHdpbGwgYmUgcHJpbnRlZCB0byB0aGUgY29u
c29sZS4KV2hlbiB1c2luZyB0aGUgYF9fXygpYCBzdGF0ZW1lbnQgbmV3IE1hcmtkb3duIHRl
eHQgaXMKaW5zZXJ0ZWQgZHluYW1pY2FsbHkgaW50byB0aGUgZG9jdW1lbnQgZHVyaW5nIHBy
ZXByb2Nlc3NpbmcuCgojIyMjIEV4YW1wbGU6IExpbmUgQnJlYWsgey19CmBgYHB5dGhvbgo8
XD8KeCA9IDQwICMgaGlkZGVuIGNvZGUKX19fKCJPdXRwdXQgaW4iLCBfX18pCl9fXygic2lu
Z2xlIGxpbmUhICIsIF9fXykKX19fKGYieCA9IHt4fSIpCj9cPgpgYGAKIyMjIyBSdW4gYW5k
IE91dHB1dCB7LX0KYGBgYmFzaAo8Pwp4ID0gNDAgIyBoaWRkZW4gY29kZQpfX18oIk91dHB1
dCBpbiAiLCBfX18pCl9fXygic2luZ2xlIGxpbmUhICIsIF9fXykKX19fKGYieCA9IHt4fSIp
Cj8+CmBgYAoKIyMjIyBFeGFtcGxlOiBTaGlmdCwgQ3JvcCwgUmV0dXJuIHstfQpgYGBweXRo
b24KPFw/CnJlc3VsdCA9IF9fXygiIiIKICAgKiB0ZXh0IGlzIGNyb3BwZWQgYW5kIHNoaWZ0
ZWQKICAgICAgICAgKiBzaGlmdCBhbmQgY3JvcAogICAgICAgICAgICAqIGNhbiBiZSBjb21i
aW5lZAogICAgICAgICAgKiByZXR1cm5pbmcgdGhlIHJlc3VsdAoiIiIsIHNoaWZ0PSIjIyMj
IyMjIyIsIGNyb3A9VHJ1ZSwgcmV0PVRydWUpCl9fXyhyZXN1bHQpCj9cPgpgYGAKIyMjIyBS
dW4gYW5kIE91dHB1dCB7LX0KYGBgYmFzaAo8PwpyZXN1bHQgPSBfX18oIiIiCiAgICogdGV4
dCBpcyBjcm9wcGVkIGFuZCBzaGlmdGVkCiAgICAgICAgICogc2hpZnQgYW5kIGNyb3AKICAg
ICAgICAgICAgKiBjYW4gYmUgY29tYmluZWQKICAgICAgICAgICogcmV0dXJuaW5nIHRoZSBy
ZXN1bHQKIiIiLCBzaGlmdD0iIyMjIyMjIyMiLCBjcm9wPVRydWUsIHJldD1UcnVlKQpfX18o
cmVzdWx0KQo/PgpgYGAKCiMjIEFsZ29yaXRobWljIFRhYmxlIEV4YW1wbGUKCkB0Ymw6YWxn
dCBpcyBnZW5lcmF0ZWQgdXNpbmcgdGhlIGZvbGxvd2luZyBweXRob24gY2xvZGUgYmxvY2su
CgpgYGBweXRob248PyEKbiA9IDUKdGFibGUgPSAiIgpkZWMgPSBbIiolcyoiLCAiKiolcyoq
IiwgIn5+JXN+fiIsICJgJXNgIiwKICAgICAgIHIiJFx0aW1lc14lcyQiLCAiJFxpbmZ0eV8l
cyQiXQp0YWJsZSArPSAifCIuam9pbigiWCIqbikgKyAiXG4iICsgInwiLmpvaW4oIi0iKm4p
ICsgIlxuIgpmb3IgaSBpbiByYW5nZShuKToKCWZpbGwgPSBbY2hyKG9yZCgiQSIpKygyKmkr
MyprKSUyNikgZm9yIGsgaW4gcmFuZ2UoaSsxKV0KCWZpbGwgPSBbZGVjWyhsK2kpJWxlbihk
ZWMpXSVrIGZvciBsLCBrIGluIGVudW1lcmF0ZShmaWxsKV0KCXRleHQgPSBsaXN0KCIwIikq
bgoJdGV4dFsobj4+MSktKGk+PjEpOihuPj4xKSsoaT4+MSldID0gZmlsbAoJdGFibGUgKz0g
InwiLmpvaW4odGV4dCkgKyAiXG4iCj8+CmBgYAoKe3t0YWJsZX19CgpUYWJsZTogVGFibGUg
aXMgZ2VuZXJhdGVkIHVzaW5nIGNvZGUgYW5kIHRoZSBgX19fKClgIHN0YXRlbWVudC4geyN0
Ymw6YWxndH0KCiMjIElubGluZSBGb3JtYXR0ZWQgT3V0cHV0CgpUaGUgYHtcey4uLn1cfWAg
c3RhdGVtZW50IHVzZXMgc250YXggc2ltaWxhciB0byBweXRob24gYGZgLXN0cmluZ3MgZm9y
CmZvcm1hdHRlZCBvdXRwdXQgb2YgdmFyaWFibGVzIGFuZCByZXN1bHRzIG9mIGV4cHJlc3Np
b25zIGludG8gTWFya2Rvd24KdGV4dC4gVGhlIGBtYXJreWAgb3BlcmF0b3IgYHtcezxleHBy
ZXNzaW9uPls6PGZvcm1hdD5dfVx9YCB1c2VzIHRoZQpzeW50YXggb2YgW2BmYC1zdHJpbmdz
XShodHRwczovL2RvY3MucHl0aG9uLm9yZy8zL3JlZmVyZW5jZS9sZXhpY2FsX2FuYWx5c2lz
Lmh0bWwjZi1zdHJpbmdzKS4KCiMjIyMgRXhhbXBsZSAxIHstfQpgYGBiYXNoClRleHQgdGV4
dCB7XHt4fVx9IGFuZCB7XHsiLCIuam9pbihbc3RyKGkpIGZvciBpIGluIHJhbmdlKHgtMTAs
eCldKX1cfS4KYGBgCiMjIyMgT3V0cHV0IHstfQo+IFRleHQgdGV4dCB7e3h9fSBhbmQge3si
LCIuam9pbihbc3RyKGkpIGZvciBpIGluIHJhbmdlKHgtMTAseCldKX19LgoKIyMjIyBFeGFt
cGxlIDIgey19CmBgYHB5dGhvbjw/IQp4ID0gaW50KDEpCnkgPSBmbG9hdCgyLjMpCnogPSAw
CmEgPSBbMSwgMiwgM10KYiA9ICg0LCA1KQo/PgpgYGAKYGBgbWFya2Rvd24KVGhpcyBpcyBh
IHBhcmFncmFwaCBhbmQgeCBpcyB7XHt4OjAzZH1cfSBhbmQgeSBpcyB7XHt5Oi4yZn1cfS4K
T3RoZXIgY29udGVudCBpczogYSA9IHtce2F9XH0sIGIgPSB7XHtifVx9LgpgYGAKIyMjIyBP
dXRwdXQgey19Cj4gVGhpcyBpcyBhIHBhcmFncmFwaCBhbmQgeCBpcyB7e3g6MDNkfX0gYW5k
IHkgaXMge3t5Oi4yZn19Lgo+IE90aGVyIGNvbnRlbnQgaXM6IGEgPSB7e2F9fSwgYiA9IHt7
Yn19LgoKIyMgRm9ybWF0IExpbmsgRXh0ZW5zaW9uCgpXaGVuIHdyaXRpbmcgbXVsdGlwbGUg
ZG9jdW1lbnRzLCBvZnRlbiBkb2N1bWVudHMgYXJlIHJlZmVyZW5jZWQKYmV0d2VlbiBlYWNo
IG90aGVyIHVzaW5nIGxpbmtzLiBJbiBvcmRlciB0byByZWZlciB0byBleHRlcm5hbApgaHRt
bGAgYW5kIGBwZGZgIGRvY3VtZW50cyB0aGUgTWFya2Rvd24gbGluayBzdGF0ZW1lbnQgaXMg
dXNlZC4KYGBgbWQKW0xpbmsgQ2FwdGlvbl0ocGF0aC90by9maWxlLmh0bWwpCltMaW5rIENh
cHRpb25dKHBhdGgvdG8vZmlsZS5wZGYpCmBgYApPbmUgbGluayBzdGF0ZW1lbnQgY2Fubm90
IGJlIHVzZWQgZm9yIHJlbmRlcmluZyBgaHRtbGAgYW5kIGBwZGZgCndpdGggY29uc2lzdGVu
dCBwYXRocy4gVXNpbmcgdGhlIGBtYXJreWAgZm9ybWF0IGxpbmsKIGAuXD8/P2AgZmlsZSBl
eHRlbnNpb24gcmVzdWx0cyBpbiBjb25zaXN0ZW50IGxpbmtzIGZvciBgaHRtbGAgYW5kCmBw
ZGZgIGRvY3VtZW50cy4KCiMjIyMgRXhhbXBsZSB7LX0KYGBgbWQKW0xpbmsgdG8gdGhpcyBE
b2N1bWVudF0obWFya3kuXD8/PykKYGBgCiMjIyMgT3V0cHV0IHstfQo+IFtMaW5rIHRvIHRo
aXMgRG9jdW1lbnRdKG1hcmt5Lj8/PykKCiMjIEZvcm1hdCBDb2RlcwoKT2Z0ZW4gd2hlbiB3
cml0aW5nIG1hcmtkb3duIGZvciBgaHRtbGAgYW5kIGBwZGZgIGRvY3VtZW50cywgdGhlCm91
dHB1dCBuZWVkcyB0byBiZSB0d2Vha2VkIGFjY29yZGluZ2x5LgpgbWFya3lgIHN1cHBvcnRz
IGZvcm1hdCBzcGVjaWZpYyB0d2Vha2luZyBieSBpbmplY3RpbmcKcmF3IGBodG1sYCBvciBg
dGV4YCBjb2RlIGludG8gTWFya2Rvd24gdXNpbmcgZm9ybWF0IGNvZGVzLgoKSW4gb3JkZXIg
dG8gaW5qZWN0IGZvcm1hdCBzcGVjaWZpYyBjb2RlIHRoZSBgZm10Y29kZWAgY2xhc3MgaXMg
dXNlZC4KVGhlIGBmbXRjb2RlYCBjbGFzcyBtYW5hZ2VzIGluamVjdGlvbiBvZiBgaHRtbGAg
YW5kIGB0ZXhgIGNvZGUKZGVwZW5kaW5nIG9uIHRoZSBvdXRwdXQgZm9ybWF0LgoKKipBVFRF
TlRJT046KiogYHRleGAgcGFja2FnZXMgaGF2ZSB0byBiZSBpbmNsdWRlZCBmb3IgYHBkZmAg
YXMgd2VsbCBhcwpKYXZhU2NyaXB0IGFuZCBzdHlsZSBzaGVldHMgZm9yIGBodG1sYCB1c2lu
ZyB0aGUgbWV0YSBkYXRhIGZpZWxkcwpgaGVhZGVyLWluY2x1ZGVzLS1wZGZgIGFuZCBgaGVh
ZGVyLWluY2x1ZGVzLS1odG1sYCByZXNwZWN0aXZlbHkuCgojIyMjIEV4YW1wbGU6IGBmbXRj
b2RlYCB7LX0KYGBgcHl0aG9uPD8hCkYgPSBmbXRjb2RlKGh0bWw9Ikg8c3VwPlQ8L3N1cD48
c3ViPk08L3N1Yj5MIiwgcGRmPXIiXExhVGVYIikKPz4KYGBgCmBgYG1hcmtkb3duCkludm9j
YXRpb24gb2YgZm9ybWF0IGNvZGUgcmVzdWx0cyBpbjoge1x7RigpfVx9LgpgYGAKIyMjIyBP
dXRwdXQgey19Cj4gSW52b2NhdGlvbiBvZiBmb3JtYXQgY29kZSByZXN1bHRzIGluOiB7e0Yo
KX19LgoKIyMjIyBFeGFtcGxlOiBDb2xvciB7LX0KYGBgcHl0aG9uPD8hCkMgPSBsYW1iZGEg
Y29sb3I6IGZtdGNvZGUoCglodG1sPSI8c3BhbiBzdHlsZT0nY29sb3I6JXM7Jz57MH08L3Nw
YW4+IiAlIGNvbG9yLAoJcGRmPXIiXHRleHRjb2xvcnt7JXN9fXt7ezB9fX0iICUgY29sb3IK
KQpCID0gQygiYmx1ZSIpClIgPSBDKCJyZWQiKQo/PgpgYGAKYGBgbWFya2Rvd24KVGV4dCB3
aXRoIHtce0IoImJsdWUiKX1cfSBhbmQge1x7UigiUkVEIil9XH0uCmBgYAojIyMjIE91dHB1
dCB7LX0KPiBUZXh0IHdpdGgge3tCKCJibHVlIil9fSBhbmQge3tSKCJSRUQiKX19LgoKCiMj
IyMgRXhhbXBsZTogQ2xhc3NlcyB7LX0KYGBgcHl0aG9uPD8hCmNsYXNzIGNvbG9yOgoJZGVm
IF9faW5pdF9fKHNlbGYsIGNvbG9yKToKCQlzZWxmLmNvbG9yID0gY29sb3IKCWRlZiB1cHBl
cihzZWxmLCB4KToKCQlyZXR1cm4gc2VsZi50ZXh0KHgudXBwZXIoKSkKCWRlZiBsb3dlcihz
ZWxmLCB4KToKCQlyZXR1cm4gc2VsZi50ZXh0KHgubG93ZXIoKSkKCmNsYXNzIGh0bWwoY29s
b3IpOgoJZGVmIHRleHQoc2VsZiwgeCk6CgkJcmV0dXJuIGYiPHNwYW4gc3R5bGU9J2NvbG9y
OntzZWxmLmNvbG9yfTsnPnt4fTwvc3Bhbj4iCgpjbGFzcyBwZGYoY29sb3IpOgoJZGVmIHRl
eHQoc2VsZiwgeCk6CgkJcmV0dXJuIHJmIlx0ZXh0Y29sb3J7e3tzZWxmLmNvbG9yfX19e3t7
eH19fSIKCkNDID0gbGFtYmRhIHg6IGZtdGNvZGUoaHRtbD1odG1sKHgpLCBwZGY9cGRmKHgp
KQpCQiA9IENDKCJibHVlIikKUlIgPSBDQygicmVkIikKPz4KYGBgCmBgYG1hcmtkb3duClRl
eHQgd2l0aCB7XHtCQi51cHBlcigiYmx1ZSIpfVx9IGFuZCB7XHtSUi5sb3dlcigiUkVEIil9
XH0uCmBgYAojIyMjIE91dHB1dCB7LX0KPiBUZXh0IHdpdGgge3tCQi51cHBlcigiYmx1ZSIp
fX0gYW5kIHt7UlIubG93ZXIoIlJFRCIpfX0uCgojIE1ldGEgRGF0YSBpbiBGcm9udCBNYXR0
ZXIKCk1ldGEgZGF0YSBpcyBhbm5vdGF0ZWQgaW4gdGhlIGZyb250IG1hdHRlciBvZiBhIAlN
YXJrZG93biB0ZXh0IGRvY3VtZW50LgpUaGUgZnJvbnQgbWF0dGVyIG11c3Qgc3RhcnQgaW4g
dGhlIGZpcnN0IGxpbmUgd2l0aCBgLS0tYCBhbmQgcHJlY2VkZXMgYWxsCm90aGVyIHRleHQg
YmVpbmcgZmVuY2VkIGJ5IGAtLS1gLiBUaGUgbWV0YSBkYXRhIGlzIGluIGB5YW1sYCBmb3Jt
YXQuClRoZSBgeWFtbGAgYmxvY2sgaXMgcGFyc2VkIHVzaW5nIGBweXRob24tcHl5YW1sYC4g
QWxsIG1ldGEKZGF0YSBpcyBpbXBvcnRlZCBpbnRvIHRoZSBwcmVwcm9jZXNzZWQgZG9jdW1l
bnQuCgojIyBQYW5kb2MgRnJvbnQgTWF0dGVyCgojIyMjIEV4YW1wbGUgey19CmBgYHlhbWwK
LS0tCnRpdGxlOgpkYXRlOgphdXRob3I6CmxpbmstY2l0YXRpb25zOgpiaWJsaW9ncmFwaHk6
CmhlYWRlci1pbmNsdWRlczoKeG5vcy1jbGV2ZXJlZjoKeG5vcy1jYXBpdGFsaXNlOgpmb250
c2l6ZToKLS0tCmBgYApUaGUgbWV0YSBkYXRhIGZpZWxkcwpbYHRpdGxlYCwgYGRhdGVgLCBg
YXV0aG9yYF0oaHR0cHM6Ly9wYW5kb2Mub3JnL01BTlVBTC5odG1sI21ldGFkYXRhLXZhcmlh
YmxlcyksCltgbGluay1jaXRhdGlvbnNgXShodHRwczovL3BhbmRvYy5vcmcvTUFOVUFMLmh0
bWwjb3RoZXItcmVsZXZhbnQtbWV0YWRhdGEtZmllbGRzKSwKW2BiaWJsaW9ncmFwaHlgXSho
dHRwczovL3BhbmRvYy5vcmcvTUFOVUFMLmh0bWwjY2l0YXRpb24tcmVuZGVyaW5nKSBhbmQK
W2BoZWFkZXItaW5jbHVkZXNgXShodHRwczovL3BhbmRvYy5vcmcvTUFOVUFMLmh0bWwjdmFy
aWFibGVzLXNldC1hdXRvbWF0aWNhbGx5KQphcmUgcHJvY2Vzc2VkIGJ5IGBwYW5kb2NgIGR1
cmluZyBkb2N1bWVudCByZW5kZXJpbmcuIGBmb250c2l6ZWAgYWRqdXN0cyB0aGUKZm9udCBz
aXplIGluIFtgaHRtbGBdKGh0dHBzOi8vcGFuZG9jLm9yZy9NQU5VQUwuaHRtbCN2YXJpYWJs
ZXMtZm9yLWh0bWwpCmFuZCBbYHBkZmBdKGh0dHBzOi8vcGFuZG9jLm9yZy9NQU5VQUwuaHRt
bCN2YXJpYWJsZXMtZm9yLWxhdGV4KSBkb2N1bWVudHMuClRoZSBgeG5vcy1jbGV2ZXJlZmAg
YW5kIGB4bm9zLWNhcGl0YWxpc2VgCmZpZWxkcyBhcmUgdXNlZCBieSB0aGUgW2BwYW5kb2Mt
eG5vc2BdKGh0dHBzOi8vZ2l0aHViLmNvbS90b21kdWNrL3BhbmRvYy14bm9zKQpleHRlbnNp
b25zIGZvciByZWZlcmVuY2luZwpbZmlndXJlc10oaHR0cHM6Ly9naXRodWIuY29tL3RvbWR1
Y2svcGFuZG9jLWZpZ25vcyNjdXN0b21pemF0aW9uKSwKW3RhYmxlc10oaHR0cHM6Ly9naXRo
dWIuY29tL3RvbWR1Y2svcGFuZG9jLXRhYmxlbm9zI2N1c3RvbWl6YXRpb24pLApbc2VjdGlv
bnNdKGh0dHBzOi8vZ2l0aHViLmNvbS90b21kdWNrL3BhbmRvYy1zZWNub3MjY3VzdG9taXph
dGlvbikgYW5kCltlcXVhdGlvbnNdKGh0dHBzOi8vZ2l0aHViLmNvbS90b21kdWNrL3BhbmRv
Yy1lcW5vcyNjdXN0b21pemF0aW9uKS4KCiMjIGBtYXJreWAgRm9ybWF0IEZpZWxkcwoKKipF
eGFtcGxlKioKYGBgeWFtbAotLS0KaGVhZGVyLWluY2x1ZGVzLS1wZGY6ID4KICBcaHlwZXJz
ZXR1cHsKICBjb2xvcmxpbmtzPWZhbHNlLAogIGFsbGJvcmRlcmNvbG9ycz17MCAwIDB9LAog
IHBkZmJvcmRlcnN0eWxlPXsvUy9VL1cgMX1cfQpoZWFkZXItaW5jbHVkZXMtLWh0bWw6ID4K
ICA8c3R5bGU+KiB7IGJveC1zaXppbmc6IGJvcmRlci1ib3g7IH08L3N0eWxlPgotLS0KYGBg
CgpUaGUgcGFuZG9jIGBoZWFkZXItaW5jbHVkZXNgIGZpZWxkIGlzIHVzZWQgZm9yIGBwZGZg
IGFuZCBgaHRtbGAgZG9jdW1lbnRzLAp0aGVyZWZvcmUgaXQgbXVzdCBjb250YWluIGNvcnJl
c3BvbmRpbmcgdGV4IGFuZCBgaHRtbGAgY29kZS4KClRoZSBmaWVsZCBgaGVhZGVyLWluY2x1
ZGVzYCBlbmRpbmcgd2l0aCBgLS1wZGZgIG9yIGAtLWh0bWxgCnNwZWNpZmllcyBjb3JyZXNw
b25kaW5nIG9wdGlvbnMgZm9yIHRoZSBnZW5lcmF0aW9uIG9mIGBwZGZgIGFuZCBgaHRtbGAK
ZG9jdW1lbnRzLiBEdXJpbmcgbWFrZSwgYG1hcmt5YCBzY2FucyBhbGwgbWV0YSBkYXRhIGZp
ZWxkcywgYW5kCmZpZWxkcyB3aGljaCBlbmQgd2l0aCBgLS1wZGZgIGFuZCBgLS1odG1sYCBh
cmUgc2VsZWN0ZWQgYW5kIGZvcndhcmRlZAp0byBgcGFuZG9jYCBiYXNlZCBvbiB0aGUgZm9y
bWF0IHRvIGJlIHJlbmRlcmVkLgoKIyBIb3cgZG9lcyBgbWFya3lgIHdvcmsgaW50ZXJuYWxs
eT8KCmBtYXJreWAgdXNlcyBhbiBleHRyZW1lbHkgc2ltcGxlIG1lY2hhbmlzbSBmb3IgZ2Vu
ZXJhdGluZyBhIHB5dGhvbiBwcm9ncmFtbQpmcm9tIHRoZSBNYXJrZG93biB0ZXh0LiBVc2lu
ZyB0aGUgYDxcPy4uLj9cPmAgYW5kIGB7XHsuLi59XH1gIHN0YXRlbWVudCwKUHl0aG9uIGNv
ZGUgaXMgZW1iZWRkZWQgaW50byB0aGUgTWFya2Rvd24gdGV4dCBhbmQgdHJhbnNsYXRlZCBp
bnRvIGEgc2VyaWVzCm9mIGNhbGxzIHRvIHRoZSBgX19fKClgIGZ1bmN0aW9uIHVzaW5nIGBm
YC1zdHJpbmdzIGFzIGFyZ3VtZW50cywgd2hlcmUKcHl0aG9uIHZhcmlhYmxlcyBhcmUgcmVm
ZXJlbmNlZC4gVGhpcyByZXN1bHRzIGludG8gYSBweXRob24gcHJvZ3JhbQp3aGljaCBjYW4g
Z2VuZXJhdGUgTWFya2Rvd24gdGV4dCBhbGdvcml0aG1pY2FsbHkuCgojIyMjIEV4YW1wbGU6
IGBtZC9maWxlLm1kYCB7LX0KYGBgcGhwCiogVGhpcyBpcyB7Zmlyc3R9LiA8XD8KeCA9IDEg
IyB0aGlzIGlzIGNvZGUKZm9yIGkgaW4gcmFuZ2UoMyk6CglpZiB4OgoJCT9cPgp7XHtpKzF9
XH0uIFRoZSB2YWx1ZSBpcyB7XHtce3h9XH1cfS4KPFw/CgllbHNlOgoJCT9cPntce2krMX1c
fS4gVGhlIHZhbHVlIGlzIHplcm8uCjxcPwoJeCA9IDAKP1w+KiBUaGlzIGlzIGxhc3QuCmBg
YApUaGUgZmlsZSBwcm9kdWNlcyB0aGUgZm9sbG93aW5nIE1hcmtkb3duIG91dHB1dC4KCiMj
IyMgT3V0cHV0OiBNYXJrZG93biB7LX0KYGBgYmFzaAoqIFRoaXMgaXMge2ZpcnN0fS4KMS4g
VGhlIHZhbHVlIGlzIHsxfS4KMi4gVGhlIHZhbHVlIGlzIHplcm8uCjMuIFRoZSB2YWx1ZSBp
cyB6ZXJvLgoqIFRoaXMgaXMgbGFzdC4KYGBgCgpgbWFya3lgIHRyYW5zZm9ybXMgdGhlIE1h
cmtkb3duIGludG8gUHl0aG9uIHNvdXJjZSBjb2RlLgpFeGVjdXRpb24gb2YgdGhlIFB5dGhv
biBzb3VyY2UgY29kZSB5aWVsZHMgdGhlIG5ldyBNYXJrZG93biB0ZXh0LgoKIyMjIyBPdXRw
dXQ6IGBidWlsZC9maWxlLnB5YCB7LX0KYGBgcHl0aG9uCl9fXyhyZiIiIiogVGhpcyBpcyB7
XHtmaXJzdH1cfS4gIiIiLCBfX18pOwp4ID0gMSAjIHRoaXMgaXMgY29kZQpmb3IgaSBpbiBy
YW5nZSgzKToKCWlmIHg6CgkJX19fKHJmIiIiCntpKzF9LiBUaGUgdmFsdWUgaXMge1x7XHt4
fVx9XH0uCiIiIiwgX19fKTsKCWVsc2U6CgkJX19fKHJmIiIie2krMX0uIFRoZSB2YWx1ZSBp
cyB6ZXJvLgoiIiIsIF9fXyk7Cgl4ID0gMApfX18ocmYiIiIqIFRoaXMgaXMgbGFzdC4KIiIi
LCBfX18pOwpgYGAKCiMgU2NpZW50aWZpYyBXcml0aW5nIGluIE1hcmtkb3duIHsjc2VjOnBh
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
YnVpbGQvCmh0bWwvCnBkZi8K
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
