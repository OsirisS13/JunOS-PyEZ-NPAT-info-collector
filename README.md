# JunOS-PyEZ-info-collector
Implementation of Juniper's PyEZ module to collect information from JunOS devices.  This specific implementation is an alternative to the following commands in the CLI

|Output description |	JuniperRouter commands | 
| --- |
|Config	| show config|display inheritance|no-more
Equipment cli	show configuration system host-name | display inheritance
show version|no-more
show chassis hardware|no-more
show chassis fpc|no-more
show chassis hardware models|no-more
Interface	show configuration system host-name | display inheritance
show interfaces|no-more
                                                     
OPTIONAL (only required if MPLS-TE  tunnels are deployed)
 
Topology	show ted database extensive|no-more    (only required for a single router)
Transit Tunnel	show configuration system host-name | display inheritance
show rsvp session ingress detail logical-router all|no-more
show rsvp session transit detail logical-router all|no-more
Tunnel Path	show configuration system host-name | display inheritance
show mpls lsp statistics ingress extensive logical-router all|no-more
 
