[app]
title = Med Quiz
package.name = medquiz
package.domain = org.medquiz

source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json

version = 1.0
requirements = python3,kivy

orientation = portrait

[buildozer]
log_level = 2

# Android specific
android.api = 31
android.minapi = 21
android.ndk = 25b
android.sdk = 28

# Buildozer flags
buildozer.init = 1
