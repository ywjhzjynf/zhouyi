[app]
title = 周易占卜
package.name = zhouyi
package.domain = org.zhouyi

source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json
version = 1.0.0

requirements = python3,kivy
orientation = portrait
osx.python_version = 3
osx.kivy_version = 2.2.0

fullscreen = 0
android.permissions = INTERNET
android.minapi = 21
android.sdk = 24
android.api = 33
android.ndk = 25b
android.accept_sdk_license = True
android.arch = arm64-v8a

p4a.branch = master
p4a.source_dir =
p4a.bootstrap = sdl2
p4a.extra_args = --ignore-path="tests" --ignore-path="docs"

[buildozer]
log_level = 2
warn_on_root = 1
debug = 0
