%define runuser toruser

Name:		tor
Version:	0.2.2.39
Release:	1
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


%changelog
* Sun Sep 09 2012 Dmitry Mikhirev <dmikhirev@mandriva.org> 0.2.2.38-1mdv2012.0
+ Revision: 816596
- update to 0.2.2.38

* Sun Jan 22 2012 Lev Givon <lev@mandriva.org> 0.2.2.35-1
+ Revision: 765034
- Update to 0.2.2.35.

* Sun Feb 27 2011 Funda Wang <fwang@mandriva.org> 0.2.1.30-1
+ Revision: 640335
- update to new version 0.2.1.30

* Wed Jan 19 2011 Funda Wang <fwang@mandriva.org> 0.2.1.29-1
+ Revision: 631656
- update to new version 0.2.1.29

* Wed Dec 22 2010 Oden Eriksson <oeriksson@mandriva.com> 0.2.1.28-2mdv2011.0
+ Revision: 623881
- rebuilt against libevent 2.x

* Mon Dec 20 2010 Funda Wang <fwang@mandriva.org> 0.2.1.28-1mdv2011.0
+ Revision: 623334
- update to new version 0.2.1.28

* Sat Nov 27 2010 Funda Wang <fwang@mandriva.org> 0.2.1.27-1mdv2011.0
+ Revision: 601752
- update to new version 0.2.1.27

  + Matthew Dawkins <mattydaw@mandriva.org>
    - added missing ghostscript BR

* Tue Jun 15 2010 Pascal Terjan <pterjan@mandriva.org> 0.2.1.26-1mdv2010.1
+ Revision: 548070
- Update to 0.2.1.26 (bugfixes)

* Mon Apr 12 2010 Funda Wang <fwang@mandriva.org> 0.2.1.25-2mdv2010.1
+ Revision: 533634
- rebuild

* Tue Mar 30 2010 Pascal Terjan <pterjan@mandriva.org> 0.2.1.25-1mdv2010.1
+ Revision: 529894
- update to new version 0.2.1.25

* Wed Mar 03 2010 Sandro Cazzaniga <kharec@mandriva.org> 0.2.1.24-1mdv2010.1
+ Revision: 513772
- Update to 0.2.1.24

* Thu Jan 21 2010 Michael Scherer <misc@mandriva.org> 0.2.1.22-1mdv2010.1
+ Revision: 494519
- new version
- update website url

* Tue Dec 29 2009 Pascal Terjan <pterjan@mandriva.org> 0.2.1.21-1mdv2010.1
+ Revision: 483281
- Update to 0.2.1.21

* Sun Dec 20 2009 Pascal Terjan <pterjan@mandriva.org> 0.2.1.20-2mdv2010.1
+ Revision: 480257
- Add upstream fix for new openssl

* Fri Nov 13 2009 Pascal Terjan <pterjan@mandriva.org> 0.2.1.20-1mdv2010.1
+ Revision: 465828
- update to new version 0.2.1.20

* Thu Aug 06 2009 Michael Scherer <misc@mandriva.org> 0.2.1.19-1mdv2010.0
+ Revision: 410624
- update to new version 0.2.1.19

* Fri Jun 26 2009 Pascal Terjan <pterjan@mandriva.org> 0.2.0.35-1mdv2010.0
+ Revision: 389362
- update to new version 0.2.0.35
- hide reload error after logrotate

* Tue Feb 10 2009 Pascal Terjan <pterjan@mandriva.org> 0.2.0.34-1mdv2009.1
+ Revision: 339154
- Update to 0.2.0.34

* Thu Jan 22 2009 Frederik Himpe <fhimpe@mandriva.org> 0.2.0.33-1mdv2009.1
+ Revision: 332633
- update to new version 0.2.0.33

* Mon Nov 24 2008 Pascal Terjan <pterjan@mandriva.org> 0.2.0.32-1mdv2009.1
+ Revision: 306255
- Group is no longer a valid option
- start tor as root and let it switch to its user
- Update to 0.2.0.32
- Stop using initlog

  + Michael Scherer <misc@mandriva.org>
    - fix %%preun

* Tue Sep 09 2008 Frederik Himpe <fhimpe@mandriva.org> 0.2.0.31-1mdv2009.0
+ Revision: 283173
- update to new version 0.2.0.31

* Wed Jul 23 2008 Pascal Terjan <pterjan@mandriva.org> 0.2.0.30-1mdv2009.0
+ Revision: 242320
- Drop P0
- Add back accidentaly dropped sources
- Switch to 0.2.0.* branch

* Thu Jul 03 2008 Michael Scherer <misc@mandriva.org> 0.1.2.19-3mdv2009.0
+ Revision: 230955
- add patch0, to build with fortify. Since /dev/null should not be created if
  it doesn't exist, i removed the O_CREATE flag, instead of adding creation mode.
- add a config file in /etc/sysconfig/tor, so the user
  can cleanly raise the limit of opened file with ulimit -n with touching
  to initscript.

  + Pixel <pixel@mandriva.com>
    - adapt to %%_localstatedir now being /var instead of /var/lib (#22312)

* Wed May 14 2008 Oden Eriksson <oeriksson@mandriva.com> 0.1.2.19-2mdv2009.0
+ Revision: 207049
- rebuilt against libevent-1.4.4

* Sun Jan 20 2008 Pascal Terjan <pterjan@mandriva.org> 0.1.2.19-1mdv2008.1
+ Revision: 155377
- update to new version 0.1.2.19

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Wed Nov 07 2007 Funda Wang <fwang@mandriva.org> 0.1.2.18-2mdv2008.1
+ Revision: 106704
- rebuild for new lzma

* Wed Oct 31 2007 Pascal Terjan <pterjan@mandriva.org> 0.1.2.18-1mdv2008.1
+ Revision: 104166
- update to new version 0.1.2.18

* Sun Sep 02 2007 Funda Wang <fwang@mandriva.org> 0.1.2.17-1mdv2008.0
+ Revision: 77742
- New version 0.1.2.17

* Fri Aug 03 2007 Pascal Terjan <pterjan@mandriva.org> 0.1.2.16-1mdv2008.0
+ Revision: 58448
- update to new version 0.1.2.16

* Mon Jul 23 2007 Pascal Terjan <pterjan@mandriva.org> 0.1.2.15-1mdv2008.0
+ Revision: 54629
- update to new version 0.1.2.15

* Sat May 26 2007 Pascal Terjan <pterjan@mandriva.org> 0.1.2.14-1mdv2008.0
+ Revision: 31230
- 0.1.2.14

* Fri May 11 2007 David Walluck <walluck@mandriva.org> 0.1.2.13-2mdv2008.0
+ Revision: 26281
- LSB initscript

* Wed Apr 25 2007 Pascal Terjan <pterjan@mandriva.org> 0.1.2.13-1mdv2008.0
+ Revision: 18291
- 0.1.2.13 (first stable release of 1.2 branch)


* Sun Mar 04 2007 Adam Williamson <awilliamson@mandriva.com> 0.1.1.26-2mdv2007.0
+ Revision: 132717
- rebuild to fix 29130

* Sun Dec 17 2006 Pascal Terjan <pterjan@mandriva.org> 0.1.1.26-1mdv2007.1
+ Revision: 98257
- 0.1.1.26 (fixes a serious privacy bug for people who use the HttpProxyAuthenticator config option)

* Thu Nov 09 2006 Pascal Terjan <pterjan@mandriva.org> 0.1.1.25-1mdv2007.0
+ Revision: 79733
- 0.1.1.25
- Add bash completion for torify
- Import tor

* Sun Sep 03 2006 Pascal Terjan <pterjan@mandriva.org> 0.1.1.23-2mdv2007.0
- Require tsocks for torify

* Wed Aug 16 2006 Pascal Terjan <pterjan@mandriva.org> 0.1.1.23-1mdv2007.0
- New release 0.1.1.23

* Sun Jul 09 2006 Pascal Terjan <pterjan@mandriva.org> 0.1.1.22-1mdv2007.0
- New release 0.1.1.22
- Fix macro in changelog

* Wed Jun 14 2006 Lenny Cartier <lenny@mandriva.com> 0.1.1.21-1mdv2007.0
- 0.1.1.21

* Fri May 26 2006 Pascal Terjan <pterjan@mandriva.org> 0.1.1.20-1mdv2007.0
- New release 0.1.1.20
- use autoconf2.5
- buildrequires latex and transfig for the doc

* Sat Mar 11 2006 Pascal Terjan <pterjan@mandriva.org> 0.1.0.17-1mdk
- New release 0.1.0.17

* Thu Jan 05 2006 Pascal Terjan <pterjan@mandriva.org> 0.1.0.16-1mdk
- 0.1.0.16

* Wed Nov 23 2005 Laurent MONTEL <lmontel@mandriva.com> 0.1.0.15-4
- Rebuild with new openssl

* Thu Oct 20 2005 Nicolas Lécureuil <neoclust@mandriva.org> 0.1.0.15-3mdk
- Fix BuildRequires

* Wed Sep 28 2005 Lev Givon <lev@columbia.edu> 0.1.0.15-2mdk
- Define %%{_logdir} macro

* Sun Sep 25 2005 Pascal Terjan <pterjan@mandriva.org> 0.1.0.15-1mdk
- 0.1.0.15

* Wed Aug 17 2005 Pascal Terjan <pterjan@mandriva.org> 0.1.0.14-2mdk
- Add forgotten changelog

* Wed Aug 17 2005 Pascal Terjan <pterjan@mandriva.org> 0.1.0.14-1mdk
- 0.1.0.14 (security fix)

* Mon Aug 08 2005 Pascal Terjan <pterjan@zarb.org> 0.1.0.13-1mdk
- 0.1.0.13

* Mon Aug 08 2005 Pascal Terjan <pterjan@zarb.org> 0.1.0.12-1mdk
- first Mandriva version (partially based on the official rpm)

