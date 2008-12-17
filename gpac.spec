# Todo:  - Patch-in xulrunner support within configure with pkg-config support.
#        - Add pkg-config support for libs detection.
#        - Add pkg-config support generated form configure for gpac (same as ffmpeg).
#        - Make it support swscaler enabled ffmpeg (at least test it - upstream).
#        - Debug Osmo4 (don't even work).
#        - Submit and import patches upstream.
#        - Fix unused-direct-shlib-dependency on libgpac

%define osmo          Osmo4
#define cvs           20080217
%define with_static   1
%define with_osmo     0
# Mozilla stuff fails. It's completely disabled for now.
%define mozver        3.0
%define geckover      1.9
%define xuldir        %{_datadir}/idl/xulrunner-sdk-1.9pre
%define xulbindir     %{_libdir}/xulrunner-%{geckover}pre

Name:        gpac
Summary:     MPEG-4 multimedia framework
Version:     0.4.5
Release:     1%{?dist}
License:     LGPLv2+
Group:       System Environment/Libraries
URL:         http://gpac.sourceforge.net/
#Source0:     http://downloads.sourceforge.net/gpac/gpac-%{version}.tar.gz
Source0:     http://rpms.kwizart.net/fedora/SOURCE/gpac-%{version}-repack.tar.bz2
Source9:     gpac-snapshot.sh
Patch0:      gpac-0.4.5-makefix.patch
Patch1:      gpac-0.4.5-soname.patch
Patch2:      gpac-0.4.5-amr.patch
Patch3:      gpac-0.4.5-lib64.patch
Patch4:      gpac-0.4.5-system_openjpeg.patch
Patch6:      gpac-0.4.5-shared_sggen.patch
Patch7:      gpac-0.4.5-libxml2.patch
BuildRoot:   %{_tmppath}/%{name}-%{version}-%{release}-root-%(id -u -n)

BuildRequires:  ImageMagick
BuildRequires:  SDL-devel
BuildRequires:  a52dec-devel
BuildRequires:  librsvg2-devel >= 2.5.0
BuildRequires:  libGLU-devel
BuildRequires:  freeglut-devel
BuildRequires:  freetype-devel >= 2.1.4
BuildRequires:  faad2-devel
BuildRequires:  libjpeg-devel
BuildRequires:  libpng-devel >= 1.2.5
BuildRequires:  libmad-devel
BuildRequires:  xvidcore-devel >= 1.0.0
BuildRequires:  ffmpeg-devel
BuildRequires:  libxml2-devel
BuildRequires:  openssl-devel
BuildRequires:  openjpeg-devel
BuildRequires:  pulseaudio-libs-devel
BuildRequires:  zlib-devel
BuildRequires:  libogg-devel libvorbis-devel libtheora-devel
BuildRequires:  libXt-devel
BuildRequires:  libXpm-devel
BuildRequires:  libXv-devel
BuildRequires:  wxGTK-devel
BuildRequires:  xmlrpc-c-devel
%{?_with_mozilla:BuildRequires: gecko-devel}
BuildRequires:  doxygen
BuildRequires:  desktop-file-utils
%{?_with_amr:BuildRequires: amrnb-devel amrwb-devel}

%description
GPAC is a multimedia framework based on the MPEG-4 Systems standard developed
from scratch in ANSI C.  The original development goal is to provide a clean,
small and flexible alternative to the MPEG-4 Systems reference software.

GPAC features the integration of recent multimedia standards (SVG/SMIL, VRML,
X3D, SWF, 3GPP(2) tools and more) into a single framework. GPAC also features
MPEG-4 Systems encoders/multiplexers, publishing tools for content distribution
for MP4 and 3GPP(2) files and many tools for scene descriptions
(MPEG4 <-> VRML <-> X3D converters, SWF -> MPEG-4, etc).

%package        libs
Summary:        Library for %{name}
Group:          System Environment/Libraries

%description    libs
The %{name}-libs package contains library for %{name}.


%package  devel
Summary:  Development libraries and files for %{name}
Group:    Development/Libraries
Requires: %{name}-libs = %{version}-%{release}
%if %{with_static}
%else
%endif

%description  devel
Development libraries and files for gpac.

%if %{with_static}
%package  devel-static
Summary:  Development libraries and files for %{name}
Group:    Development/Libraries
Requires: %{name}-devel = %{version}-%{release}


%description  devel-static
Static library for gpac.
%endif

%if %{with_osmo}
%package -n  %{osmo}
Summary:  Media player based on gpac
Group:    Applications/Multimedia

%description -n %{osmo}
Osmo4 is an MPEG-4 player with the following features:
* MPEG-4 Systems player
* Optimized 2D graphics renderer compliant with the Complete2D Scene Graph
  and Graphics profiles
* Video and audio presentation achieved through plugins
* Multimedia player features:
  * Timeline controls: play, pause, step.
  * Graphics features: antialising, zoom and pan, scalable resizing of
    rendering area, basic full screen support.
  * Support for Advanced Text and Graphics extension of MPEG-4 Systems
    under standardization.
  * Frame export to JPG, PNG, BMP.
%endif

%{?_with_mozilla:
%package -n mozilla-%{osmo}
Summary:  Osmo Media Player plugin for Mozilla compatible web browsers
Group:    Applications/Multimedia  
Requires:  %{osmo} = %{version}-%{release}
#Requires:  firefox >= %{mozver}
Requires:  %{_libdir}/mozilla


%description -n mozilla-%{osmo}
This package contains the OSMO Media Player plugin for Mozilla compatible
web browsers.
}

%prep
%setup -q -n gpac
%patch0 -p1 -b .makefix
%patch1 -p1 -b .soname
%patch2 -p1 -b .amr
%if %{_lib} == "lib64"
%patch3 -p1 -b .lib64
%endif
%patch4 -p1 -b .openjpeg
%patch6 -p1 -b .shared
%patch7 -p1 -b .libxml2

## kwizart - enable dynamic mode - hardcoded with patch2
# define SONAME number from the first number of gpac version.
#define soname libgpac.so.0
#sed -i.soname -e 's|EXTRALIBS+=$(GPAC_SH_FLAGS)|EXTRALIBS+=$(GPAC_SH_FLAGS)\nLDFLAGS+="-Wl,-soname,%{soname}"|' src/Makefile

# Update doxygen
pushd doc
doxygen -u
popd

# Fix encoding warnings
cp -p Changelog Changelog.origine
iconv -f ISO-8859-1 -t UTF8 Changelog.origine >  Changelog
touch -r Changelog.origine Changelog
rm -rf Changelog.origine

cp -p doc/ipmpx_syntax.bt doc/ipmpx_syntax.bt.origine
iconv -f ISO-8859-1 -t UTF8 doc/ipmpx_syntax.bt.origine >  doc/ipmpx_syntax.bt
touch -r doc/ipmpx_syntax.bt.origine doc/ipmpx_syntax.bt
rm -rf doc/ipmpx_syntax.bt.origine


%build
%configure \
  --enable-debug \
  --X11-path=%{_prefix} \
  --extra-cflags="$RPM_OPT_FLAGS -D_FILE_OFFSET_BITS=64 -D_LARGE_FILES -D_LARGEFILE_SOURCE=1 -D_GNU_SOURCE=1" \
  --disable-oss-audio \
%{?_with_mozilla:--mozdir=%{_libdir}/mozilla/plugins} \
%{?_with_amr:--enable-amr} \
  --disable-static

##
## Osmo-zila plugin.
##
%{?_with_mozilla:
#
# Rebuild osmozilla.xpt
pushd applications/osmozilla
%{xulbindir}/xpidl -m header -I%{xuldir}/stable -I%{xuldir}/unstable nsIOsmozilla.idl
%{xulbindir}/xpidl -m typelib -I%{xuldir}/stable -I%{xuldir}/unstable nsIOsmozilla.idl
%{xulbindir}/xpt_link nposmozilla.xpt nsIOsmozilla.xpt
mv nsIOsmozilla.xpt nsIOsmozilla.xpt_linux
popd 

## kwizart - osmozilla parallel make fails
# %{?_smp_mflags}
#make -C applications/osmozilla   \
#  OPTFLAGS="%optflags -fPIC -I%{_includedir}/nspr4/"     \
#  INCLUDES="-I%{_datadir}/idl/firefox-%{mozver}/       \
#    -I%{_includedir}/firefox-%{mozver}/       \
#    -I%{_includedir}/firefox-%{mozver}/xpcom    \
#    -I%{_includedir}/nspr4/ $INCLUDES"       \
#  XPIDL_INCL="-I%{_datadir}/idl/firefox-%{mozver}/     \
#    -I%{_includedir}/firefox-%{mozver}/       \
#    -I%{_includedir}/firefox-%{mozver}/xpcom    \
#    -I%{_includedir}/nspr4/ $INCLUDES"       \
#  install
}

# Parallele build will fail
make all OPTFLAGS="$RPM_OPT_FLAGS -fPIC -DPIC" 
#{?_smp_mflags}
make sggen OPTFLAGS="$RPM_OPT_FLAGS -fPIC -DPIC" 
#{?_smp_mflags}

## kwizart - build doxygen doc for devel
pushd doc
doxygen
popd

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install install-lib

%{?_with_mozilla:
## kwizart - Install osmozilla plugin - make instmoz disabled.
mkdir -p $RPM_BUILD_ROOT%{_libdir}/mozilla/{plugins,components}
install -m 755 bin/gcc/nposmozilla.so $RPM_BUILD_ROOT%{_libdir}/mozilla/plugins/nposmozilla.so
install -m 755 bin/gcc/nposmozilla.xpt $RPM_BUILD_ROOT%{_libdir}/mozilla/components/nposmozilla.xpt
}

%if %{with_osmo}
# Desktop menu Osmo4
mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications
cat > %{osmo}.desktop <<EOF
[Desktop Entry]
Name=Osmo4 Media Player
GenericName=Media Player
Comment=MPEG-4 Media Player
Exec=%{osmo}
Terminal=false
Icon=%{osmo}
Type=Application
Encoding=UTF-8
Categories=AudioVideo;Player;
EOF

desktop-file-install --vendor "" \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications \
  --mode 644 \
  %{osmo}.desktop

#icons
mkdir -p $RPM_BUILD_ROOT%{_datadir}/pixmaps
install -m 0644 applications/osmo4_wx/osmo4.xpm $RPM_BUILD_ROOT%{_datadir}/pixmaps/%{osmo}.xpm
%else
rm -rf $RPM_BUILD_ROOT%{_bindir}/%{osmo}
%endif

## kwizart - rpmlint gpac no-ldconfig-symlink
ln -sf  libgpac.so.%{version} $RPM_BUILD_ROOT%{_libdir}/libgpac.so.0
ln -sf  libgpac.so.0 $RPM_BUILD_ROOT%{_libdir}/libgpac.so

#Install generated sggen binaries
for b in MPEG4 SVG X3D; do
  pushd applications/generators/${b}
    install -pm 0755 ${b}Gen $RPM_BUILD_ROOT%{_bindir}
  popd
done


%clean
rm -rf $RPM_BUILD_ROOT

%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig


%files
%defattr(-,root,root)
%doc AUTHORS BUGS Changelog COPYING README TODO 
%{_bindir}/MP4*
%{_bindir}/*Gen
%{_datadir}/gpac/
%{_mandir}/man1/*.1.*

%files libs
%defattr(-,root,root)
%{_libdir}/libgpac.so.*
%{_libdir}/gpac/

%if %{with_osmo}
%files -n %{osmo}
%doc AUTHORS BUGS COPYING README TODO
%defattr(-,root,root)
%{_bindir}/Osmo4
%{_datadir}/applications/*.desktop
%{_datadir}/pixmaps/%{osmo}.xpm
%endif

%{?_with_mozilla:
%files -n mozilla-%{osmo}
%defattr(-,root,root)
%{_libdir}/mozilla/plugins/nposmozilla.so
%{_libdir}/mozilla/components/nposmozilla.xpt
}

%files devel
%doc doc/CODING_STYLE doc/ipmpx_syntax.bt
%doc doc/html/*
%defattr(-,root,root)
%{_includedir}/gpac/
%{_libdir}/libgpac.so

%if %{with_static}
%files devel-static
%defattr(-,root,root)
%{_libdir}/libgpac_static.a
%else
%exclude %{_libdir}/libgpac_static.a
%endif

%changelog
* Wed Dec 17 2008 kwizart < kwizart at gmail.com > - 0.4.5-1
- Update to 0.4.5 (final)
- Drop upstreamed patches - Rewrite some
- Add More BR.
- Conditionalize --with mozilla amr

* Mon Sep  8 2008 kwizart < kwizart at gmail.com > - 0.4.5-0.5.20080217cvs
- Fix for Large File Support (was livna #2075 )

* Mon Feb 25 2008 kwizart < kwizart at gmail.com > - 0.4.5-0.3.20080217cvs
- Enable devel-static
- Conditionalize Osmo4 (buggy).
- Clean the spec

* Sun Feb 17 2008 kwizart < kwizart at gmail.com > - 0.4.5-0.2.20080217cvs
- Update to 20080217.
- Split libs.
- Use the new amr nosrc scheme (need an end-users rebuilt to add support to it).
- Add openjpeg-devel missing BR
- Static patching instead of dyn patch when possible.
- Disable %%{smp_mflags} (it tries to build the bin before the lib is ready)
- Define soname as libgpac.so.0 (instead of libgpac.so.%%version )
- Exclude static lib

* Mon Feb 11 2008 Stewart Adam < s.adam at diffingo.com > - 0.4.5-0.1.20080211cvs
- Use %%{smp_mflags}
- Oops, we're actually 0.4.5
- Fix gpac so filenames
- Only install nposmozilla when %%{with_firefox} is set

* Mon Feb 11 2008 Stewart Adam < s.adam at diffingo.com > - 0.4.4-3.20080211cvs
- Update to 20080211cvs
- Disable osmozilla, doesn't build with xulrunner
- Fix builds with gcc 4.3

* Sat Dec 15 2007 Stewart Adam < s.adam at diffingo.com > - 0.4.4-2
- Rebuild for rawhide

* Tue Oct 16 2007 Stewart Adam < s.adam at diffingo.com > - 0.4.4-1
- Update to v4.4

* Sat May 26 2007 kwizart < kwizart at gmail.com > - 0.4.3-0.1cvs20070526
- Update to cvs 20070526
- Enable conditional build ( 3gpp firefox )

* Wed Apr 11 2007 kwizart < kwizart at gmail.com > - 0.4.3-0.1cvs20070411
- Update to cvs 20070411

* Thu Dec 08 2006 kwizart < kwizart at gmail.com > - 0.4.3-cvs20061208.1.kwizart.fc6
- Update to 20061208
- Uses firefox-devel (since fc6!)
- Drop tutorial
- Use version-DEV-date with libgpac.so
- Disabled osmozilla
- Fix soname 
- Enabled gprof

* Tue Oct 17 2006 kwizart < kwizart at gmail.com > - 0.4.3-cvs20061017.1_FC5
- gpac snapshot.sh
- Revert Patch osmozilla.cpp (v1.17 - build error from gpac/internal/terminal_dev.h)
- TODO: - no-soname make option for libgpac.so
  - static lib in devel - needed ?
  - osmozilla - xpt link problem.
  - Osmo4: segmentation fault on exit.
  - MP4Client: segmentation fault on launch.
  - The program 'Osmo4' received an X Window System error:
  "The error was 'BadMatch (invalid parameter attributes)'.
  (Details: serial 37 error_code 8 request_code 42 minor_code 0)"
  - MP4Box -version display: GPAC version 0.4.3-DEV (try to display cvs )

* Sat Oct 15 2006 kwizart < kwizart at gmail.com > - 0.4.2-rc2.1_FC5
- Update to 0.4.2cvs20061017
- Use DESTDIR=RPM_BUILD_ROOT in various Makefile.
- Enable mozilla plugin: osmozilla.
- Enable AMR_NB_FLOAT and AMR_WB_FLOAT / bundle AMR_NB_FIXED (but not used by default).
- Provide documentation html in doc .
- Provide tutorial from http://www.wildamerica.com/pages/Marty.html
- Various corrections.

* Fri Sep 01 2006 Anssi Hannula <anssi@zarb.org> 0.4.1-0.20060630.2plf2007.0
- lib64 fixes

* Fri Jan 30 2006 Austin Acton <austin@mandriva.org> 0.4.1-0.20060630.1plf2007.0
- initial package
