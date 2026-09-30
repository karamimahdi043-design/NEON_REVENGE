[app]

title = NEON REVENGE Demo
package.name = neonrevenge
package.domain = com.mahdi.studio

source.dir = .
source.include_exts = py,png,jpg,jpeg,kv,atlas,mp3,ogg,wav,json,ttf
source.exclude_exts = pyc,pyo

version = 1.0.0

requirements = python3,pygame

orientation = landscape
fullscreen = 0

android.api = 35
android.minapi = 23

android.archs = arm64-v8a

android.accept_sdk_license = True

[buildozer]

log_level = 2
warn_on_root = 1
