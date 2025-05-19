[app]

title = Flappy Clone
package.name = flappyclone
package.domain = org.umarsultani
source.dir = .
source.main = main.py
version = 1.0
orientation = all
source.include_exts = py,png,jpg,kv,atlas,ttf,mp3,wav
source.exclude_exts = spec
android.arch = armeabi-v7a
copy_to_current = 1

[buildozer]

android.api = 33
android.ndk = 25b
android.minapi = 21
android.sdk = 33
force_build = 0
android.permissions = INTERNET

[app]

requirements = python3,kivy
android.add_version = 0
android.enable_androidx = 1

[log]

log_level = 2

[buildozer]

clean_build = 0
android.accept_sdk_license = True
