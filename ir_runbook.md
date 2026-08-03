# Incident Response Runbook — Ransomware

Condensed playbook aligned to **NIST SP 800-61** (*Computer Security Incident Handling Guide*) and the **SANS PICERL** six-step IR process. Use checkboxes to track progress during an active event.

> Phases follow NIST 800-61: **Preparation → Detection & Analysis → Containment, Eradication & Recovery → Post-Incident Activity.**

---

## Phase 1 — Preparation *(standing posture, before any incident)*

- [ ] **1.1** Maintain **offline, tested backups** and a current asset/contact list.
- [ ] **1.2** Keep this runbook, escalation paths, and legal/comms contacts up to date.
- [ ] **1.3** Ensure logging and evidence-collection tooling are in place ahead of time (SIEM, EDR, log retention, forensic workstation, write-blockers).

---

## Phase 2 — Detection & Analysis

### 1. Confirm and scope the incident.

- [ ] **2.1** Verify it really is ransomware: ransom note, mass file encryption, changed file extensions, or AV/EDR detections.
- [ ] **2.2** Determine the blast radius — which hosts, accounts, and shares are affected.
- [ ] **2.3** Record initial discovery time, reporter, and affected systems/users.
- [ ] **2.4** Build a timeline from the evidence; don't assume, confirm.

### 2. ⚠ Preserve evidence *before* you change anything.

- [ ] **2.5** Capture **volatile data first**: memory, active network connections, logged-in users.
- [ ] **2.6** Collect relevant logs (authentication, file activity, network traffic) for the incident window.
- [ ] **2.7** **Do not power off encrypted machines** — powering down destroys memory artifacts and can lose keys or decryption material. **Isolate instead of shutting down.**
- [ ] **2.8** Take forensic copies (screenshots, disk images) where feasible.

### 3. Identify patient zero and the entry vector.

- [ ] **2.9** Trace the earliest indicator of compromise (phishing, exposed RDP, brute-forced login, C2 beacon).
- [ ] **2.10** Identify attacker IP(s), domains, and classify the ransomware family (extensions, ransom note hash).
- [ ] **2.11** Determine whether data exfiltration occurred (DLP alerts, unusual outbound volume, attacker claims).
- [ ] **2.12** Assign severity, notify the IR lead, and open an incident ticket.

---

## Phase 3 — Containment, Eradication & Recovery

### 4. ⚠ Contain — isolate, don't destroy.

- [ ] **3.1** Disconnect affected hosts from the network (disable the switch port or pull the cable — **not** power off).
- [ ] **3.2** Disable compromised accounts; revoke active sessions and API keys.
- [ ] **3.3** Block attacker IPs/domains and known file hashes at the firewall, DNS, and EDR.
- [ ] **3.4** Suspend remote access (VPN, RDP) if the entry vector is unknown or still active.
- [ ] **3.5** Protect backups: verify backup repositories were not encrypted or deleted; take them offline if at risk.
- [ ] **3.6** Containment must **not** wipe the evidence preserved in Step 2.

### 5. Eradicate.

- [ ] **3.7** Remove the malware and any persistence (scheduled tasks, registry keys, new admin accounts).
- [ ] **3.8** Close the entry vector found in Step 3 (patch, reset credentials, disable the exposed service).
- [ ] **3.9** Reimage compromised hosts from known-good gold images; do not trust decryptors unless policy explicitly allows.
- [ ] **3.10** **Confirm the attacker no longer has access** before moving on to recovery.

### 6. ⚠ Recover from known-good backups.

- [ ] **3.11** Restore from **offline backups you have verified are clean**; rebuild rather than trust decryptors where possible.
- [ ] **3.12** **Do not pay the ransom as a first resort** — payment is no guarantee of recovery and funds criminal activity; escalate any payment question to leadership and legal.
- [ ] **3.13** Bring systems back in priority order (critical services first).
- [ ] **3.14** Monitor restored systems closely for reinfection.
- [ ] **3.15** Confirm business operations restored; document any data loss and systems rebuilt vs. restored.

---

## Phase 4 — Post-Incident Activity

### 7. Document everything.

- [ ] **4.1** Record the full timeline and every action taken (timestamped, with systems touched and commands run).
- [ ] **4.2** Document all indicators of compromise (IPs, domains, file hashes, accounts, affected hosts).
- [ ] **4.3** Map **MITRE ATT&CK** techniques observed (e.g., T1110 Brute Force, T1071 C2 over web protocols, T1486 Data Encrypted for Impact).
- [ ] **4.4** Archive evidence and reports per retention policy; retain chain-of-custody documentation.

### 8. Lessons learned.

- [ ] **4.5** Hold a review within 5–10 business days of closure (include all responders, not just the IR team).
- [ ] **4.6** Fix the root cause — the entry vector identified in Step 3.
- [ ] **4.7** Tune detections, update playbooks, and revise this runbook based on findings.
- [ ] **4.8** Make any required notifications (legal, regulators, affected parties) according to policy.
- [ ] **4.9** Track remediation tasks to completion (patches, MFA rollout, segmentation, monitoring gaps).

---

## Quick Reference

| NIST 800-61 Phase | SANS PICERL Step | Primary goal |
|-------------------|------------------|--------------|
| Preparation | Preparation | Be ready before an attack |
| Detection & Analysis | Identification | Confirm, preserve, and understand the incident |
| Containment, Eradication & Recovery | Containment → Eradication → Recovery | Stop spread, remove threat, restore operations |
| Post-Incident Activity | Lessons Learned | Document, learn, and improve |
