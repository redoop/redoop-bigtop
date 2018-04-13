# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

%define ambari_mpacks_name ambari-mpacks
%define distro_select crh-select
%define _binaries_in_noarch_packages_terminate_build   0
%define _unpackaged_files_terminate_build 0



# disable repacking jars
%define __os_install_post %{nil}

Name: ambari-mpacks%{crh_version_as_name}
Version: %{ambari_mpacks_version}
Release: %{ambari_mpacks_release}
Summary: Redoop Ambari Mpacks
URL: http://ambari.apache.org
Group: Development
BuildArch: noarch
Buildroot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
License: ASL 2.0 
Source0: do-component-build 
Source1: bigtop.bom
Source2: selector


# FIXME
AutoProv: no
AutoReqProv: no

%description
Redoop Ambari Management Packs


%build
# build source
bash $RPM_SOURCE_DIR/do-component-build



%install
%__rm -rf $RPM_BUILD_ROOT

# Stack-select and conf-select
install -d -m 0755 ${RPM_BUILD_ROOT}/usr/bin
cp -ra $RPM_SOURCE_DIR/selector/* ${RPM_BUILD_ROOT}/usr/bin/

# Redoop Management Packs
install -d -m 0755 $RPM_BUILD_ROOT/var/lib/ambari-mpacks/
%__cp -ra crh-ts-mpack/target/crh-ts-mpack-*.tar.gz ${RPM_BUILD_ROOT}/var/lib/ambari-mpacks/
%__cp -ra crh-dw-mpack/target/crh-dw-mpack-*.tar.gz ${RPM_BUILD_ROOT}/var/lib/ambari-mpacks/
%__cp -ra crh-stream-mpack/target/crh-stream-mpack-*.tar.gz ${RPM_BUILD_ROOT}/var/lib/ambari-mpacks/
%__cp -ra crh-BI-mpack/target/crh-BI-mpack-*.tar.gz ${RPM_BUILD_ROOT}/var/lib/ambari-mpacks/
%__cp -ra crh-spark-mpack/target/crh-spark-mpack-*.tar.gz ${RPM_BUILD_ROOT}/var/lib/ambari-mpacks/
%__cp -ra crh-security-mpack/target/crh-security-mpack-*.tar.gz ${RPM_BUILD_ROOT}/var/lib/ambari-mpacks/

%package -n %{distro_select}
Summary: Distro Select
Group: Development/Libraries
AutoProv: no
AutoReqProv: no
%description -n %{distro_select}
Distro Select


%package crh-ts
Summary: CRH Time Series Mpack
Group: Development/Libraries
AutoProv: no
AutoReqProv: no
%description crh-ts
Redoop Ambari CRH Time Series Mpack


%package crh-dw
Summary: CRH Data Warehouse Mpack
Group: Development/Libraries
AutoProv: no
AutoReqProv: no
%description crh-dw
Redoop Ambari CRH Data Warehouse Mpack

%package crh-stream
Summary: CRH stream  Mpack
Group: Development/Libraries
AutoProv: no
AutoReqProv: no
%description crh-stream
Redoop Ambari CRH stream Mpack

%package crh-BI
Summary: CRH BI  Mpack
Group: Development/Libraries
AutoProv: no
AutoReqProv: no
%description crh-BI
Redoop Ambari CRH BI Mpack

%package crh-spark
Summary: CRH spark  Mpack
Group: Development/Libraries
AutoProv: no
AutoReqProv: no
%description crh-spark
Redoop Ambari CRH spark Mpack

%package crh-security
Summary: CRH cluster security  Mpack
Group: Development/Libraries
AutoProv: no
AutoReqProv: no
%description crh-security
Redoop Ambari CRH cluster security Mpack

%files -n %{distro_select}
%attr(755,root,root) /usr/bin/%{distro_select}
%attr(755,root,root) /usr/bin/conf-select


# Service file management RPMs
%define service_macro() \
%files %1 \
%attr(644,root,root) /var/lib/ambari-mpacks/%1-mpack-1.0.0.0-SNAPSHOT.tar.gz \
%post %1 \
ambari-server install-mpack --mpack=/var/lib/ambari-mpacks/%1-mpack-1.0.0.0-SNAPSHOT.tar.gz --verbose \
ambari-server restart

%service_macro crh-ts
%service_macro crh-dw
%service_macro crh-stream
%service_macro crh-spark
%service_macro crh-BI
%service_macro crh-security
