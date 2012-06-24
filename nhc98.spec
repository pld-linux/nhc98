
# _with_ghc	- build using ghc haskell compiler

# _with_nhc	- build not using ghc haskell compiler, but nhc98
#		  (slow compiler in effect)

# Due to nhc being old it does not build with new ghc, so default compiler
# is now gcc
#		  (results is slower compiler, but buildtime is much (!)
#		  shorter, and you don't have to have ghc/nhc/... installed)

%{?_with_ghc:%define	compiler	ghc}
%{?_with_nhc:%define	compiler	nhc98}
%{!?compiler:%define	compiler	gcc}

Summary:	York compiler for Haskell 98
Summary(pl):	Kompilator York do Haskella 98
Name:		nhc98
Version:	1.17
Release:	1
License:	Free
Group:		Development/Languages
Source0:	ftp://ftp.cs.york.ac.uk/pub/haskell/nhc98/%{name}src-%{version}.tar.gz
# Source0-md5:	a8ae8c0273cc8a881a527af4c7219847
Patch0:		%{name}-termcap.patch
Patch1:		%{name}-uname.patch
Patch2:		%{name}-LP64.patch
Patch3:		%{name}-alpha.patch
URL:		http://www.cs.york.ac.uk/fp/nhc98/
BuildRequires:	%{compiler}
BuildRequires:	jdk
# for some tools
BuildRequires:	gmp-devel
BuildRequires:	ncurses-devel
BuildRequires:	rpmbuild(macros) >= 1.213
Requires:	jre
# this should be moved to subpackage
Requires:	hmake
Provides:	haskell
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
nhc98 is a fully-fledged compiler for Haskell 98, the standard lazy
functional programming language. It based on Niklas R�jemo's nhc13, a
compiler for an earlier version of the language. Written in Haskell,
it is small and very portable, and aims to produce small executables
that run in small amounts of memory. Is a pattern becoming obvious
here? :-) It also comes with extensive tool support.

%description -l pl
nhc98 jest w pe�ni wyposa�onym kompilatorem Haskella 98,
standardowego, leniwego, funkcyjnego j�zyka programowania. Bazuje na
nhc13 Niklasa R�jemo, kompilatora wcze�niejszej wersji tego j�zyka.
Jest napisany w Haskellu, ma�y i przeno�ny, jego celem jest
produkowanie ma�ych binarek, wymagaj�cych ma�o pami�ci.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%ifarch %{x8664} alpha ia64 ppc64 s390x sparc64
%patch2 -p1
%endif
%patch3 -p1

%build
./configure \
	--prefix=%{_prefix} \
	--mandir=%{_mandir}/man1 \
	--docdir=docs_/docs +docs \
	--buildwith=%{compiler} \
	--buildopts=-O

%{__make} all \
	OPT="%{rpmcflags}"

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
rm -f $RPM_BUILD_ROOT%{_bindir}/{harch,hi,hmake}
rm -f $RPM_BUILD_ROOT%{_mandir}/man1/hmake*

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc COPYRIGHT INSTALL README docs_/docs
%attr(755,root,root) %{_bindir}/*nhc98
%attr(755,root,root) %{_bindir}/hood
%attr(755,root,root) %{_bindir}/hp2graph
%attr(755,root,root) %{_bindir}/tprofprel
%{_includedir}/nhc98
%dir %{_libdir}/nhc98
%dir %{_libdir}/nhc98/ix86-Linux
%dir %{_libdir}/nhc98/*.jar
%attr (755,root,root) %{_libdir}/nhc98/ix86-Linux/nhc98*
%attr (755,root,root) %{_libdir}/nhc98/ix86-Linux/hmake*
%attr (755,root,root) %{_libdir}/nhc98/ix86-Linux/greencard-nhc98
%attr (755,root,root) %{_libdir}/nhc98/ix86-Linux/hp2graph
%{_libdir}/nhc98/ix86-Linux/*.a
%{_libdir}/nhc98/ix86-Linux/*.o
%{_libdir}/nhc98/ix86-Linux/config
# this file is not %%config
%{_mandir}/*/*
