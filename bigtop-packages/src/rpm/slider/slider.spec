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
%define distroselect %{distro_select}
%define component_name slider
%define app_dir %{crh_dir}/%{component_name}
%define conf_dist_dir %{crh_dir}/etc/%{component_name}/conf.dist
%define conf_dir %{hdp_dir}/etc/%{component_name}/conf
%define agent_dir %{crh_dir}/%{component_name}/agent
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


%define doc_dir %{app_dir}/%{component_name}
%global initd_dir %{crh_dir}/etc/rc.d
%define alternatives_cmd alternatives

%endif


Name: slider%{crh_version_as_name}
Version: %{slider_base_version}
Release: %{slider_release}
Summary: Apache Slider is a YARN application to deploy existing distributed applications on YARN, monitor them and make them larger or smaller as desired -even while the application is running.
URL: http://slider.incubator.apache.org/
Group: Applications/Server
Buildroot: %{_topdir}/INSTALL/%{component_name}-%{version}
License:  Apache License, Version 2.0
Source0: %{component_name}-%{slider_base_version}.tar.gz
Source1: do-component-build
Source2: install_slider.sh
BuildArch: noarch
Requires(pre): coreutils, /usr/sbin/groupadd, /usr/sbin/useradd, %{distroselect} >= %{crh_version_with_bn}



##############################
%description 
##############################
Apache Slider is a YARN application to deploy existing distributed applications on YARN, monitor them and make them larger or smaller as desired -even while the application is running.


##############################
%prep
##############################
%setup -q -n %{component_name}-%{slider_base_version}

##############################
%build
##############################
env SLIDER_VERSION=%{version} slider_jar_version=%{slider_jar_version} bash %{SOURCE1}


##############################
%install
##############################
%__rm -rf $RPM_BUILD_ROOT
env HDP_DIR=%{crh_dir} HDP_VERSION=%{crh_version_with_bn} sh %{SOURCE2} \
        --build-dir=build \
        --prefix=$RPM_BUILD_ROOT \
        --hdp-dir=%{crh_dir}
 
##############################
%pre
##############################

##############################
%post
if [ !  -e "/etc/slider/conf" ]; then
	rm -f /etc/slider/conf
	mkdir -p /etc/slider/conf
        cp -rp  /usr/%{white_label}/%{crh_version_with_bn}/etc/slider/conf.dist/*  /etc/slider/conf
fi
/usr/bin/%{distroselect} --rpm-mode set slider-client %{crh_version_with_bn}
##############################

##############################
%preun
##############################

##############################
%postun
##############################

##############################
%files 
##############################
%defattr(-,root,root,755)
%{app_dir}
%{conf_dist_dir}
