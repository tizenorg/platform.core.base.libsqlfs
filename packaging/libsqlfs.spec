Name:       libsqlfs
Summary:    FUSE module for filesystem on top of an SQLite db
Version:	1.1
Release:    1
Group:      TO_BE/FILLED_IN
License:    LGPLv2
Source0:    libsqlfs-%{version}.tar.gz
BuildRequires:  pkgconfig(sqlite3)
BuildRequires:  pkgconfig(fuse)
BuildRequires:  libattr-devel
BuildRequires:  libcap-devel


%description
FUSE module for filesystem on top of an SQLite database

%prep
%setup -q 


%build
gcc  $CFLAGS \
                -DFUSE \
                -D_GNU_SOURCE \
                -D_FILE_OFFSET_BITS=64 \
                -D_REENTRANT \
                -DFUSE_USE_VERSION=25 \
                -I/usr/include -I. \
                sqlfs.c fuse_main.c \
                -o libsqlfs_mount \
                $LDFLAGS \
                -L/usr/lib \
                -lpthread \
                -lfuse -lrt\
                -lsqlite3 -ldl -lcap

gcc $CFLAGS \
                sqlfs_txn_cmd.c \
                -o sqlfs_txn_cmd \
                $LDFLAGS


%install
%__mkdir_p %{buildroot}/etc/rc.d/init.d
%__mkdir_p %{buildroot}/etc/rc.d/rc3.d
%__mkdir_p %{buildroot}/etc/rc.d/rc4.d
%__mkdir_p %{buildroot}%_bindir
install -c libsqlfs_mount %{buildroot}%_bindir
install -c sqlfs_txn_cmd %{buildroot}%_bindir
install -c sqlfs-mount %{buildroot}/etc/rc.d/init.d
ln -s ../init.d/sqlfs-mount %{buildroot}/etc/rc.d/rc3.d/S10sqlfs-mount
ln -s ../init.d/sqlfs-mount %{buildroot}/etc/rc.d/rc4.d/S10sqlfs-mount


%files
%_bindir/sqlfs_txn_cmd
%_bindir/libsqlfs_mount
%_sysconfdir/rc.d/init.d/sqlfs-mount
%_sysconfdir/rc.d/rc3.d/S10sqlfs-mount
%_sysconfdir/rc.d/rc4.d/S10sqlfs-mount

