Lab 1 — Meet Your AI & Start The Investigator
A.	What is a phishing email?
Generic: A phishing email is a fraudulent message designed to trick you into giving up sensitive information — like passwords, credit card numbers, or bank details — or into installing malware on your device.
How they typically work:
1.	Impersonation — The email pretends to be from a trusted source: your bank, a company you use (Amazon, Microsoft, PayPal), a coworker, or even a government agency.
2.	Urgency or fear — It often creates pressure: "Your account has been suspended," "Unusual sign-in detected," "Payment failed, act now."
3.	A call to action — It asks you to click a link, download an attachment, or reply with personal information.
4.	A fake destination — The link usually leads to a lookalike website that mimics the real one, where anything you type gets stolen.
Common warning signs:
•	Mismatched or suspicious sender email addresses (e.g., support@amaz0n-security.com instead of amazon.com)
•	Generic greetings like "Dear Customer" instead of your actual name
•	Spelling and grammar errors
•	Urgent or threatening language
•	Requests for sensitive info (banks/legitimate companies rarely ask for passwords or full card numbers via email)
•	Links that don't match the company's real domain when you hover over them
•	Unexpected attachments, especially .zip, .exe, or macro-enabled Office files
Variants worth knowing:
•	Spear phishing — targeted at a specific person, often using personal details to seem more credible
•	Whaling — targets high-profile individuals like executives
•	Smishing/vishing — the same tactic via text message or phone call
If you get one: don't click links or download attachments, don't reply, verify by contacting the company directly through their official website or phone number, and report/delete the email.
Want tips on how to check a suspicious email you received, or how to set up better email filtering?

Investigator: Assume the role of a brand new network operations technician, list the top 5 things to keep in mind regarding phishing. Keep the list to bullets (1 subheading per bullet).
Response: •  Verify the sender, not just the display name. Attackers spoof display names easily. Check the actual email address/domain for subtle misspellings (e.g., "rnicrosoft.com" or "support@company-verify.net") before trusting a message, especially ones claiming to be from vendors, ticketing systems, or leadership. 
•  Be extra cautious with urgency and authority cues. Phishing (and especially "vishing"/spear-phishing aimed at NOC staff) often impersonates a manager, exec, or critical vendor and pressures you to act fast — reset a password, approve access, click a "critical alert" link. Slow down and verify through a separate channel (phone, Slack, in person) before acting. 
•  Never enter credentials from a link in an email or chat message. Always navigate to internal tools, monitoring dashboards, or admin portals directly via bookmarks or typed URLs, not by clicking through. NOC credentials are high-value targets because they often grant broad network access. 
•  Watch for lookalike alerts and tooling. Attackers sometimes mimic monitoring/alerting emails (Nagios, PagerDuty, Zabbix, ticketing systems) or fake "system down" notifications to get you to click a malicious link during a moment of stress. Confirm alerts match expected formatting and originate from known internal systems. 
•  Report, don't just delete. If something looks like phishing, report it to your security team or use the official "report phishing" function rather than ignoring or deleting it — your report could be the first signal of a broader campaign targeting the network team specifically.
 
Three Favorites:
1.	In the NOC, elaborate on identifying lookalike spoofs
Good instinct to dig into this one — NOC teams are a favorite target because a single successful spoof can hand an attacker legitimate-looking access to monitoring and alerting infrastructure. Here's a deeper breakdown:
1. Domain and URL lookalikes
•	Character substitution/typosquatting: paloalto-networks.com vs paloaIto-networks.com (capital I instead of lowercase l), or zabbix-alerts.com vs zabbix-alerts.net. Read domains character by character, not at a glance.
•	Homoglyph attacks: Unicode characters that look identical to ASCII (Cyrillic "а" vs Latin "a"). These can pass visual inspection entirely. If something feels off, copy the URL into a plain text editor or hover to inspect the actual rendered link/hex.
•	Subdomain tricks: yourcompany.com.status-alerts.io — the real domain is status-alerts.io; yourcompany.com is just a subdomain designed to catch a quick glance.
•	Extra/missing hyphens or words: service-now.com vs servicenow.com, or pagerduty-alerts.com (not an official PagerDuty domain).
2. Email header inconsistencies
•	Display name says "Datadog Alerts" but the reply-to or return-path domain doesn't match Datadog's known sending domains.
•	Check SPF/DKIM/DMARC pass-fail status if your mail client shows it — a failed authentication check on a "monitoring system" email is a major red flag.
•	Legitimate automated alerts usually come from consistent, known sending infrastructure. A sudden change in sending domain or format for a tool you see alerts from daily is worth a second look.
3. Formatting and content tells
•	Fake alert emails often copy visual branding well but get details wrong: incorrect ticket number formats, wrong severity taxonomy, off-brand terminology, or slightly different logo/color rendering.
•	Generic greetings ("Dear User") instead of your actual name or team alias, when the real system always personalizes.
•	Links that don't match the anchor text — hover (don't click) to see where a "View Incident" button actually points.
2.	In the context of a network engineer, explain the ease of access of native vs nat.
Good question — this comes up constantly when designing network architecture, especially around exposing services, remote access, and troubleshooting. Here's the breakdown:
Native (Direct/Public) Addressing
What it means: A device has a globally routable IP address (or is directly reachable within a flat routing domain) with no translation occurring between it and the requester.
Ease of access:
•	Very easy — arguably too easy. Any host that knows the IP can initiate a connection directly, assuming routing and firewall rules allow it.
•	No translation state to maintain, no session tracking overhead, no ambiguity about "which internal host does this packet belong to."
•	Troubleshooting is simpler: what you see in a packet capture upstream is exactly the source/destination the endpoint itself sees. No need to correlate NAT tables to figure out who actually sent what.
•	The tradeoff: this ease of access is also the security liability. Every natively addressed device is a potential direct target unless something else (host firewall, ACLs, segmentation) is doing the gatekeeping. This is why native/public addressing is typically reserved for things that need to be reachable — web servers, VPN concentrators, edge routers — not for internal workstations or NOC tooling.
NAT (Network Address Translation)
What it means: Internal, typically private (RFC 1918) addresses are translated to a different address — usually a shared public IP — at a boundary device before traffic leaves the network.
Ease of access:
•	Much harder from the outside in, by design. Inbound connections can't reach an internal host unless there's an explicit translation rule (static NAT, port forwarding, or an established outbound session for dynamic/PAT).
•	This makes NAT an incidental security boundary — not a substitute for a firewall, but a practical byproduct: unsolicited inbound traffic simply has nowhere to go without a mapping.
•	From the inside out, access is largely unaffected for typical use — outbound-initiated sessions (web browsing, API calls, agent check-ins) work transparently thanks to PAT (Port Address Translation), which is why NAT scales so well for client-heavy networks.
•	Operational cost: NAT adds complexity for you as the engineer. You're maintaining translation tables, troubleshooting requires correlating pre- and post-NAT addresses (which matters a lot in packet captures and log correlation), and certain protocols that embed IP info in their payload (some VoIP/SIP, older FTP, some VPN protocols) need ALGs or special handling to work through NAT cleanly.
•	Peer-to-peer or inbound-initiated traffic (remote access to an internal box, hosting a service behind NAT) requires deliberate configuration — port forwarding, static NAT entries, or a VPN/tunnel — it doesn't happen by accident.

Practical NOC takeaway	Native/Public	NAT
Inbound access	Easy by default	Blocked by default, needs explicit mapping
Outbound access	Easy	Easy (transparent via PAT)
Troubleshooting	Simpler correlation	Requires NAT table/log correlation
Attack surface	Higher if unmanaged	Lower by default (not a firewall substitute)
Address conservation	None — needs real IPv4 space	High — many hosts share few public IPs
In most enterprise NOC environments, you'll see a mix: NAT for the bulk of the internal fleet (workstations, most servers) and native/public addressing reserved for edge-facing infrastructure that's meant to be reached — with firewalls doing the real access control in both cases rather than relying on NAT as a security feature.


 
3.	As a wireless security engineer, name the top 3 things to lookout for when having "Guest" wifi.

Here's the top 3 from a wireless security engineer's perspective:
•	Network segmentation and isolation. Guest WiFi must be logically and ideally physically separated from your internal/corporate network — typically via a dedicated VLAN with strict firewall rules preventing any routing to internal subnets, servers, or management interfaces. Also enable client isolation (sometimes called AP isolation or peer-to-peer blocking) so guest devices can't see or attack each other — this stops a compromised guest laptop from pivoting laterally to another guest's phone or laptop on the same SSID.
•	Bandwidth and access controls. Without rate limiting, a handful of guest users can saturate your uplink (streaming, large downloads, or even someone running a personal hotspot off your network). Implement bandwidth caps per client, session timeouts/re-authentication requirements, and consider a captive portal with acceptable use terms — both for liability coverage and to force periodic re-auth rather than leaving sessions open indefinitely.
•	Authentication and visibility. Open, unauthenticated guest networks are an easy vector for abuse (illegal downloads, attacks launched from your IP space, or just freeloading). At minimum use a captive portal with logging (who connected, when, MAC address, traffic volume) — ideally tied to some form of identity (email, SMS verification, sponsor approval) so you have accountability and can trace incidents back to a session if something malicious originates from your guest network. Also make sure logging/retention meets whatever compliance requirements apply to your organization.
One thing worth flagging as a bonus: rogue AP awareness on the guest SSID's frequency space — since guest networks are often lower-priority in monitoring, they're a common place for an attacker to set up an evil twin AP mimicking your guest SSID to harvest credentials or MITM traffic. Worth including guest SSIDs in your WIDS/WIPS monitoring, not just your corporate ones.

Reflection
1.	What changed between the “plain question” answer and the “you are a SOC analyst” answer? Why does that matter for building a tool?
a.	The plain question gave the broadest and highest level explanation of phishing, while the SOC analyst answer was able to ‘understand’ that the user does not need a high level explanation and do not need definitions for basic networking concepts. The specific prompt does not ‘dance around the question’ but simply analyzes the specific prompt from the user.
2.	After this week’s deepfake story, what’s one thing about AI in security that surprised you or stuck with you?
a.	The thing that stuck with me the most about the Hong Kong finance deepfake disaster was the simple fact that people will not do their due diligence if something is ‘routine’ or they trust the person. I cannot fathom doing a 25 million dollar deal over video call to begin with, let alone in the age of smoke and mirrors on the internet. I feel that the real lesson is that there are reasons for validation and authentication of important information and finances, and need to be followed. With deep-fake technology improving seemingly overnight, everyone needs to be on their toes to spot phishy behavior.
3.	One sentence: what do you hope The Investigator can do by Week 8?
a.	I hope the investigator is able to pinpoint flaws in my thinking of network security and reinforce current concepts I know already.

