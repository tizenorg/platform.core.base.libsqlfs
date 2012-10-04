Name:       libsqlfs
Summary:    FUSE module for filesystem on top of an SQLite db
Version:    1.2
Release:    8
Group:      TO_BE/FILLED_IN
License:    LGPLv2
Source0:    libsqlfs-%{version}.tar.gz
Source1:    opt-var-kdb-db.mount
Source4:    mount.fuse.libsqlfs
Source5:    opt-var-kdb-db-libsqlfs.service
BuildRequires:  pkgconfig(sqlite3)
BuildRequires:  pkgconfig(fuse)
BuildRequires:  libattr-devel
BuildRequires:  libcap-devel
Requires:       /usr/bin/find
Requires(post):   systemd 
Requires(postun): systemd


%description
FUSE module for filesystem on top of an SQLite database

%prep
%setup -q 

%build
#%configure
#make

gcc  $(CFLAGS) -g \
                -DFUSE \
                -D_GNU_SOURCE \
                -D_FILE_OFFSET_BITS=64 \
                -D_REENTRANT \
                -DFUSE_USE_VERSION=25 \
                -I/usr/include -I. \
                sqlfs.c fuse_main.c \
                -o libsqlfs_mount \
                $(LDFLAGS) \
                -L/usr/lib \
                -lpthread \
                -lfuse -lrt\
                -lsqlite3 -ldl -lcap

gcc $(CFLAGS) -g \
                sqlfs_txn_cmd.c \
                -o sqlfs_txn_cmd \
                $(LDFLAGS)


%install
mkdir -p %{buildroot}%{_bindir}
install -m 0755 libsqlfs_mount %{buildroot}%{_bindir}/
install -m 0755 sqlfs_txn_cmd %{buildroot}%{_bindir}/
mkdir -p %{buildroot}/sbin
install -m 0755 %{SOURCE4} %{buildroot}/sbin/

mkdir -p %{buildroot}%{_libdir}/systemd/system/basic.target.wants
install -m 0644 %{SOURCE1} %{buildroot}%{_libdir}/systemd/system/
install -m 0644 %{SOURCE5} %{buildroot}%{_libdir}/systemd/system/
ln -sf ../opt-var-kdb-db-libsqlfs.service %{buildroot}%{_libdir}/systemd/system/basic.target.wants/

mkdir -p %{buildroot}%{_sysconfdir}/rc.d/init.d
mkdir -p %{buildroot}%{_sysconfdir}/rc.d/rc3.d
mkdir -p %{buildroot}%{_sysconfdir}/rc.d/rc4.d
install -m 0755 sqlfs-mount %{buildroot}%{_sysconfdir}/rc.d/init.d
ln -s ../init.d/sqlfs-mount %{buildroot}%{_sysconfdir}/rc.d/rc3.d/S03sqlfs-mount
ln -s ../init.d/sqlfs-mount %{buildroot}%{_sysconfdir}/rc.d/rc4.d/S03sqlfs-mount


%post
systemctl daemon-reload
 
%postun
systemctl daemon-reload


%files
%{_sysconfdir}/rc.d/init.d/sqlfs-mount
%{_sysconfdir}/rc.d/rc3.d/S03sqlfs-mount
%{_sysconfdir}/rc.d/rc4.d/S03sqlfs-mount
/sbin/mount.fuse.libsqlfs
%{_bindir}/sqlfs_txn_cmd
%{_bindir}/libsqlfs_mount
%{_libdir}/systemd/system/opt-var-kdb-db.mount
%{_libdir}/systemd/system/opt-var-kdb-db-libsqlfs.service
%{_libdir}/systemd/system/basic.target.wants/opt-var-kdb-db-libsqlfs.service

%changelog
* Thu Jul 12 2012 - Hyungdeuk Kim <hd3.kim@samsung.com>
- Add -g flags to spec file for exe file strip
