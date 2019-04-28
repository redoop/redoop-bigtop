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
%define distroselect crh-select
%define component_name knox
%define app_dir %{crh_dir}/%{component_name}
%define knox_user_home /var/lib/%{component_name}
%define conf_dir /etc/%{component_name}/conf
%define conf_dir_shipped /etc/%{component_name}/conf.%{crh_version_with_bn}
%define conf_dist_dir %{crh_dir}/etc/%{component_name}/conf
%define data_dir %{knox_user_home}/data
%define logs_dir %{_localstatedir}/log/%{component_name}
%define pids_dir %{_localstatedir}/run/%{component_name}

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

%define doc_dir %{app_dir}/%{component_name}
%global initd_dir %{crh_dir}/etc/rc.d
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


%define doc_dir %{_docdir}/%{component_name}
%global initd_dir %{_sysconfdir}/rc.d
%define alternatives_cmd alternatives

%endif


Name: knox%{crh_version_as_name}
Version: %{knox_base_version}
Release: %{knox_release}
Summary: Knox is an authenticating REST API gateway that provides perimeter security for Hadoop clusters.
URL: http://knox.incubator.apache.org/
Group: Applications/Server
Buildroot: %{_topdir}/INSTALL/%{component_name}-%{version}
License:  Apache License, Version 2.0
Source0: %{component_name}-%{knox_base_version}.tar.gz
Source1: do-component-build
Source2: install_knox.sh
BuildArch: noarch
Requires: ranger%{crh_version_as_name}-knox-plugin, %{distroselect} >= %{crh_version_with_bn}

##############################
%description 
##############################
Knox is an authenticating REST API gateway that provides perimeter security for Hadoop clusters.


##############################
%prep
##############################
%setup -q -n %{component_name}-%{knox_base_version}


##############################
%build
##############################
env CRH_DIR=%{crh_dir} CRH_VERSION=%{crh_version_with_bn} KNOX_VERSION=%{version} knox_jar_version=%{knox_base_version} knox_name=%{component_name} bash %{SOURCE1}


##############################
%install
##############################
%__rm -rf $RPM_BUILD_ROOT
env CRH_DIR=%{crh_dir} CRH_VERSION=%{crh_version_with_bn} sh -x  %{SOURCE2} \
        --build-dir=build \
        --crh-dir=%{crh_dir} \
        --prefix=$RPM_BUILD_ROOT
 

##############################
%pre
##############################
getent group knox 2>&1 > /dev/null || /usr/sbin/groupadd -r knox
getent group hadoop 2>&1 > /dev/null || /usr/sbin/groupadd -r hadoop
getent passwd knox 2>&1 > /dev/null || /usr/sbin/useradd -c "KNOX" -s /bin/bash -g knox -G hadoop -r -d %{knox_user_home} knox 2> /dev/null || :


##############################
%post
if [ !  -e "%{conf_dir}" ]; then
    rm -f %{conf_dir}
    mkdir -p %{conf_dir}
    cp -rp  %{conf_dist_dir}/* %{conf_dir}
fi
/usr/bin/%{distroselect} --rpm-mode set knox-server %{crh_version_with_bn}
##############################
#%{alternatives_cmd} --install %{conf_dir} %{name}-conf %{conf_dist_dir} 30
# Generate a random master secret.
# su -l knox -c "%{app_dir}/bin/knoxcli.sh create-master --generate"
# Generate a self-signed SSL identity certificate.
# su -l knox -c "%{app_dir}/bin/knoxcli.sh create-cert --hostname $(hostname -f)"


##############################
%preun
##############################
#if [ "$1" = "0" ]; then
    #%{alternatives_cmd} --remove %{name}-distributed-conf %{conf_dist} || :
#fi


##############################
%postun
##############################
# If this is an erase and not an upgrade
#if [ "$1" = "0" ]; then
    #%__rm -rf %{logs_dir}
    #%__rm -rf %{pids_dir}
    #%__rm -rf %{home_dir}
    #%__rm -rf %{ext_dir}
    #%__rm -rf %{app_dir}
    #/usr/sbin/userdel --force knox 2> /dev/null; true
    #/usr/sbin/groupdel knox 2> /dev/null; true
#fi


##############################
%files 
##############################

#=============================
%defattr(644,root,root,755)
#=============================
%{app_dir}
%{conf_dist_dir}

#=============================
%defattr(755,root,root)
#=============================
%{app_dir}/bin/gateway
%{app_dir}/bin/*.sh

%defattr(644,knox,knox,755)
#=============================
%config(noreplace) %{data_dir}
%{logs_dir}
%{pids_dir}

#=============================
%defattr(600,knox,knox,700)
#=============================
#%config(noreplace) %{data_dir}/security
