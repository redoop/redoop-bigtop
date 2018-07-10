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

# Redoop CRH Management Packs
install -d -m 0755 $RPM_BUILD_ROOT/var/lib/ambari-mpacks/
%__cp -ra crh-DW-mpack/target/crh-DW-mpack-*.tar.gz ${RPM_BUILD_ROOT}/var/lib/ambari-mpacks/
%__cp -ra crh-Spark-mpack/target/crh-Spark-mpack-*.tar.gz ${RPM_BUILD_ROOT}/var/lib/ambari-mpacks/
%__cp -ra crh-Security-mpack/target/crh-Security-mpack-*.tar.gz ${RPM_BUILD_ROOT}/var/lib/ambari-mpacks/
%__cp -ra crh-TS-mpack/target/crh-TS-mpack-*.tar.gz ${RPM_BUILD_ROOT}/var/lib/ambari-mpacks/
%__cp -ra crs-mpack/target/crs-mpack-*.tar.gz ${RPM_BUILD_ROOT}/var/lib/ambari-mpacks/
%__cp -ra crf-mpack/target/crf-mpack-*.tar.gz ${RPM_BUILD_ROOT}/var/lib/ambari-mpacks/


%package -n %{distro_select}
Summary: Distro Select
Group: Development/Libraries
AutoProv: no
AutoReqProv: no
%description -n %{distro_select}
Distro Select


%package crh-DW
Summary: CRH Data Warehouse Mpack
Group: Development/Libraries
Requires: ambari-server
AutoProv: no
AutoReqProv: no
%description crh-DW
Redoop Ambari CRH Data Warehouse Mpack

%package crh-Spark
Summary: CRH Spark Mpack
Group: Development/Libraries
Requires: ambari-server
AutoProv: no
AutoReqProv: no
%description crh-Spark
Redoop Ambari CRH Spark Mpack

%package crh-Security
Summary: CRH Cluster Security Mpack
Group: Development/Libraries
Requires: ambari-server
AutoProv: no
AutoReqProv: no
%description crh-Security
Redoop Ambari CRH Cluster Security Mpack

%package crh-TS
Summary: CRH Time Series Mpack
Group: Development/Libraries
Requires: ambari-server
AutoProv: no
AutoReqProv: no
%description crh-TS
Redoop Ambari CRH Time Series Mpack

%package crs
Summary: Data Scientist Mpack
Group: Development/Libraries
Requires: ambari-server
AutoProv: no
AutoReqProv: no
%description crs
Redoop Ambari Data Scientist Mpack

%package crf
Summary: Data Flow Mpack
Group: Development/Libraries
Requires: ambari-server
AutoProv: no
AutoReqProv: no
%description crf
Redoop Ambari Data Flow Mpack


%files -n %{distro_select}
%attr(755,root,root) /usr/bin/%{distro_select}
%attr(755,root,root) /usr/bin/conf-select


# Service file management RPMs
%define service_macro() \
%files %1 \
%attr(644,root,root) /var/lib/ambari-mpacks/%1-mpack-1.0.0.0-SNAPSHOT.tar.gz \
%post %1 \
ambari-server install-mpack --mpack=/var/lib/ambari-mpacks/%1-mpack-1.0.0.0-SNAPSHOT.tar.gz --verbose \
%preun %1 \
ambari-server uninstall-mpack --mpack-name=%1-mpack \
%postun %1 \
rm -rf /var/lib/ambari-server/resources/mpacks/cache/%1-mpack-1.0.0.0-SNAPSHOT.tar.gz \
rm -rf /var/lib/ambari-server/data/tmp/%1-mpack-1.0.0.0-SNAPSHOT \
rm -rf /var/lib/ambari-server/data/tmp/%1-mpack-1.0.0.0-SNAPSHOT.tar.gz

%service_macro crh-DW
%service_macro crh-Spark
%service_macro crh-Security
%service_macro crh-TS
%service_macro crs
%service_macro crf