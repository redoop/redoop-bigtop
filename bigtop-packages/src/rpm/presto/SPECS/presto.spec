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
%define crh_dir /usr/%{crh_tag}/%{crh_version_with_bn}
%define presto_name presto
%define etc_presto /etc/presto/conf
%define lib_presto %{crh_dir}/presto
%define presto_data /var/presto/data
%define vlb_presto /var/lib/presto
%define bin_presto %{_bindir}


%define __jar_repack 0


%define presto_folder %{presto_name}-server-%{presto_base_version}

%if  %{?suse_version:1}0

# Only tested on openSUSE 11.4. le'ts update it for previous release when confirmed
%if 0%{suse_version} > 1130
%define suse_check \# Define an empty suse_check for compatibility with older sles
%endif

# SLES is more strict and check all symlinks point to valid path
# But we do point to a hadoop jar which is not there at build time
# (but would be at install time).
# Since our package build system does not handle dependencies,
# these symlink checks are deactivated
%define __os_install_post \
    %{suse_check} ; \
    /usr/lib/rpm/brp-compress ; \
    %{nil}

%define doc_presto %{_docdir}/presto
%define alternatives_cmd update-alternatives
%global initd_dir %{_sysconfdir}/rc.d

%else

%define doc_presto %{_docdir}/presto-%{presto_version}
%define alternatives_cmd alternatives
%global initd_dir %{_sysconfdir}/rc.d/init.d

%endif


Name: presto%{crh_version_as_name}
Version: %{presto_version}
Release: %{presto_release}
Summary:  presto is an open source distributed SQL query engine for running interactive analytic queries against data sources of all sizes ranging from gigabytes to petabytes.
URL: https://prestodb.io/
Group: Development/Libraries
Buildroot: %{_topdir}/INSTALL/%{presto_name}-%{version}
License: ASL 2.0
Source0: %{presto_folder}.tar.gz
Source1: do-component-build
Source2: install_%{presto_name}.sh
#BIGTOP_PATCH_FILES
Requires: /usr/sbin/useradd
Requires: coreutils


%if  0%{?mgaversion}
Requires: bsh-utils
%else
Requires: sh-utils
%endif

%description 
presto is an open source distributed SQL query engine for running interactive analytic queries against data sources of all sizes ranging from gigabytes to petabytes. 


%prep
%setup -n %{presto_folder}

#BIGTOP_PATCH_COMMANDS

%build
env presto_VERSION=%{version} sh %{SOURCE1}

%install
%__rm -rf $RPM_BUILD_ROOT


env CRH_DIR=%{crh_dir} sh %{SOURCE2} \
          --build-dir=$PWD \
          --prefix=$RPM_BUILD_ROOT \
	  --doc-dir=%{doc_presto}


%__install -d -m 0755 $RPM_BUILD_ROOT/usr/bin


%pre
getent group presto >/dev/null || groupadd -r presto
getent passwd presto >/dev/null || useradd -c "presto" -s /sbin/nologin -g presto -r -d %{vlb_presto} presto 2> /dev/null || :
%__install -d -o presto -g presto -m 0755 %{vlb_presto}


%post
%{alternatives_cmd} --install %{etc_presto} %{presto_name}-conf %{etc_presto}.empty 30

%preun
if [ "$1" = 0 ]; then
        %{alternatives_cmd} --remove %{presto_name}-conf %{etc_presto} || :
fi


%files 
%defattr(644,root,root,755)
%{etc_presto}
%{lib_presto}
%attr(755,root,root) %{lib_presto}/bin/launcher
%attr(755,root,root) %{lib_presto}/bin/launcher.properties
%attr(755,root,root) %{lib_presto}/bin/launcher.py
%attr(755,root,root) %{lib_presto}/bin/presto
%attr(755,root,root) %{bin_presto}/presto

%dir %{presto_data}
