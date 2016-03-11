Summary:        System wide CA certificates resource
Name:           ca-certificates
Version:        1
Release:        0
License:        Apache-2.0
Group:          Security/Certificate Management
Source0:        %{name}-%{version}.tar.gz
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

# prefix macro
%define etc_dir     %{?TZ_SYS_ETC:%TZ_SYS_ETC}%{!?TZ_SYS_ETC:/opt/etc}
%define ro_etc_dir  %{?TZ_SYS_RO_ETC:%TZ_SYS_RO_ETC}%{!?TZ_SYS_RO_ETC:%_sysconfdir}
%define ssl_dir     %{etc_dir}/ssl
%define ro_ssl_dir  %{ro_etc_dir}/ssl
%define ro_data_dir %{?TZ_SYS_RO_SHARE:%TZ_SYS_RO_SHARE}%{!?TZ_SYS_RO_SHARE:%_datadir}

# CA certs macro
%define ro_ca_certs_orig_dir %{ro_data_dir}/ca-certificates/certs
%define ro_ca_certs_dir      %{ro_ssl_dir}/certs
%define ca_certs_dir         %{ssl_dir}/certs

# CA bundle macro
%define ca_bundle_dir /var/lib/ca-certificates
%define ca_bundle     %{ca_bundle_dir}/ca-bundle.pem
%define ro_ca_bundle  %{ro_ssl_dir}/ca-bundle.pem

%define macro_ca_certificates %{ro_etc_dir}/rpm/macros.ca-certificates

%prep
%setup -q

%build
%cmake . -DVERSION=%version \
         -DTZ_SYS_CA_CERTS=%ca_certs_dir \
         -DTZ_SYS_CA_BUNDLE=%ca_bundle

%install

# devel macro
mkdir -p %{buildroot}%{ro_etc_dir}/rpm
touch %{buildroot}%{macro_ca_certificates}
echo "%TZ_SYS_RO_CA_CERTS_ORIG %{ro_ca_certs_orig_dir}" >> %{buildroot}%{macro_ca_certificates}
echo "%TZ_SYS_RO_CA_CERTS      %{ro_ca_certs_dir}"      >> %{buildroot}%{macro_ca_certificates}
echo "%TZ_SYS_CA_CERTS         %{ca_certs_dir}"         >> %{buildroot}%{macro_ca_certificates}
echo "%TZ_SYS_RO_CA_BUNDLE     %{ro_ca_bundle}"         >> %{buildroot}%{macro_ca_certificates}
echo "%TZ_SYS_CA_BUNDLE        %{ca_bundle}"            >> %{buildroot}%{macro_ca_certificates}

# generate original CA certificates
mkdir -p %{buildroot}%{ro_ca_certs_orig_dir}
cp -rf certs/* %{buildroot}%{ro_ca_certs_orig_dir}

# link files : for certs RW area
mkdir -p %{buildroot}%{ca_certs_dir}
for cert in %{buildroot}%{ro_ca_certs_orig_dir}/*
do
    ln -sf %{ro_ca_certs_orig_dir}/${cert/*\//} %{buildroot}%{ca_certs_dir}
done

# link directory : for sync certs RW area with RO area
mkdir -p %{buildroot}%{ro_ssl_dir}
ln -sf %{ca_certs_dir} %{buildroot}%{ro_ca_certs_dir}

# generate original CA bundle
mkdir -p %{buildroot}%{ca_bundle_dir}
%make_install

# link file : for bundle
ln -sf %{ca_bundle} %{buildroot}%{ro_ca_bundle}

%files
%defattr(-, root, root)
%manifest %{name}.manifest
%license LICENSE
# original CA Certificates
%dir %{ro_ca_certs_orig_dir}
%attr(444, root, root) %{ro_ca_certs_orig_dir}/*
# symbol Certificates : R0 area
%dir %{ro_ca_certs_dir}
# symbol Certificates : RW area
%dir %{ca_certs_dir}
%attr(775, system, system) %{ca_certs_dir}/*
# original CA bundle
%dir %{ca_bundle_dir}
%attr(664, root, system) %{ca_bundle}
# symbol CA bundle
%attr(664, root, system) %{ro_ca_bundle}

%files devel
%config %{macro_ca_certificates}
