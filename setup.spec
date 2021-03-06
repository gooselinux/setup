Summary: A set of system configuration and setup files
Name: setup
Version: 2.8.14
Release: 10%{?dist}
License: Public Domain
Group: System Environment/Base
URL: https://fedorahosted.org/setup/
Source0: https://fedorahosted.org/releases/s/e/%{name}/%{name}-%{version}.tar.bz2
Patch1: setup-uidgid.patch
Patch2: setup-x11r6path.patch
Patch3: setup-pathmunge.patch
Buildroot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch: noarch
BuildRequires: bash tcsh perl
Conflicts: initscripts < 4.26, bash <= 2.0.4-21

%description
The setup package contains a set of important system configuration and
setup files, such as passwd, group, and profile.

%prep
%setup -q
%patch1 -p1
%patch2 -p1
%patch3 -p1
./shadowconvert.sh

%build

%check
# Run any sanity checks.
make check

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/etc/profile.d
cp -ar * %{buildroot}/etc
rm -f %{buildroot}/etc/uidgid
rm -f %{buildroot}/etc/COPYING
mkdir -p %{buildroot}/var/log
touch %{buildroot}/var/log/lastlog
touch %{buildroot}/etc/environment
chmod 0644 %{buildroot}/etc/environment
chmod 0400 %{buildroot}/etc/{shadow,gshadow}
chmod 0644 %{buildroot}/var/log/lastlog
touch %{buildroot}/etc/fstab
touch %{buildroot}/etc/mtab

# remove unpackaged files from the buildroot
rm -f %{buildroot}/etc/Makefile
rm -f %{buildroot}/etc/serviceslint
rm -f %{buildroot}/etc/uidgidlint
rm -f %{buildroot}/etc/shadowconvert.sh
rm -f %{buildroot}/etc/setup.spec

%clean
rm -rf %{buildroot}

#throw away useless and dangerous update stuff until rpm will be able to
#handle it ( http://rpm.org/ticket/6 )
%post -p <lua>
for i, name in ipairs({"passwd", "shadow", "group", "gshadow"}) do
     os.remove("/etc/"..name..".rpmnew")
end

%files
%defattr(-,root,root,-)
%doc uidgid COPYING
%verify(not md5 size mtime) %config(noreplace) /etc/passwd
%verify(not md5 size mtime) %config(noreplace) /etc/group
%verify(not md5 size mtime) %attr(0000,root,root) %config(noreplace,missingok) /etc/shadow
%verify(not md5 size mtime) %attr(0000,root,root) %config(noreplace,missingok) /etc/gshadow
%config(noreplace) /etc/services
%verify(not md5 size mtime) %config(noreplace) /etc/exports
%config(noreplace) /etc/aliases
%config(noreplace) /etc/environment
%config(noreplace) /etc/filesystems
%config(noreplace) /etc/host.conf
%verify(not md5 size mtime) %config(noreplace) /etc/hosts
%config(noreplace) /etc/hosts.allow
%config(noreplace) /etc/hosts.deny
%verify(not md5 size mtime) %config(noreplace) /etc/motd
%config(noreplace) /etc/printcap
%verify(not md5 size mtime) %config(noreplace) /etc/inputrc
%config(noreplace) /etc/bashrc
%config(noreplace) /etc/profile
%config(noreplace) /etc/protocols
%attr(0600,root,root) %config(noreplace,missingok) /etc/securetty
%config(noreplace) /etc/csh.login
%config(noreplace) /etc/csh.cshrc
%dir /etc/profile.d
%config(noreplace) %verify(not md5 size mtime) /etc/shells
%ghost %attr(0644,root,root) %verify(not md5 size mtime) /var/log/lastlog
%ghost %verify(not md5 size mtime) %config(noreplace,missingok) /etc/fstab
%ghost %verify(not md5 size mtime) %config(noreplace,missingok) /etc/mtab

%changelog
* Wed Jun 30 2010 Ondrej Vasik <ovasik@redhat.com> 2.8.14-10
- reserve uidgid pair 172:172 for rtkit(#609171)

* Tue Jun 15 2010 Ondrej Vasik <ovasik@redhat.com> 2.8.14-9
- reserve uidgid pair 170:170 for avahi-autoipd
- reserve uidgid pair 171:171 for pulse (pulseaudio)
- update reserved homedir for avahi
- update name of group reserved by cyrus-imapd to saslauth

* Mon May 24 2010 Ondrej Vasik <ovasik@redhat.com> 2.8.14-8
- speedup pathmunge (related #592825)

* Wed May 19 2010 Ondrej Vasik <ovasik@redhat.com> 2.8.14-7
- fix syntax error in bashrc pathmunge(since bash 3.2)(#592825)

* Tue Apr 27 2010 Ondrej Vasik <ovasik@redhat.com> 2.8.14-6
- reserve uidgid pair 140:140 for ricci daemon(#585957)
- reserve uidgid pair 141:141 for luci daemon(#585958)
- reserve uidgid pair 113:113 for usbmuxd

* Wed Mar 31 2010 Ondrej Vasik <ovasik@redhat.com> 2.8.14-5
- verify md5sum/size/mtime in the case of /etc/hosts.allow
  and /etc/hosts.deny (#578263)
- do the same for /etc/services and /etc/protocols, we
  provide (almost) complete IANA set, so no reason to modify
  it in most cases outside of setup package

* Fri Mar 26 2010 Ondrej Vasik <ovasik@redhat.com> 2.8.14-4
- get rid off obsolete X11R6 paths in csh.login script(#577268)

* Mon Jan 25 2010 Ondrej Vasik <ovasik@redhat.com> 2.8.14-2
- reserve uidgid pair 155:155 for stap-server(#555813)

* Tue Jan 12 2010 Ondrej Vasik <ovasik@redhat.com> 2.8.14-1
- reserve uidgid pair 133:133 for bacula(#554705)

* Tue Jan 05 2010 Ondrej Vasik <ovasik@redhat.com> 2.8.13-1
- update services to latest IANA
- avoid one /usr/bin/id stat call in /etc/profile

* Thu Dec 17 2009 Ondrej Vasik <ovasik@redhat.com> 2.8.12-1
- speed up pathmunge inside bashrc
- do not use deprecated egrep in profile

* Thu Dec 03 2009 Ondrej Vasik <ovasik@redhat.com> 2.8.11-1
- don't have HISTCONTROL ignorespace by default (#520632),
  but do not override it when it is already set
- add csync alias for port 2005 / tcp, udp

* Wed Nov 11 2009 Ondrej Vasik <ovasik@redhat.com> 2.8.10-1
- reserve uidgid pair 112:112 for vhostmd (#534110)
- update /etc/services to latest IANA

* Tue Sep 08 2009 Ondrej Vasik <ovasik@redhat.com> 2.8.9-1
- reserve uidgid pair 108:108 for ovirt from libvirt (#513261)
- reserve uidgid pair 111:111 for saned from sane-backends
  (#520634)

* Mon Aug 17 2009 Ondrej Vasik <ovasik@redhat.com> 2.8.8-1
- change permissions on /etc/shadow and /etc/gshadow to 0000 and
  use capabilities for them(#517577)

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.8.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Jul 21 2009 Ondrej Vasik <ovasik@redhat.com> 2.8.7-1
- increase threshold for uidgid reservations to 200
- reserve uidgid pair 107:107 for qemu (libvirt,#511957)
- reflect threshold in profile and bashrc, do inform about
  uidgid file existence there
- remove old remnants about portmap from hosts.deny(#509919)

* Mon Jun 29 2009 Ondrej Vasik <ovasik@redhat.com> 2.8.6-1
- update protocols and services to latest IANA
- add example for tty in prompt(#503304)

* Wed May 20 2009 Ondrej Vasik <ovasik@redhat.com> 2.8.5-1
- use history-search-backward/forward for pageup/pagedown
  mapping in inputrc (#500989)
- add HISTCONTROL="ignoreboth" to /etc/profile to not include
  duplicities and lines starting with space into the history
  (#500819)

* Tue May 12 2009 Ondrej Vasik <ovasik@redhat.com> 2.8.4-1
- add oprofile (16:16) to uidgid
- use os.remove instead of os.execute in lua post
  - no dependency on /bin/sh (thanks Panu Matilainen)

* Wed Apr 22 2009 Ondrej Vasik <ovasik@redhat.com> 2.8.3-2
- rewrite postun scriptlet to <lua> to prevent /bin/sh
  dependency

* Fri Apr 10 2009 Ondrej Vasik <ovasik@redhat.com> 2.8.3-1
- do not disable coredumps in profile/csh.cshrc scripts,
  coredumps already disabled in rawhide's RLIMIT_CORE(#495035)

* Wed Mar 25 2009 Ondrej Vasik <ovasik@redhat.com> 2.8.2-2
- reserve uid 65 for nslcd (will share group 55 ldap, #491899)

* Tue Mar 24 2009 Ondrej Vasik <ovasik@redhat.com> 2.8.2-1
- ship COPYING file, update protocols and services
  to latest IANA

* Mon Mar 23 2009 Ondrej Vasik <ovasik@redhat.com> 2.8.1-2
- fix sources syntax, add sources URL (#226412)

* Thu Feb 26 2009 Ondrej Vasik <ovasik@redhat.com> 2.8.1-1
- do ship/generate /etc/{shadow,gshadow} files(#483251)
- do ship default /etc/hosts with setup (#483244)
- activate multi on (required for IPv6 only localhost
  recognition out-of-the-box) (#486461)
- added postun section for cleaning of dangerous .rpmnew
  files after updates
- make profile and bashrc more portable (ksh, #487419)

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.7.7-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Feb 02 2009 Ondrej Vasik <ovasik@redhat.com> 2.7.7-4
- drop <lua> scriptlet completely(audio/video group
  temporarily created by packages which use it for
  updates(#477769))

* Fri Jan 30 2009 Ondrej Vasik <ovasik@redhat.com> 2.7.7-3
- add support for ctrl+arrow shortcut in rxvt(#474110)

* Thu Jan 29 2009 Ondrej Vasik <ovasik@redhat.com> 2.7.7-2
- reserve 87 gid for polkituser (just uid was reserved),
  reserve 18 gid for dialout(to prevent conflicts with
  polkituser gid)

* Thu Jan 22 2009 Ondrej Vasik <ovasik@redhat.com> 2.7.7-1
- synchronize /etc/services with latest IANA, do not use
  tabs in that file to have consistent output
- fix indentation in /etc/profile and /etc/bashrc
  (#481074)
- assign uid 36 for vdsm, gid 36 for kvm
  (#346151,#481021)

* Tue Jan 20 2009 Ondrej Vasik <ovasik@redhat.com> 2.7.6-1
- make uidgid file better parsable (synchronize tabs)
- reserve gid 11 for group cdrom (udev,MAKEDEV)
- reserve gid 33 for group tape (udev,MAKEDEV)
- reserve gid 87 for group dialout (udev,MAKEDEV)

* Tue Jan 06 2009 Ondrej Vasik <ovasik@redhat.com> 2.7.5-4
- use lua language in post to prevent additional
  dependencies

* Thu Dec 18 2008 Ondrej Vasik <ovasik@redhat.com> 2.7.5-3
- add pkiuser (17:17) to uidgid
- temporarily create video/audio group in post section
  (#476886)

* Wed Dec 10 2008 Ondrej Vasik <ovasik@redhat.com> 2.7.5-2
- do not export PATH twice(#449286 NOTABUG revert)
- do not export INPUTRC(to respect just created ~/.inputrc)
  (#443717)

* Thu Nov 27 2008 Ondrej Vasik <ovasik@redhat.com> 2.7.5-1
- Modified upstream URL, synchronized with upstream git

* Wed Nov 19 2008 Ondrej Vasik <ovasik@redhat.com> 2.7.4-3
- update protocols to latest IANA list (2008-04-18)
- update services to latest IANA list (2008-11-17)
- mark /etc/protocols and /etc/inputrc %%config(noreplace)
- added URL, fixed few rpmlint warnings
- do own audio and video group (#458843), create it in default
  /etc/group

* Tue Nov 18 2008 Ondrej Vasik <ovasik@redhat.com> 2.7.4-2
- again process profile.d scripts in noninteractive shells,
  but do not display stderr/stdout messages(#457243)
- fix wrong prompt for csh/tcsh (#443854)
- don't show error message about missing hostname in profile
  (#301481)
- reserve rquotad port 875 in /etc/services (#455859)
- export PATH after processing profile.d scripts (#449286)
- assign gid's for audio (:63) and video (:39) group(#458843),
  assign uidgid pair (52:52) for puppet (#471918)
- fix /etc/services duplicities to pass serviceslint

* Thu Oct 09 2008 Phil Knirsch <pknirsch@redhat.com> 2.7.4-1
- Include new serviceslint for speedup (#465642)
- Cleaned up services due to newly discovered bugs in it with new serviceslint

* Wed Sep 03 2008 Phil Knirsch <pknirsch@redhat.com> 2.7.3-1
- Added SBinSanity patch as an approved feature (#458176)

* Wed Aug 06 2008 Phil Knirsch <pknirsch@redhat.com> 2.7.2-1
- Added uidgid pair for condor
- Added uidgid pair for trousers

* Fri Jul 25 2008 Phil Knirsch <pknirsch@redhat.com> 2.7.1-1
- Bump to 2.7.1 to avoid version problems with F-9
- Removed group news as well (#437462)

* Tue Jun 17 2008 Phil Knirsch <pknirsch@redhat.com> 2.6.16-1
- Dropped user news from default /etc/passwd (#437462)

* Thu Jun 05 2008 Phil Knirsch <pknirsch@redhat.com> 2.6.15-1
- Added prelude-manager and snortd to uidgid list

* Mon Apr 07 2008 Phil Knirsch <pknirsch@redhat.com> 2.6.14-1
- Updated /etc/services to latest IANA version (#315571)

* Fri Apr 04 2008 Phil Knirsch <pknirsch@redhat.com>
- Fixed a problem with the new prompt for tcsh and screen terminal (#438550)

* Thu Mar 20 2008 Phil Knirsch <pknirsch@redhat.com> 2.6.13-1
- Drop the wrong precmd for csh for xterm and screen terminals

* Tue Feb 26 2008 Phil Knirsch <pknirsch@redhat.com> 2.6.12-1
- Corrected wrong /etc/profile.d behaviour for non-interactive bash and tcsh

* Fri Feb 22 2008 Phil Knirsch <pknirsch@redhat.com> 2.6.11-1
- Fixed problem with /etc/profile.d/* and non-interactive tcsh (#299221)
- Fixed xterm -title problem (#387581)
- Fixed problem with /etc/profile.d/*.csh not being executed for none loginshells anymore
  (#381631, #429838)
- Corrected missing shell for news user in uidgid and passwd

* Thu Aug 16 2007 Phil Knirsch <pknirsch@redhat.com> 2.6.10-1
- License review and update

* Tue Jul 24 2007 Phil Knirsch <pknirsch@redhat.com> 2.6.9-1
- Assigned uid 87 for PolicyKit package (#244950)
- Fixed precmd fix if TERM isn't set (#242732)

* Wed Jun 06 2007 Phil Knirsch <pknirsch@redhat.com> 2.6.7-1
- Fixed precmd setting to behave like bash for (t)csh (#242732)

* Thu May 24 2007 Phil Knirsch <pknirsch@redhat.com> 2.6.6-1
- Added another set of proposed changes to /etc/csh.cshrc (#199817)
- Added missing documentation in /etc/hosts.[allow|deny] (#157053)

* Wed May 23 2007 Phil Knirsch <pknirsch@redhat.com> 2.6.5-1
- Fixed tcsh behaviour for non login shells (#191233)
- Fixed umask setting for tcsh to behave identical to bash logins (#199817)
- Added ipv6-crypt and ipv6-auth for backwards compatibility (#210546)

* Wed Apr 18 2007 Phil Knirsch <pknirsch@redhat.com> 2.6.4-1
- Modified the 111/[tcp/udp] entries to work with rpcbind (#236639)

* Mon Mar 12 2007 Phil Knirsch <pknirsch@redhat.com> 2.6.3-1
- Changed winbind_auth to wbpriv by request of the samba maintainer

* Tue Dec 12 2006 Phil Knirsch <pknirsch@redhat.com> 2.6.2-1.fc7
- Updated uidgid for split of pcap into arpwatcher and tcpdump.

* Tue Nov 28 2006 Phil Knirsch <pknirsch@redhat.com> 2.6.1-1.fc7
- Update version and rebuilt

* Tue Nov 28 2006 Phil Knirsch <pknirsch@redhat.com> 2.5.57-1
- Revert change for umask in /etc/bashrc (#217523)

* Thu Nov 16 2006 Phil Knirsch <pknirsch@redhat.com> 2.5.56-1
- Added an entry for samba and winbind_auth

* Wed Oct 11 2006 Phil Knirsch <pknirsch@redhat.com> 2.5.55-1
- Extended the protocols to include the missing hopopt (#209191)

* Tue Oct 10 2006 Phil Knirsch <pknirsch@redhat.com> 2.5.54-1
- Update /etc/protocols to latest officiall IANA version (#209191)

* Thu Jul 27 2006 Phil Knirsch <pknirsch@redhat.com> 2.5.53-1
- Added utempter gid for new libutempter package (#200240)

* Mon Jun 19 2006 Phil Knirsch <pknirsch@redhat.com> 2.5.52-1
- Lock password for root account by default (#182206)

* Wed May 03 2006 Karsten Hopp <karsten@redhat.de>
- remove gkrellmd from the reserved uid/gid list (#186974)

* Tue Mar 21 2006 Florian La Roche <laroche@redhat.com> 2.5.50-1
- use stricter umask of 022 for all logins

* Thu Feb 23 2006 Phil Knirsch <pknirsch@redhat.com> 2.5.49-1
- Really switch to new /etc/services file
- Added /etc/fstab and /etc/mtab to ownership of setup (#177061)

* Tue Jan 31 2006 Phil Knirsch <pknirsch@redhat.com> 2.5.48-1
- Switched to the new large /etc/services file which fixes #112298, #133683,
  #166443, #168872, #171228.
- Fixed pathmunge problem with bashrc (#123621)
- Removed /usr/X11R6/bin from default PATH (#173856)

* Tue Jan 24 2006 Phil Knirsch <pknirsch@redhat.com>
- Fixed bug with PROMPT_COMMAND being broken for wierd dirs (#142125)
- Added hfsplus to know filesystems (#172820)

* Mon Oct 17 2005 Bill Nottingham <notting@redhat.com>
- make motd noreplace (#170539)

* Tue Sep  6 2005 Bill Nottingham <notting@redhat.com> 2.5.47-1
- make lastlog 0644  (#167200)

* Mon Jun 20 2005 Bill Nottingham <notting@redhat.com> 2.5.46-1
- add buildrequires on bash, tcsh (#161016)
- move core dump size setting from csh.login to csh.cshrc (#156914) 

* Fri Jun 17 2005 Bill Nottingham <notting@redhat.com> 2.5.45-1
- ksh doesn't implement EUID/UID. Work around that. (#160731)

* Thu May 19 2005 Bill Nottingham <notting@redhat.com> 2.5.44-1
- fix csh.cshrc when -e is used (#158265)

* Mon Apr 25 2005 Bill Nottingham <notting@redhat.com> 2.5.43-1
- remove mailman aliases (#155841)

* Mon Apr 18 2005 Bill Nottingham <notting@redhat.com> 2.5.42-1
- fix lastlog conflict (#155256)

* Fri Apr 15 2005 Bill Nottingham <notting@redhat.com> 2.5.41-1
- get rid of 'id' error messages if there is no /usr (#142707)

* Mon Jan 31 2005 Bill Nottingham <notting@redhat.com> 2.5.40-1
- have similar prompt changes for su to root in tcsh as in bash (#143826)

* Tue Nov 23 2004 Bill Nottingham <notting@redhat.com> 2.5.39-1
- ghost lastlog (#139539)

* Thu Nov 18 2004 Bill Nottingham <notting@redhat.com> 2.5.38-1
- fix bash/tcsh coredump size inconsistency (#139821)

* Wed Oct 27 2004 Bill Nottingham <notting@redhat.com> 2.5.37-1
- fix inconsistency in profile.d handling (#136859, <agrajag@dragaera.net>)

* Fri Oct  8 2004 Bill Nottingham <notting@redhat.com> 2.5.36-1
- fix duplicate alias

* Tue Sep 28 2004 Bill Nottingham <notting@redhat.com> 2.5.35-1
- add /etc/environment

* Mon Sep 27 2004 Rik van Riel <riel@redhat.com> 2.5.34-2
- mark /etc/services config(noreplace) (#133683)

* Thu Sep 23 2004 Bill Nottingham <notting@redhat.com> 2.5.34-1
- add dict (#107807)
- add cyrus services (#118832)
- move delete-char binding for csh (#113682)
- do the same path munging for csh as for bash (#57708)
- add postfix aliases (#117661)
- fix bashrc login shell check (#104491)
- add odmr to services (#101098)
- add distcc to services (#91535)
- add xterm forware/backward word bindings (#80860)

* Mon May 24 2004 Bill Nottingham <notting@redhat.com>
- make pathmunge available for profile.d scripts (#123621)

* Wed May 19 2004 Joe Orton <jorton@redhat.com> 2.5.33-2
- add IANA Register Port for svn to /etc/services (#122863)

* Wed May  5 2004 Nalin Dahyabhai <nalin@redhat.com> 2.5.33-1
- fix syntax error in csh.cshrc

* Tue May  4 2004 Bill Nottingham <notting@redhat.com> 2.5.32-1
- set MAIL in csh.cshrc (#115376)
- fix inputrc check in csh.login (#115073)

* Mon Jan 26 2004 Bill Nottingham <notting@redhat.com> 2.5.31-1
- move /etc/aliases here

* Mon Dec  8 2003 Bill Nottingham <notting@redhat.com> 2.5.30-1
- remove stty `tput kbs` section (#91357)

* Tue Sep  2 2003 Bill Nottingham <notting@redhat.com> 2.5.27-1
- securetty should be noreplace (#103585)

* Fri Mar 14 2003 Bill Nottingham <notting@redhat.com> 2.5.26-1
- clean up some typos in /etc/services (#86129)

* Mon Feb 17 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- add "console" to /etc/securetty for mainframe

* Mon Jan 20 2003 Nalin Dahyabhai <nalin@redhat.com> 2.5.24-1
- allocate uid/gid for mgetty

* Thu Jan  9 2003 Dan Walsh <dwalsh@redhat.com> 2.5.23-1
- added PXE to /etc/services 

* Wed Jan  1 2003 Bill Nottingham <notting@redhat.com> 2.5.22-1
- remove bogus entries from inputrc (#80652)

* Fri Nov 29 2002 Tim Powers <timp@redhat.com> 2.5.21-1
- remove unpackaged files from the buildroot

* Thu Aug 29 2002 Bill Nottingham <notting@redhat.com> 2.5.20-1
- shopt -s checkwinsize everywhere

* Wed Aug 28 2002 Preston Brown <pbrown@redhat.com> 2.5.19-1
- fix bug #61129 (~ substitution)

* Wed Aug 15 2002 Jens Petersen <petersen@redhat.com> 2.5.18-1
- bring back the screen case in /etc/bashrc, since /etc/screenrc no
  longer sets defhstatus (#60596, #60597)

* Sun Aug 11 2002 Florian La Roche <Florian.LaRoche@redhat.de> 2.5.17-1
- add "set mark-symlinked-directories on" to /etc/inputrc

* Mon Jul 22 2002 Phil Knirsch <pknirsch@redhat.com> 2.5.16-2
- Added shopt -s checkwinsize to /etc/bashrc for xterm resizing

* Fri Jul 19 2002 Jens Petersen <petersen@redhat.com> 2.5.16-1
- dont special case screen in /etc/bashrc, since it overrides the user's
  screenrc title setting (#60596)

* Thu Jul 18 2002 Florian La Roche <Florian.LaRoche@redhat.de> 2.5.14-1
- move home dir of "news" to /etc/news

* Tue May 28 2002 Nalin Dahyabhai <nalin@redhat.com> 2.5.13-1
- allocate uid/gid for privilege-separated sshd

* Thu May 23 2002 Tim Powers <timp@redhat.com> 2.5.12-2
- automated rebuild

* Wed Apr  3 2002 Bill Nottingham <notting@redhat.com> 2.5.12-1
- fix misformatted comment in /etc/services, allocate uid/gid for
  frontpage

* Thu Mar 28 2002 Bill Nottingham <notting@redhat.com> 2.5.11-1
- add newline in /etc/shells (#62271)

* Thu Mar 28 2002 Nalin Dahyabhai <nalin@redhat.com> 2.5.10-1
- allocate uid for the vcsa user

* Tue Mar 12 2002 Bill Nottingham <notting@redhat.com> 2.5.9-1
- re-add ext3 to /etc/filesystems

* Mon Mar 11 2002 Bill Nottingham <notting@redhat.com> 2.5.8-1
- add nologin to /etc/shells (#53963)
- fix some quoting issues (#59627)
- fix screen status line (#60596)
- fix path regexps (#59624)
- move profile.d stuff to csh.cshrc (#59946)

* Fri Mar  8 2002 Nalin Dahyabhai <nalin@redhat.com>
- add bprd, bpdbm, bpjava-msvc, vnetd, bpcd, and vopied to /etc/services

* Tue Sep 25 2001 Nalin Dahyabhai <nalin@redhat.com>
- change rmtcfg to an alias for bvcontrol, which is a registered name

* Mon Sep 17 2001 Nalin Dahyabhai <nalin@redhat.com> 2.5.7-1
- add entries to services (ipp, wnn4, and so on)
- try to remove duplicates in services (remove nameserver as alias for domain,
  and readnews as alias for netnews)

* Mon Aug 20 2001 Bill Nottingham <notting@redhat.com>
- change FTP user's home dir to /var/ftp (#52091)
- %%ghost /etc/shadow, /etc/gshadow

* Fri Aug 17 2001 Bill Nottingham <notting@redhat.com>
- add /etc/shells to filelist (#51813)

* Mon Aug 13 2001 Bill Nottingham <notting@redhat.com>
- put lock in /etc/group (#51654)

* Wed Aug  8 2001 Bill Nottingham <notting@redhat.com>
- lock only needs to be a gid
- don't set dspmbyte=euc here; do it in lang.csh, and only if necessary (#50318)

* Mon Aug  6 2001 Jeff Johnson <jbj@redhat.com>
- add lock.lock uid/gid 54 to own /var/lock directory.

* Thu Jul 19 2001 Bill Nottingham <notting@redhat.com>
- add forward/backward-word mappings (#48783)
- add pgpkeyserver port to /etc/services (#49407)

* Thu Jul 19 2001 Preston Brown <pbrown@redhat.com>
- core files disabled by default.  Developers can enable them.

* Fri Jul 13 2001 Bill Nottingham <notting@redhat.com> 2.5.1-1
- revert news user back to no shell (#48701)

* Tue Jul 10 2001 Bill Nottingham <notting@redhat.com> 2.5.0-1
- move profile.d parsing from csh.cshrc to csh.login (#47417)

* Sat Jul  7 2001 Nalin Dahyabhai <nalin@redhat.com> 2.4.15-1
- reorder /etc/services to match comments again
- protocol 118 is stp, not st
- update URLs in /etc/protocols and /etc/services

* Thu Jul  5 2001 Preston Brown <pbrown@redhat.com> 2.4.14-1
- put */sbin in path if user ID is 0.

* Mon Jun 25 2001 Bill Nottingham <notting@redhat.com>
- add an entry to /etc/services for ssh X11 forwarding (#44944)

* Wed Jun 13 2001 Bill Nottingham <notting@redhat.com>
- take ttyS0 out of securetty on main tree

* Tue Jun 12 2001 Philip Copeland <bryce@redhat.com>
- added ttyS0 to securetty for serial console usage

* Tue Jun 12 2001 Bill Nottingham <notting@redhat.com>
- add rndc to /etc/services (#40265)
- test for read bit, not execute bit, for profile.d (#35714)

* Sun Jun 03 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- add "canna" entry to /etc/services

* Mon May 21 2001 Bernhard Rosenkraenzer <bero@redhat.com> 2.4.10-1
- Fix bugs #24159 and #30634 again; whoever moved bashrc from bash
  to setup used an old version. :((

* Wed May  2 2001 Preston Brown <pbrown@redhat.com> 2.4.9-1
- bashrc moved here from bash package
- set umask in bashrc, so it applies for ALL shells.

* Fri Apr 27 2001 Preston Brown <pbrown@redhat.com> 2.4.8-1
- /sbin/nologin for accounts that aren't "real."

* Sat Apr  7 2001 Preston Brown <pbrown@redhat.com>
- revert control-arrow forward/backward word (broken)

* Tue Mar 27 2001 Preston Brown <pbrown@redhat.com>
- fix japanese input with tcsh (#33211)

* Tue Mar  6 2001 Bill Nottingham <notting@redhat.com>
- fix some weirdness with rxvt (#30799)

* Wed Feb 28 2001 Bill Nottingham <notting@redhat.com>
- add SKK input method (#29759)

* Fri Feb 23 2001 Preston Brown <pbrown@redhat.com>

* Wed Feb 21 2001 Bill Nottingham <notting@redhat.com>
- fix inputrc, Yet Again. (#28617)

* Thu Feb 15 2001 Bill Nottingham <notting@redhat.com>
- add in uidgid file, put it in %%doc

* Wed Feb  7 2001 Adrian Havill <havill@redhat.com>
- bindkey for delete in the case of tcsh

* Wed Feb  7 2001 Bill Nottingham <notting@redhat.com>
- add some more stuff to /etc/services (#25396, patch from
  <pekkas@netcore.fi>)

* Tue Feb  6 2001 Nalin Dahyabhai <nalin@redhat.com>
- add gii/tcp = 616 for gated

* Tue Jan 30 2001 Bill Nottingham <notting@redhat.com>
- wrap some inputrc settings with tests for mode, term (#24117)

* Mon Jan 29 2001 Bill Nottingham <notting@redhat.com>
- overhaul /etc/protocols (#18530)
- add port 587 to /etc/services (#25001)
- add corbaloc (#19581)
- don't set /usr/X11R6/bin in $PATH if it's already set (#19968)

* Fri Dec  1 2000 Nalin Dahyabhai <nalin@redhat.com>
- Clean up /etc/services, separating registered numbers from unregistered
  ("squatted") numbers, and adding some.

* Mon Nov 20 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- Add smtps (465/tcp) and submission (587/tcp) to /etc/services for TLS
  support (postfix >= 20001030-2)

* Sun Aug  6 2000 Bill Nottingham <notting@redhat.com>
- /var/log/lastlog is %%config(noreplace) (#15412)
- some of the various %%verify changes (#14819)

* Thu Aug  3 2000 Nalin Dahyabhai <nalin@redhat.com>
- linuxconf should be 98, not 99

* Tue Jul 25 2000 Bill Nottingham <notting@redhat.com>
- fix some of the csh stuff (#14622)

* Sun Jul 23 2000 Nalin Dahyabhai <nalin@redhat.com>
- stop setting "multi on" in /etc/host.conf

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Tue Jun 27 2000 Bill Nottingham <notting@redhat.com>
- add hfs filesystem

* Wed Jun 21 2000 Preston Brown <pbrown@redhat.com>
- printcap is a noreplace file now

* Sun Jun 18 2000 Bill Nottingham <notting@redhat.com>
- fix typo

* Tue Jun 13 2000 Nalin Dahyabhai <nalin@redhat.com>
- add linuxconf/tcp = 99 to /etc/services

* Sat Jun 10 2000 Bill Nottingham <notting@redhat.com>
- add some stuff to /etc/services
- tweak ulimit call again

* Tue Jun  6 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- homedir of ftp is now /var/ftp

* Sun May 14 2000 Nalin Dahyabhai <nalin@redhat.com>
- move profile.d logic in csh.login to csh.cshrc

* Tue Apr 18 2000 Nalin Dahyabhai <nalin@redhat.com>
- redirect ulimit -S -c to /dev/null to avoid clutter

* Thu Apr 13 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- s/ulimit -c/ulimit -S -c/ - bash 2.x adaption

* Mon Apr 03 2000 Nalin Dahyabhai <nalin@redhat.com>
- Add more of the kerberos-related services from IANA's registry and krb5

* Wed Mar 29 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- Add 2.4'ish vc/* devices to securetty

* Thu Feb 17 2000 Preston Brown <pbrown@redhat.com>
- add /etc/filesystems with sane defaults

* Wed Feb 16 2000 Bill Nottingham <notting@redhat.com>
- don't set prompt in /etc/profile (it's done in /etc/bashrc)

* Fri Feb  5 2000 Bill Nottingham <notting@redhat.com>
- yet more inputrc tweaks from Hans de Goede (hans@highrise.nl)

* Sun Jan 30 2000 Bill Nottingham <notting@redhat.com>
- yet more inputrc tweaks from Hans de Goede (hans@highrise.nl)

* Sun Jan 23 2000 Bill Nottingham <notting@redhat.com>
- fix mailq line. (#7140)

* Fri Jan 21 2000 Bill Nottingham <notting@redhat.com>
- add ldap to /etc/services

* Tue Jan 18 2000 Bill Nottingham <notting@redhat.com>
- kill HISTFILESIZE, it's broken

* Tue Jan 18 2000 Preston Brown <pbrown@redhat.com>
- some inputrc tweaks

* Wed Jan 12 2000 Bill Nottingham <notting@redhat.com>
- make some more stuff noreplace

* Fri Nov 19 1999 Bill Nottingham <notting@redhat.com>
- fix mailq line. (#7140)

* Fri Oct 29 1999 Bill Nottingham <notting@redhat.com>
- split csh.login into csh.login and csh.cshrc (#various)
- fix pop service names (#6206)
- fix ipv6 protocols entries (#6219)

* Thu Sep  2 1999 Jeff Johnson <jbj@redhat.com>
- rename /etc/csh.cshrc to /etc/csh.login (#2931).
- (note: modified /etc/csh.cshrc should end up in /etc/csh.cshrc.rpmsave)

* Fri Aug 20 1999 Jeff Johnson <jbj@redhat.com>
- add defattr.
- fix limit command in /etc/csh.cshrc (#4582).

* Thu Jul  8 1999 Bill Nottingham <notting@redhat.com>
- move /etc/inputrc here.

* Mon Apr 19 1999 Bill Nottingham <notting@redhat.com>
- always use /etc/inputrc

* Wed Mar 31 1999 Preston Brown <pbrown@redhat.com>
- added alias pointing to imap from imap2

* Tue Mar 23 1999 Preston Brown <pbrown@redhat.com>
- updated protocols/services from debian to comply with more modern 
- IETF/RFC standards

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 4)

* Thu Feb 18 1999 Jeff Johnson <jbj@redhat.com>
- unset variables used in /etc/csh.cshrc (#1212)

* Mon Jan 18 1999 Jeff Johnson <jbj@redhat.com>
- compile for Raw Hide.

* Tue Oct 13 1998 Cristian Gafton <gafton@redhat.com>
- fix the csh.cshrc re: ${PATH} undefined

* Mon Apr 27 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Fri Dec 05 1997 Erik Troan <ewt@redhat.com>
- /etc/profile uses $i, which needs to be unset

* Mon Nov 03 1997 Donnie Barnes <djb@redhat.com>
- made /etc/passwd and /etc/group %%config(noreplace)

* Mon Oct 20 1997 Erik Troan <ewt@redhat.com>
- removed /etc/inetd.conf, /etc/rpc
- flagged /etc/securetty as missingok
- fixed buildroot stuff in spec file

* Thu Jul 31 1997 Erik Troan <ewt@redhat.com>
- made a noarch package

* Wed Apr 16 1997 Erik Troan <ewt@redhat.com>
- Don't verify md5sum, size, or timestamp of /var/log/lastlog, /etc/passwd,
  or /etc/group.
