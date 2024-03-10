Title: View Japanese on OpenBSD 7.4 Firefox with unifont
Date: 2024-03-10
Category: en,
Tags: openbsd, font, japanese

By default, you cannot view Chinese/Japanese/Korean (CJK) on OpenBSD, it shows only square box.

It needs CJK fonts to be installed. `unifont` is one supports many languages by GNU.

```
$ pkg_info unifont
Information for inst:unifont-15.0.06

Comment:
free Unicode font from the GNU project

Description:
GNU Unifont is a font that contains glyphs for every printable code
point in the Unicode Basic Multilingual Plane (BMP).

There is also growing coverage of the Supplementary Multilingual Plane
(SMP), and of Michael Everson's ConScript Unicode Registry (CSUR).

Maintainer: Brian Callahan <bcallah@openbsd.org>

WWW: https://unifoundry.com/unifont/

$ pkg_info -L unifont
Information for inst:unifont-15.0.06

Files:
/usr/local/share/fonts/unifont/unifont.otf
/usr/local/share/fonts/unifont/unifont.ttf
/usr/local/share/fonts/unifont/unifont_csur.otf
/usr/local/share/fonts/unifont/unifont_csur.ttf
/usr/local/share/fonts/unifont/unifont_jp.otf
/usr/local/share/fonts/unifont/unifont_jp.ttf
/usr/local/share/fonts/unifont/unifont_upper.otf
/usr/local/share/fonts/unifont/unifont_upper.ttf

```

Install:

```
# pkg_add unifont
```

Then restart Firefox and it will display CJK. Welcome to 2024!

Written on
```
$ uname -a
OpenBSD obsd.dev.obsd 7.4 GENERIC.MP#2 amd
```

