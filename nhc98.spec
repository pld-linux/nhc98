
# _with_gcc	- build not using ghc haskell compiler, but standard gcc
#		  (results is slower compiler, but buildtime is much (!) 
#		  shorter, and you don't have to have ghc/nhc/... installed)

# _with_nhc	- build not using ghc haskell compiler, but nhc98
#		  (very long time of compilation...)

%{?_with_gcc:%define	compiler	gcc}
%{?_with_nhc:%define	compiler	nhc98}
%{!?compiler:%define	compiler	ghc}

Summary:	York compiler for Haskell 98
Name:		nhc98
Version:	1.10
Release:	1
Copyright:	Freely available
Group:		Development/Languages
Group(de):	Entwicklung/Sprachen
Group(pl):	Programowanie/Jêzyki
URL:		http://www.cs.york.ac.uk/fp/%{name}/
Source0:	ftp://ftp.cs.york.ac.uk/pub/haskell/%{name}/%{name}src-%{version}.tar.gz
Patch0:		%{name}-termcap.patch
Patch1:		%{name}-ghc.patch
BuildRequires:	jdk
BuildRequires:	gmp-devel
BuildRequires:	ncurses-devel
# for some tools
Provides:	haskell
BuildRequires:	%{compiler}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
nhc98 is a fully-fledged compiler for Haskell 98, the standard lazy
functional programming language. It based on Niklas Röjemo's nhc13, a
compiler for an earlier version of the language. Written in Haskell,
it is small and very portable, and aims to produce small executables
that run in small amounts of memory. Is a pattern becoming obvious
here? :-) It also comes with extensive tool support.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
./configure \
	--prefix=%{_prefix} \
	--mandir=%{_mandir}/man1 \
	--docdir=docs_/docs +docs \
	--buildwith=%{compiler} \
	--buildopts=-O

%{__make} OPT="$RPM_OPT_FLAGS" all

%install
rm -rf $RPM_BUILD_ROOT
./configure \
    --install \
    --prefix=$RPM_BUILD_ROOT%{_prefix} \
    --mandir=$RPM_BUILD_ROOT%{_mandir}/man1
%{__make} install

# correct hardcoded paths in some scripts
for f in $RPM_BUILD_ROOT%{_prefix}/{bin/{harch,hp2graph,hood,nhc98,hat-trail},lib/nhc98/ix86-Linux/hmake.config} ; do
ed -s $f <<EOF || :
,s|$RPM_BUILD_ROOT||g
wq
EOF
done

# remove hmake
rm $RPM_BUILD_ROOT%{_bindir}/{harch,hi,hmake}
rm $RPM_BUILD_ROOT%{_mandir}/man1/hmake*

gzip -9nf COPYRIGHT INSTALL README

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc *.gz docs_/docs
%attr(755,root,root) %{_bindir}/*
%{_includedir}/nhc98
%{_libdir}/nhc98
%{_mandir}/*/*
