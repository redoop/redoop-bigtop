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

%define ambari_name ambari
%define ambari_stack CRH
%define distro_select crh-select
%define _binaries_in_noarch_packages_terminate_build   0
%define _unpackaged_files_terminate_build 0

%if  %{?suse_version:1}0
%define doc_ambari %{_docdir}/ambari-doc
%global initd_dir %{_sysconfdir}/rc.d
%else
%define doc_ambari %{_docdir}/ambari-doc-%{ambari_version}
%global initd_dir %{_sysconfdir}/rc.d/init.d
%endif

# disable repacking jars
%define __os_install_post %{nil}

Name: ambari
Version: %{ambari_version}
Release: %{ambari_release}
Summary: Ambari
URL: http://ambari.apache.org
Group: Development
BuildArch: noarch
Buildroot: %(mktemp -ud %{_tmppath}/apache-%{ambari_name}-%{version}-%{release}-XXXXXX)
License: ASL 2.0 
Source0: apache-%{ambari_name}-%{ambari_base_version}-src.tar.gz
Source1: do-component-build 
Source2: install_%{ambari_name}.sh
Source3: bigtop.bom
Source4: stacks
Source5: selector
Source6: custom-style
Source7: licenseutils

Patch0: patch0-METRICS-TAR-DOWNLOADROOT.diff
Patch1: patch1-REDOOP-AMBARI-LICENSE.diff

# FIXME
AutoProv: no
AutoReqProv: no

%description
Ambari

%prep
%setup -n apache-%{ambari_name}-%{ambari_base_version}-src
# Apply patch
%patch0 -p1
%patch1 -p1


# apply custom style
DISTRO_DIR=$RPM_SOURCE_DIR bash $RPM_SOURCE_DIR/custom-style/copy-custom-style.sh %{ambari_stack}


%build
# build source
DISTRO_DIR=$RPM_SOURCE_DIR AMBARI_STACK=%{ambari_stack} PREFIX=$RPM_BUILD_ROOT bash $RPM_SOURCE_DIR/do-component-build



%install
%__rm -rf $RPM_BUILD_ROOT
AMBARI_VERSION=%{ambari_version} bash $RPM_SOURCE_DIR/install_ambari.sh \
          --build-dir=`pwd` \
          --distro-dir=$RPM_SOURCE_DIR \
          --source-dir=`pwd` \
          --prefix=$RPM_BUILD_ROOT
%__install -d -m 0755 $RPM_BUILD_ROOT/%{initd_dir}
%__cp ${RPM_BUILD_ROOT}/etc/init.d/ambari-server ${RPM_BUILD_ROOT}/%{initd_dir} || :
%__cp ${RPM_BUILD_ROOT}/etc/init.d/ambari-agent ${RPM_BUILD_ROOT}/%{initd_dir} || :


%package server
Summary: Ambari Server
Group: Development/Libraries
Requires: openssl, postgresql-server >= 8.1, python >= 2.6, curl
AutoProv: no
AutoReqProv: no
%description server
Ambari Server

%pre server
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
# limitations under the License


STACKS_FOLDER="/var/lib/ambari-server/resources/stacks"
STACKS_FOLDER_OLD="/var/lib/ambari-server/resources/stacks_$(date '+%d_%m_%y_%H_%M').old"

COMMON_SERVICES_FOLDER="/var/lib/ambari-server/resources/common-services"
COMMON_SERVICES_FOLDER_OLD="/var/lib/ambari-server/resources/common-services_$(date '+%d_%m_%y_%H_%M').old"

MPACKS_FOLDER="/var/lib/ambari-server/resources/mpacks"
MPACKS_FOLDER_OLD="/var/lib/ambari-server/resources/mpacks_$(date '+%d_%m_%y_%H_%M').old"

AMBARI_PROPERTIES="/etc/ambari-server/conf/ambari.properties"
AMBARI_PROPERTIES_OLD="$AMBARI_PROPERTIES.rpmsave"

AMBARI_ENV="/var/lib/ambari-server/ambari-env.sh"
AMBARI_ENV_OLD="$AMBARI_ENV.rpmsave"

AMBARI_KRB_JAAS_LOGIN_FILE="/etc/ambari-server/conf/krb5JAASLogin.conf"
AMBARI_KRB_JAAS_LOGIN_FILE_OLD="$AMBARI_KRB_JAAS_LOGIN_FILE.rpmsave"

AMBARI_VIEWS_FOLDER="/var/lib/ambari-server/resources/views"
AMBARI_VIEWS_BACKUP_FOLDER="$AMBARI_VIEWS_FOLDER/backups"

AMBARI_SERVER_JAR_FILES="/usr/lib/ambari-server/ambari-server-*.jar"
AMBARI_SERVER_JAR_FILES_BACKUP_FOLDER="/usr/lib/ambari-server-backups"
SERVER_CONF_SAVE="/etc/ambari-server/conf.save"
SERVER_CONF_SAVE_BACKUP="/etc/ambari-server/conf_$(date '+%d_%m_%y_%H_%M').save"

if [ -d "$SERVER_CONF_SAVE" ]
then
    echo "Backing up configs $SERVER_CONF_SAVE -> $SERVER_CONF_SAVE_BACKUP"
    mv "$SERVER_CONF_SAVE" "$SERVER_CONF_SAVE_BACKUP"
fi

if [ -f "$AMBARI_PROPERTIES" ]
then
    echo "Backing up Ambari properties $AMBARI_PROPERTIES -> $AMBARI_PROPERTIES_OLD"
    cp -n "$AMBARI_PROPERTIES" "$AMBARI_PROPERTIES_OLD"
fi

if [ -f "$AMBARI_ENV" ]
then
    echo "Backing up Ambari properties $AMBARI_ENV -> $AMBARI_ENV_OLD"
    cp -n "$AMBARI_ENV" "$AMBARI_ENV_OLD"
fi

if [ -f "$AMBARI_KRB_JAAS_LOGIN_FILE" ]
then
    echo "Backing up JAAS login file $AMBARI_KRB_JAAS_LOGIN_FILE -> $AMBARI_KRB_JAAS_LOGIN_FILE_OLD"
    cp -n "$AMBARI_KRB_JAAS_LOGIN_FILE" "$AMBARI_KRB_JAAS_LOGIN_FILE_OLD"
fi

if [ -d "$STACKS_FOLDER" ]
then
    echo "Backing up stacks directory $STACKS_FOLDER -> $STACKS_FOLDER_OLD"
    mv -f "$STACKS_FOLDER" "$STACKS_FOLDER_OLD"
fi

if [ -d "$COMMON_SERVICES_FOLDER" ]
then
    echo "Backing up common-services directory $COMMON_SERVICES_FOLDER -> $COMMON_SERVICES_FOLDER_OLD"
    mv -f "$COMMON_SERVICES_FOLDER" "$COMMON_SERVICES_FOLDER_OLD"
fi

if [ -d "$MPACKS_FOLDER" ]
then
    # Make a copy of mpacks folder
    if [ ! -d "$MPACKS_FOLDER_OLD" ]; then
        echo "Backing up mpacks directory $MPACKS_FOLDER -> $MPACKS_FOLDER_OLD"
        cp -R "$MPACKS_FOLDER" "$MPACKS_FOLDER_OLD"
    fi

    # Update symlinks in $STACKS_FOLDER_OLD to point to $MPACKS_FOLDER_OLD
    if [ -d "$STACKS_FOLDER_OLD" ]; then
        for link in $(find "$STACKS_FOLDER_OLD" -type l)
        do
            target=`readlink $link`
            if grep -q "$MPACKS_FOLDER/"<<<$target; then
                new_target="${target/$MPACKS_FOLDER/$MPACKS_FOLDER_OLD}"
                echo "Updating symlink $link -> $new_target"
                ln -snf $new_target $link
            fi
        done
    fi

    # Update symlinks in $COMMON_SERVICES_FOLDER_OLD to point to $MPACKS_FOLDER_OLD
    if [ -d "$COMMON_SERVICES_FOLDER_OLD" ]; then
    for link in $(find "$COMMON_SERVICES_FOLDER_OLD" -type l)
        do
            target=`readlink $link`
            if grep -q "$MPACKS_FOLDER/"<<<$target; then
                new_target="${target/$MPACKS_FOLDER/$MPACKS_FOLDER_OLD}"
                echo "Updating symlink $link -> $new_target"
                ln -snf $new_target $link
            fi
        done
    fi
fi

if [ ! -d "$AMBARI_VIEWS_BACKUP_FOLDER" ] && [ -d "$AMBARI_VIEWS_FOLDER" ]
then
    mkdir "$AMBARI_VIEWS_BACKUP_FOLDER"
fi

if [ -d "$AMBARI_VIEWS_FOLDER" ] && [ -d "$AMBARI_VIEWS_BACKUP_FOLDER" ]
then
    echo "Backing up Ambari view jars $AMBARI_VIEWS_FOLDER/*.jar -> $AMBARI_VIEWS_BACKUP_FOLDER/"
    cp -u $AMBARI_VIEWS_FOLDER/*.jar $AMBARI_VIEWS_BACKUP_FOLDER/
fi

for f in $AMBARI_SERVER_JAR_FILES;
do
    if [ -f "$f" ]
    then
        if [ ! -d "$AMBARI_SERVER_JAR_FILES_BACKUP_FOLDER" ]
        then
            mkdir -p "$AMBARI_SERVER_JAR_FILES_BACKUP_FOLDER"
        fi
        echo "Backing up Ambari server jar $f -> $AMBARI_SERVER_JAR_FILES_BACKUP_FOLDER/"
        mv -f $f $AMBARI_SERVER_JAR_FILES_BACKUP_FOLDER/
    fi
done

exit 0



%post server
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
# limitations under the License

# Warning: don't add changes to this script directly, please add changes to install-helper.sh.

INSTALL_HELPER="/var/lib/ambari-server/install-helper.sh"

AMBARI_SERVER_KEYS_FOLDER="/var/lib/ambari-server/keys"
AMBARI_SERVER_KEYS_DB_FOLDER="/var/lib/ambari-server/keys/db"
AMBARI_SERVER_NEWCERTS_FOLDER="/var/lib/ambari-server/keys/db/newcerts"

case "$1" in
  1) # Action install
    if [ -f "$INSTALL_HELPER" ]; then
        $INSTALL_HELPER install
    fi
  ;;
  2) # Action upgrade
    if [ -f "$INSTALL_HELPER" ]; then
        $INSTALL_HELPER upgrade
    fi
  ;;
esac

if [ -d "$AMBARI_SERVER_KEYS_FOLDER" ]
then
    chmod 700 "$AMBARI_SERVER_KEYS_FOLDER"
    if [ -d "$AMBARI_SERVER_KEYS_DB_FOLDER" ]
    then
        chmod 700 "$AMBARI_SERVER_KEYS_DB_FOLDER"
        if [ -d "$AMBARI_SERVER_NEWCERTS_FOLDER" ]
        then
            chmod 700 "$AMBARI_SERVER_NEWCERTS_FOLDER"

        fi
    fi
fi

exit 0



%preun server
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
# limitations under the License

# WARNING: This script is performed not only on uninstall, but also
# during package update. See http://www.ibm.com/developerworks/library/l-rpm2/
# for details

if [ "$1" -eq 0 ]; then  # Action is uninstall
    /usr/sbin/ambari-server stop > /dev/null 2>&1
    if [ -d "/etc/ambari-server/conf.save" ]; then
        mv /etc/ambari-server/conf.save /etc/ambari-server/conf_$(date '+%d_%m_%y_%H_%M').save
    fi

    if [ -e "/usr/sbin/ambari-server" ]; then
        # Remove link created during install
        rm /usr/sbin/ambari-server
    fi

    mv /etc/ambari-server/conf /etc/ambari-server/conf.save

    if [ -f "/var/lib/ambari-server/install-helper.sh" ]; then
      /var/lib/ambari-server/install-helper.sh remove
    fi

    chkconfig --list | grep ambari-server && chkconfig --del ambari-server
fi

exit 0



%posttrans server
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
# limitations under the License


RESOURCE_MANAGEMENT_DIR="/usr/lib/python2.6/site-packages/resource_management"
RESOURCE_MANAGEMENT_DIR_SERVER="/usr/lib/ambari-server/lib/resource_management"
JINJA_DIR="/usr/lib/python2.6/site-packages/ambari_jinja2"
JINJA_SERVER_DIR="/usr/lib/ambari-server/lib/ambari_jinja2"
AMBARI_SERVER_EXECUTABLE_LINK="/usr/sbin/ambari-server"
AMBARI_SERVER_EXECUTABLE="/etc/init.d/ambari-server"


# needed for upgrade though ambari-2.2.2
rm -f "$AMBARI_SERVER_EXECUTABLE_LINK"
ln -s "$AMBARI_SERVER_EXECUTABLE" "$AMBARI_SERVER_EXECUTABLE_LINK"

# remove RESOURCE_MANAGEMENT_DIR if it's a directory
if [ -d "$RESOURCE_MANAGEMENT_DIR" ]; then  # resource_management dir exists
  if [ ! -L "$RESOURCE_MANAGEMENT_DIR" ]; then # resource_management dir is not link
    rm -rf "$RESOURCE_MANAGEMENT_DIR"
  fi
fi
# setting resource_management shared resource
if [ ! -d "$RESOURCE_MANAGEMENT_DIR" ]; then
  ln -s "$RESOURCE_MANAGEMENT_DIR_SERVER" "$RESOURCE_MANAGEMENT_DIR"
fi

# setting jinja2 shared resource
if [ ! -d "$JINJA_DIR" ]; then
  ln -s "$JINJA_SERVER_DIR" "$JINJA_DIR"
fi

exit 0



%package agent
Summary: Ambari Agent
Group: Development/Libraries
Requires: openssl, zlib, python >= 2.6, rpm-python
AutoProv: no
AutoReqProv: no
%description agent
Ambari Agent


%pre agent
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
# limitations under the License

STACKS_FOLDER="/var/lib/ambari-agent/cache/stacks"
STACKS_FOLDER_OLD=/var/lib/ambari-agent/cache/stacks_$(date '+%d_%m_%y_%H_%M').old

COMMON_SERVICES_FOLDER="/var/lib/ambari-agent/cache/common-services"
COMMON_SERVICES_FOLDER_OLD=/var/lib/ambari-agent/cache/common-services_$(date '+%d_%m_%y_%H_%M').old

if [ -d "/etc/ambari-agent/conf.save" ]
then
    mv /etc/ambari-agent/conf.save /etc/ambari-agent/conf_$(date '+%d_%m_%y_%H_%M').save
fi

BAK=/etc/ambari-agent/conf/ambari-agent.ini.old
ORIG=/etc/ambari-agent/conf/ambari-agent.ini

BAK_SUDOERS=/etc/sudoers.d/ambari-agent.bak
ORIG_SUDOERS=/etc/sudoers.d/ambari-agent

[ -f $ORIG ] && mv -f $ORIG $BAK
[ -f $ORIG_SUDOERS ] && echo "Moving $ORIG_SUDOERS to $BAK_SUDOERS. Please restore the file if you were using it for ambari-agent non-root functionality" && mv -f $ORIG_SUDOERS $BAK_SUDOERS

if [ -d "$STACKS_FOLDER" ]
then
    mv -f "$STACKS_FOLDER" "$STACKS_FOLDER_OLD"
fi

if [ -d "$COMMON_SERVICES_FOLDER" ]
then
    mv -f "$COMMON_SERVICES_FOLDER" "$COMMON_SERVICES_FOLDER_OLD"
fi

exit 0



%post agent
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
# limitations under the License

# Warning: don't add changes to this script directly, please add changes to install-helper.sh.

case "$1" in
  1) # Action install
    if [ -f "/var/lib/ambari-agent/install-helper.sh" ]; then
        /var/lib/ambari-agent/install-helper.sh install
    fi
  ;;
  2) # Action upgrade
    if [ -f "/var/lib/ambari-agent/install-helper.sh" ]; then
        /var/lib/ambari-agent/install-helper.sh upgrade
    fi
  ;;
esac

exit 0



%preun agent
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
# limitations under the License

# WARNING: This script is performed not only on uninstall, but also
# during package update. See http://www.ibm.com/developerworks/library/l-rpm2/
# for details


if [ "$1" -eq 0 ]; then  # Action is uninstall
    /usr/sbin/ambari-agent stop > /dev/null 2>&1
    if [ -d "/etc/ambari-agent/conf.save" ]; then
        mv /etc/ambari-agent/conf.save /etc/ambari-agent/conf_$(date '+%d_%m_%y_%H_%M').save
    fi
    mv /etc/ambari-agent/conf /etc/ambari-agent/conf.save

    if [ -f "/var/lib/ambari-agent/install-helper.sh" ]; then
      /var/lib/ambari-agent/install-helper.sh remove
    fi

    chkconfig --list | grep ambari-server && chkconfig --del ambari-server
fi

exit 0



%posttrans agent
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
# limitations under the License


RESOURCE_MANAGEMENT_DIR="/usr/lib/python2.6/site-packages/resource_management"
RESOURCE_MANAGEMENT_DIR_AGENT="/usr/lib/ambari-agent/lib/resource_management"
JINJA_DIR="/usr/lib/python2.6/site-packages/ambari_jinja2"
JINJA_AGENT_DIR="/usr/lib/ambari-agent/lib/ambari_jinja2"
AMBARI_AGENT_BINARY="/etc/init.d/ambari-agent"
AMBARI_AGENT_BINARY_SYMLINK="/usr/sbin/ambari-agent"

# remove RESOURCE_MANAGEMENT_DIR if it's a directory
if [ -d "$RESOURCE_MANAGEMENT_DIR" ]; then  # resource_management dir exists
  if [ ! -L "$RESOURCE_MANAGEMENT_DIR" ]; then # resource_management dir is not link
    rm -rf "$RESOURCE_MANAGEMENT_DIR"
  fi
fi
# setting resource_management shared resource
if [ ! -d "$RESOURCE_MANAGEMENT_DIR" ]; then
  ln -s "$RESOURCE_MANAGEMENT_DIR_AGENT" "$RESOURCE_MANAGEMENT_DIR"
fi

# setting jinja2 shared resource
if [ ! -d "$JINJA_DIR" ]; then
  ln -s "$JINJA_AGENT_DIR" "$JINJA_DIR"
fi

# setting ambari-agent binary symlink
if [ ! -f "$AMBARI_AGENT_BINARY_SYMLINK" ]; then
  ln -s "$AMBARI_AGENT_BINARY" "$AMBARI_AGENT_BINARY_SYMLINK"
fi

exit 0


%package -n %{distro_select}
Summary: Distro Select
Group: Development/Libraries
AutoProv: no
AutoReqProv: no
%description -n %{distro_select}
Distro Select



%files server
%config  /etc/ambari-server/conf
%attr(644,root,root) /etc/init/ambari-server.conf
%attr(755,root,root) /etc/init.d/ambari-server
%attr(755,root,root) /etc/rc.d/init.d/ambari-server
/etc/redoop
%attr(755,root,root) /usr/sbin/ambari-server.py
%attr(755,root,root) /usr/sbin/ambari_server_main.py
/usr/lib/ambari-server
%dir  /var/lib/ambari-server/resources/upgrade
%dir %attr(755,root,root) /var/lib/ambari-server/data/tmp
%dir %attr(700,root,root) /var/lib/ambari-server/data/cache
/var/lib/ambari-server
%attr(755,root,root) /usr/lib/python2.6/site-packages/ambari_server
%dir  /var/log/ambari-server
%dir  /var/run/ambari-server
%dir  /var/run/ambari-server/bootstrap
%dir  /var/run/ambari-server/stack-recommendations



%files agent
%attr(755,root,root) /etc/ambari-agent/conf/ambari-agent.ini
%attr(755,root,root) /etc/ambari-agent/conf/logging.conf.sample
%attr(644,root,root) /etc/init/ambari-agent.conf
%attr(755,root,root) /etc/init.d/ambari-agent
%attr(755,root,root) /etc/rc.d/init.d/ambari-agent
/usr/lib/ambari-agent
%attr(755,root,root) /usr/lib/python2.6/site-packages
/var/lib/ambari-agent
%attr(644,root,root) /var/lib/ambari-agent/cred/lib/*.jar
%attr(644,root,root) /var/lib/ambari-agent/tools/*.jar
%attr(644,root,root) /var/lib/ambari-agent/cache
%dir %attr(755,root,root) /var/lib/ambari-agent/data
%dir %attr(755,root,root) /var/lib/ambari-agent/tmp
%dir %attr(755,root,root) /var/log/ambari-agent
%dir %attr(755,root,root) /var/run/ambari-agent


%files -n %{distro_select}
%attr(755,root,root) /usr/bin/%{distro_select}
%attr(755,root,root) /usr/bin/conf-select


