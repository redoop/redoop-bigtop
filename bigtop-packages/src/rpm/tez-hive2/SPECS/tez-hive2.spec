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
%define tez_hive2_name tez-hive2
%define tez_hive2_home %{crh_dir}/%{tez_hive2_name}
%define lib_tez_hive2 %{tez_hive2_home}/lib
%define man_dir %{_mandir}


%if %{!?suse_version:1}0 && %{!?mgaversion:1}0

%define __os_install_post \
    %{_rpmconfigdir}/brp-compress ; \
    %{_rpmconfigdir}/brp-strip-static-archive %{__strip} ; \
    %{_rpmconfigdir}/brp-strip-comment-note %{__strip} %{__objdump} ; \
    /usr/lib/rpm/brp-python-bytecompile ; \
    %{nil}

%define doc_tez_hive2 %{_docdir}/tez_hive2-%{tez_hive2_version}

%endif


%if  %{?suse_version:1}0

# Only tested on openSUSE 11.4. le'ts update it for previous release when confirmed
%if 0%{suse_version} > 1130
%define suse_check \# Define an empty suse_check for compatibility with older sles
%endif

%define doc_tez_hive2 %{_docdir}/tez_hive2
%define alternatives_cmd update-alternatives
%define __os_install_post \
    %{suse_check} ; \
    /usr/lib/rpm/brp-compress ; \
    %{nil}

%endif

Name: %{tez_hive2_name}%{crh_version_as_name}
Version: %{tez_hive2_version}
Release: %{tez_hive2_release}
Summary:Apache Tez required by hive2 is the Hadoop enhanced Map/Reduce module.
URL: http://tez.apache.org
Group: Development/Libraries
Buildroot: %{_topdir}/INSTALL/%{tez_hive2_name}-%{version}
License: Apache License v2.0
Source0: apache-%{tez_hive2_name}-%{tez_hive2_base_version}-src.tar.gz
Source1: do-component-build
Source2: install_tez_hive2.sh
Source3: tez_hive2.1
Source4: bigtop.bom
Source5: init.d.tmpl
BuildArch: noarch
Requires: hadoop%{crh_version_as_name} hadoop%{crh_version_as_name}-hdfs hadoop%{crh_version_as_name}-yarn hadoop%{crh_version_as_name}-mapreduce

%if  0%{?mgaversion}
Requires: bsh-utils
%else
Requires: sh-utils
%endif


%description
The Apache Tez project is aimed at building an application framework
which allows for a complex directed-acyclic-graph of tasks for
processing data. It is currently built atop Apache Hadoop YARN

%prep
%setup -q -n apache-%{tez_hive2_name}-%{tez_hive2_base_version}-src

%build
env TEZ_HIVE2_VERSION=%{version} tez_hive2_name=%{tez_hive2_name} tez_hive2_base_version=%{tez_hive2_base_version}  bash %{SOURCE1}

%install
%__rm -rf $RPM_BUILD_ROOT

cp %{SOURCE3} %{SOURCE4} .
env CRH_DIR=%{crh_dir} CRH_VERSION=%{crh_version_with_bn} sh %{SOURCE2} \
	--build-dir=build \
        --doc-dir=%{doc_tez_hive2} \
        --libexec-dir=%{libexec_tez_hive2} \
	--prefix=$RPM_BUILD_ROOT

%pre

%post
if [ !  -e "/etc/tez-hive2/conf" ]; then
    rm -f /etc/tez-hive2/conf
    mkdir -p /etc/tez-hive2/conf
fi

ln -s /etc/tez-hive2/conf %{tez_hive2_home}/conf

%preun

#######################
#### FILES SECTION ####
#######################
%files
%defattr(-,root,root)
%{tez_hive2_home}
%doc %{doc_tez_hive2}
%{man_dir}/man1/tez_hive2.1.*
/etc/tez-hive2/conf
