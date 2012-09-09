%define runuser toruser

Name:		tor
Version:	0.2.2.38
Release:	%mkrel 1
Summary:	Anonymizing overlay network for TCP (The onion router)
URL:		http://www.torproject.org/
Group:		Networking/Other
License:	BSD-like
Requires(pre):	rpm-helper
Requires(post):	rpm-helper
Requires(preun):	rpm-helper
Requires(postun):	rpm-helper
Requires:	openssl >= 0.9.6
Requires:	tsocks
BuildRequires:	openssl-devel >= 0.9.6 
BuildRequires:	libevent-devel
BuildRequires:	zlib-devel
BuildRequires:	autoconf2.5
Source0:	http://www.torproject.org/dist/%{name}-%{version}.tar.gz
Source1:	%{name}.logrotate
Source2:	%{name}.init
Source3: 	%{name}.sysconfig

%description
Tor is a connection-based low-latency anonymous communication system.

This package provides the "tor" program, which serves as both a client and
a relay node. Scripts will automatically create a "%{runuser}" user and
group, and set tor up to run as a daemon when the system is rebooted.

Applications connect to the local Tor proxy using the SOCKS
protocol. The local proxy chooses a path through a set of relays, in
which each relay knows its predecessor and successor, but no
others. Traffic flowing down the circuit is unwrapped by a symmetric
key at each relay, which reveals the downstream relay.

Warnings: Tor does no protocol cleaning.  That means there is a danger
that application protocols and associated programs can be induced to
reveal information about the initiator. Tor depends on Privoxy and
similar protocol cleaners to solve this problem. This is alpha code,
and is even more likely than released code to have anonymity-spoiling
bugs. The present network is very small -- this further reduces the
strength of the anonymity provided. Tor is not presently suitable
for high-stakes anonymity.

%prep
%setup -q 
 
%build
%configure2_5x
%make

%install
%makeinstall

%define _logdir %{_var}/log

mkdir -p %{buildroot}%{_initrddir}
cat %{SOURCE2} > %{buildroot}%{_initrddir}/%{name}
chmod 0755 %{buildroot}%{_initrddir}/%{name}

install -p -m 644 %{buildroot}%{_sysconfdir}/%{name}/torrc.sample %{buildroot}%{_sysconfdir}/%{name}/torrc

mkdir -p -m 755 %{buildroot}%{_sysconfdir}/logrotate.d
cat %{SOURCE1} > %{buildroot}%{_sysconfdir}/logrotate.d/%{name}

mkdir -p -m 755 %{buildroot}%{_sysconfdir}/sysconfig/
cat %{SOURCE3} > %{buildroot}%{_sysconfdir}/sysconfig/%{name}

mkdir -p -m 700 %{buildroot}%{_localstatedir}/lib/%{name}
mkdir -p -m 755 %{buildroot}%{_var}/run/%{name}
mkdir -p -m 755 %{buildroot}%{_logdir}/%{name}

# Bash completion
mkdir -p %{buildroot}%{_sysconfdir}/bash_completion.d
echo 'complete -F _command $filenames torify' > %{buildroot}%{_sysconfdir}/bash_completion.d/%{name}

%pre
%_pre_useradd %{runuser} / /bin/false

%post
%_post_service %{name}

%preun
%_preun_service %{name}
rm -f %{_localstatedir}/%{name}/cached-directory
rm -f %{_localstatedir}/%{name}/bw_accounting
rm -f %{_localstatedir}/%{name}/control_auth_cookie
rm -f %{_localstatedir}/%{name}/router.desc
rm -f %{_localstatedir}/%{name}/fingerprint

%postun
%_postun_userdel %{runuser}
%_postun_groupdel %{runuser}

%files
%defattr(-,root,root)
%doc LICENSE README ChangeLog ReleaseNotes doc/HACKING doc/TODO 
%{_mandir}/man*/*
%{_bindir}/tor
%{_bindir}/torify
%{_bindir}/tor-resolve
%{_bindir}/tor-gencert
%config(noreplace) %attr(0755,%{runuser},%{runuser}) %{_initrddir}/%{name}
%config(noreplace) %attr(0644,root,root) %{_sysconfdir}/logrotate.d/%{name}
%dir %attr(0755,root,%{runuser}) %{_sysconfdir}/%{name}/
%config(noreplace) %attr(0644,root,%{runuser}) %{_sysconfdir}/%{name}/*
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%attr(0700,%{runuser},%{runuser}) %dir %{_localstatedir}/lib/%{name}
%attr(0750,%{runuser},%{runuser}) %dir %{_var}/run/%{name}
%attr(0750,%{runuser},%{runuser}) %dir %{_logdir}/%{name}
%{_sysconfdir}/bash_completion.d/%{name}
%{_datadir}/%{name}
