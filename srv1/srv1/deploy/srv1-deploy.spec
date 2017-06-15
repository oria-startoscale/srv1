%define longhash %(git log | head -1 | awk '{print $2}')
%define shorthash %(echo %{longhash} | dd bs=1 count=12)

Name:    srv1-deploy
Version: 1.0
Release: 1.strato.%{shorthash}
Summary: srv1 service deploy
Packager: Stratoscale Ltd
Vendor: Stratoscale Ltd
URL: http://www.stratoscale.com
#Source0: THIS_GIT_COMMIT
License: Strato

%define __strip /bin/true
%define __spec_install_port /usr/lib/rpm/brp-compress

%description
srv1 service deployment

%build
cp %{_srcdir}/deploy/srv1-api.service .
cp %{_srcdir}/deploy/srv1-api.yml .
cp %{_srcdir}/deploy/srv1-monitor.service .
cp %{_srcdir}/deploy/srv1-worker.service .
cp %{_srcdir}/deploy/srv1-worker.yml .

%install
install -p -D -m 655 srv1-api.service $RPM_BUILD_ROOT/usr/lib/systemd/system/srv1-api.service
install -p -D -m 655 srv1-api.yml $RPM_BUILD_ROOT/etc/stratoscale/compose/rootfs-star/srv1-api.yml
install -p -D -m 655 srv1-monitor.service $RPM_BUILD_ROOT/etc/stratoscale/clustermanager/services/control/srv1.service
install -p -D -m 655 srv1-worker.service $RPM_BUILD_ROOT/usr/lib/systemd/system/srv1-worker.service
install -p -D -m 655 srv1-worker.yml $RPM_BUILD_ROOT/etc/stratoscale/compose/rootfs-star/srv1-worker.yml


%files
/usr/lib/systemd/system/srv1-api.service
/etc/stratoscale/compose/rootfs-star/srv1-api.yml
/etc/stratoscale/clustermanager/services/control/srv1.service
/usr/lib/systemd/system/srv1-worker.service
/etc/stratoscale/compose/rootfs-star/srv1-worker.yml