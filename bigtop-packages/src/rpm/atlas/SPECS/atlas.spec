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
%define component_name atlas

%define etc_atlas_conf /etc/%{component_name}/conf
%define conf_dir_shipped %{_sysconfdir}/%{component_name}/
%define etc_atlas_conf_dist %{etc_atlas_conf}.dist

%define atlas_home %{crh_dir}/%{component_name}
%define distroselect crh-select
#%define atlas_slider_client_home %{crh_dir}/%{component_name}-slider-client
%define atlas_user_home /var/lib/%{component_name}
%define bin_atlas %{atlas_home}/bin
%define lib_atlas %{atlas_home}
%define conf_atlas %{atlas_home}/conf
%define logs_atlas %{atlas_home}/logs
%define pids_atlas %{atlas_home}/pids
%define man_dir %{_mandir}
%define atlas_username atlas
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

%define doc_atlas %{component_name}/doc
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


%define doc_atlas %{_docdir}/%{component_name}
%global initd_dir %{_sysconfdir}/rc.d/init.d
%define alternatives_cmd alternatives

%endif


Name: atlas%{crh_version_as_name}
Version: %{atlas_base_version}
Release: %{atlas_release}
Summary: Apache Atlas
URL: http://incubator.apache.org/atlas/
Group: Applications/Server
Buildroot: %{_topdir}/INSTALL/%{component_name}-%{version}
License:  Apache License, Version 2.0
Source0: %{component_name}-%{atlas_base_version}.tar.gz
Source1: do-component-build
Source2: install_atlas.sh
Requires: zookeeper%{crh_version_as_name},hadoop%{crh_version_as_name},hbase%{crh_version_as_name}
#Requires: ranger%{crh_version_as_name}-atlas-plugin


%description
Altas is a distributed.



%prep
%setup -q -n apache-%{component_name}-sources-%{atlas_base_version}

%build
env ALTAS_VERSION=%{version} atlas_base_version=%{altas_base_version} bash %{SOURCE1}

%install
%__rm -rf $RPM_BUILD_ROOT
env CRH_DIR=%{crh_dir} CRH_VERSION=%{crh_version_with_bn} sh %{SOURCE2} \
        --build-dir=build \
        --prefix=$RPM_BUILD_ROOT \
        --crh-dir=%{crh_dir}

%__install -d  -m 0755  %{buildroot}/%{_localstatedir}/log/%{component_name}
ln -s %{_localstatedir}/log/%{component_name} %{buildroot}/%{logs_atlas}

%__install -d  -m 0755  %{buildroot}/%{_localstatedir}/run/%{component_name}
ln -s %{_localstatedir}/run/%{component_name} %{buildroot}/%{pids_atlas}

%pre
getent group atlas 2>&1 > /dev/null || /usr/sbin/groupadd -r atlas
getent group hadoop 2>&1 > /dev/null || /usr/sbin/groupadd -r hadoop
getent passwd atlas 2>&1 > /dev/null || /usr/sbin/useradd -c "ATLAS" -s /bin/bash -g atlas -G atlas, hadoop -r -m -d %{atlas_user_home} atlas 2> /dev/null || :

%post
if [ !  -e "%{conf_dir_shipped}/conf" ]; then
    rm -f %{conf_dir_shipped}/conf
    mkdir -p %{conf_dir_shipped}/conf
    cp -rp  %{etc_atlas_conf_dist}/* %{conf_dir_shipped}/conf
fi

/usr/bin/%{distroselect} --rpm-mode set atlas-client %{crh_version_with_bn}
/usr/bin/%{distroselect} --rpm-mode set atlas-server %{crh_version_with_bn}


#######################
#### FILES SECTION ####
#######################
%files
%defattr(-,root,root)
%{atlas_home}/
%{atlas_home}/DISCLAIMER.txt
%{atlas_home}/LICENSE
%{atlas_home}/NOTICE
%config(noreplace) %{etc_atlas_conf_dist}
%defattr(-,atlas,atlas)
%{logs_atlas}
%{pids_atlas}
%dir %{_localstatedir}/log/%{component_name}/
%dir %{_localstatedir}/run/%{component_name}/

