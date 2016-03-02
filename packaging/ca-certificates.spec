Summary:        System wide CA certificates resource
Name:           ca-certificates
Version:        1
Release:        0
License:        Apache-2.0
Group:          Security/Certificate Management
Source0:        %{name}-%{version}.tar.gz
Source1001:     %{name}.manifest
BuildArch:      noarch
BuildRequires:  openssl
BuildRequires:  pkgconfig(libtzplatform-config)
BuildRequires:  cmake
BuildRequires:  findutils
Requires: filesystem

%description
Utilities for system wide CA certificate installation

%package devel
Summary:  Devel package of ca-certificates which contains RPM macros
Group:    Development/Libraries
License:  Apache-2.0
Requires: %name = %version-%release

%description devel
ca-certificates devel package which contains RPM macros
for ca-bundle and ssl certs directory

%define ssletcdir   %{TZ_SYS_RO_ETC}/ssl
%define usrcadir    %{TZ_SYS_RO_SHARE}/ca-certificates/certs
%define etccadir    %{ssletcdir}/certs
%define cabundledir /var/lib/ca-certificates
%define cabundle    %{cabundledir}/ca-bundle.pem
%define etccabundle %{ssletcdir}/ca-bundle.pem
%define macro_ca_certificates %{TZ_SYS_RO_ETC}/rpm/macros.ca-certificates

%prep
%setup
cp %{SOURCE1001} .

%build
%cmake .

%install
mkdir -p %{buildroot}%{usrcadir}
mkdir -p %{buildroot}%{etccadir}
mkdir -p %{buildroot}%{cabundledir}

cp -rf certs/* %{buildroot}%{usrcadir}

%make_install

for cert in %{buildroot}%{usrcadir}/*
do
    ln -sf %{usrcadir}/${cert/*\//} %{buildroot}%{etccadir}
done

ln -sf %{cabundle} %{buildroot}%{etccabundle}

mkdir -p %{buildroot}%{TZ_SYS_RO_ETC}/rpm

touch %{buildroot}%{macro_ca_certificates}
echo "%TZ_SYS_CA_CERTS      %{etccadir}"    >> %{buildroot}%{macro_ca_certificates}
echo "%TZ_SYS_CA_CERTS_ORIG %{usrcadir}"    >> %{buildroot}%{macro_ca_certificates}
echo "%TZ_SYS_CA_BUNDLE     %{etccabundle}" >> %{buildroot}%{macro_ca_certificates}
echo "%TZ_SYS_CA_BUNDLE_RW  %{cabundle}"    >> %{buildroot}%{macro_ca_certificates}

%files
%defattr(-, root, root)
%manifest %{name}.manifest
%license LICENSE
%dir %{usrcadir}
%dir %attr(775, root, system) %{etccadir}
%dir %{cabundledir}
%dir %{ssletcdir}
%attr(444, root, root) %{usrcadir}/*
%attr(777, system, system) %{etccadir}/*
%attr(664, root, system) %{cabundle}
%attr(777, root, root) %{etccabundle}

%files devel
%config %{macro_ca_certificates}
