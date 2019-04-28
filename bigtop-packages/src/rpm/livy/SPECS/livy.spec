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
%define component_name livy
%define etc_livy_conf /etc/%{component_name}/
%define conf_dir_shipped %{_sysconfdir}/%{component_name}/
%define etc_livy_conf_dist %{etc_livy_conf}/conf.dist
%define livy_home %{crh_dir}/%{component_name}
%define licy_user_home /var/lib/%{component_name}
%define bin_livy %{livy_home}/bin
%define conf_livy %{livy_home}/conf
%define jars_livy %{livy_home}/jars
%define repl_jars_livy %{livy_home}/repl-jars
%define rsc_jars_livy %{livy_home}/rsc-jars
%define livy_username livy
#fix BUG-26074
%global debug_package %{nil}
%if  %{?suse_version:1}0
# Only tested on openSUSE 11.4. le'ts update it for previous release when confirmed
%if 0%{suse_version} > 1130
%define suse_check \# Define an empty suse_check for compatibility with older sles
%endif
# SLES is more strict anc check all symlinks point to valid path
# But we do point to a hadoop jar which is not there at build time
# (but would be at install time).
# Since our package build system does not handle dependencies,
# these symlink checks are deactivated
%define __os_install_post \
    %{suse_check} ; \
    /usr/lib/rpm/brp-compress ; \
    %{nil}
%define doc_livy %{component_name}/doc
%global initd_dir %{_sysconfdir}/rc.d/init.d
%define alternatives_cmd update-alternatives
%else
# CentOS 5 does not have any dist macro
# So I will suppose anything that is not Mageia or a SUSE will be a RHEL/CentOS/Fedora
%if %{!?mgaversion:1}0
# FIXME: brp-repack-jars uses unzip to expand jar files
# Unfortunately guice-2.0.jar pulled by ivy contains some files and directories without any read permission
# and make whole process to fail.
# So for now brp-repack-jars is being deactivated until this is fixed.
# See BIGTOP-294
%define __os_install_post \
    /usr/lib/rpm/redhat/brp-compress ; \
    /usr/lib/rpm/redhat/brp-strip-static-archive %{__strip} ; \
    /usr/lib/rpm/redhat/brp-strip-comment-note %{__strip} %{__objdump} ; \
    /usr/lib/rpm/brp-python-bytecompile ; \
    %{nil}
%endif
%define doc_livy %{_docdir}/%{component_name}
%global initd_dir %{_sysconfdir}/rc.d/init.d
%define alternatives_cmd alternatives
%endif
Name: livy%{crh_version_as_name}
Version: %{livy_base_version}
Release: %{livy_release}
Summary: Livy is an open source REST interface for interacting with Spark from anywhere. It supports executing snippets of code or programs in a Spark context that runs locally or in YARN.
URL: http://livy.incubator.apache.org/
Group: Applications/Server
Buildroot: %{_topdir}/INSTALL/%{component_name}-%{version}
License:  Apache License, Version 2.0
Source0: %{component_name}-%{livy_base_version}.tar.gz
Source1: do-component-build
Source2: install_livy.sh
%description
Livy is an open source REST interface for interacting with Spark from anywhere. It supports executing snippets of code or programs in a Spark context that runs locally or in YARN.
%prep
%setup -q -n %{component_name}-%{livy_base_version}
%build
env LIVY_VERSION=%{version} livy_base_version=%{livy_base_version} bash %{SOURCE1}
%install
%__rm -rf $RPM_BUILD_ROOT
env CRH_DIR=%{crh_dir} CRH_VERSION=%{crh_version_with_bn} sh %{SOURCE2} \
        --build-dir=`pwd` \
        --prefix=$RPM_BUILD_ROOT \
        --crh-dir=%{crh_dir}
%pre
getent group storm 2>&1 > /dev/null || /usr/sbin/groupadd -r livy
getent group hadoop 2>&1 > /dev/null || /usr/sbin/groupadd -r hadoop
getent passwd storm 2>&1 > /dev/null || /usr/sbin/useradd -c "LIVY" -s /bin/bash -g livy -G livy, hadoop -r -m -d %{livy_user_home} livy 2> /dev/null || :
%post
if [ !  -e "%{conf_dir_shipped}/conf" ]; then
    rm -f %{conf_dir_shipped}/conf
    mkdir -p %{conf_dir_shipped}/conf
    cp -rp  %{etc_livy_conf_dist}/* %{conf_dir_shipped}/conf
fi
%preun
#######################
#### FILES SECTION ####
#######################
%files
%defattr(-,root,root)
%{livy_home}/
%config(noreplace) %{etc_livy_conf_dist}
