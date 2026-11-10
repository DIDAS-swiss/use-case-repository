### Use case

Diploma and qualification verification by employers

### Short id (optional)

diploma-employer-verification

### Title in German, French and Italian (optional)

DE: Prüfung von Diplomen durch Arbeitgeber

### Summary

When hiring, employers, recruiters and staffing firms check that a candidate holds the qualifications the role requires; DIDAS describes today's practice as checking PDF or paper copies and, in doubt, contacting the school (DIDAS assessment, not an official finding). With verifiable diplomas the candidate presents the qualification from the wallet and the employer checks issuer and authenticity directly. swiyu lists diplomas from educational institutions as a credential type (swiyu – Ökosystem; swiyu – Behörden). No official pilot of employer verification is documented; the introduction of the e-ID has been postponed with no new date, and the trust infrastructure (swiyu) is expected in H1 2027 (Federal Council / BJ, 30.06.2026).

**DE:**

Bei der Anstellung prüfen Arbeitgeber, Recruiter und Personalverleiher, ob eine Kandidatin oder ein Kandidat die für die Stelle nötigen Qualifikationen besitzt; DIDAS beschreibt die heutige Praxis als Prüfung von PDF- oder Papierkopien und, im Zweifel, als Rückfrage bei der Schule (Einschätzung DIDAS, kein offizieller Befund). Mit prüfbaren Diplomen weist die Kandidatin oder der Kandidat die Qualifikation aus der Wallet vor, und der Arbeitgeber prüft Aussteller und Echtheit direkt. swiyu führt Diplome von Bildungsinstitutionen als Nachweistyp (swiyu – Ökosystem; swiyu – Behörden). Ein offizieller Pilot zur Prüfung durch Arbeitgeber ist nicht dokumentiert; die Einführung der E-ID wurde ohne neues Datum verschoben, und die Vertrauensinfrastruktur (swiyu) wird im 1. Halbjahr 2027 erwartet (Bundesrat / BJ, 30.06.2026).

### Outcome: what must be proven (optional)

- The candidate holds the named diploma or qualification
- The diploma was issued by a recognised institution
- The diploma has not been revoked
- The candidate is the person named on the diploma

**DE:**

- Die Kandidatin oder der Kandidat besitzt das genannte Diplom oder die genannte Qualifikation
- Das Diplom wurde von einer anerkannten Institution ausgestellt
- Das Diplom wurde nicht widerrufen
- Die Kandidatin oder der Kandidat ist die auf dem Diplom genannte Person

### Actors and roles

- Holder: Graduate / candidate
- Issuer: Universities, universities of applied sciences, VET bodies
- Verifier: Employer, recruiter, staffing firm
- Issuer: fedpol
- Governing authority: to be confirmed

### Process flow (optional)

1. Educational institution: Issues the diploma as a credential at graduation
2. Candidate: Applies and presents the diploma credential
3. Employer: Optionally requests identity to bind the diploma to the candidate
4. Employer: Verifies issuer in the trust registry and revocation status

### Design basis (optional)

DIDAS proposal (flow modelled in the DIDAS industry-function-graph as 'employment-onboarding-ch'). swiyu lists the credential type only.

### Credentials needed

Diploma / qualification credential (new, emerging) | Swiss e-ID (reused, emerging)

- **Reused**: [Swiss e-ID](https://github.com/DIDAS-swiss/use-case-repository/blob/main/credentials/swiss-e-id.md)
- **New**: `diploma-qualification-credential`

### Credentials described in this repository (optional)

swiss-e-id · Swiss e-ID

### Credentials already on I14Y (optional)

_No response_

### Emerging or other schemas (optional)

_No response_

### Ambition level(s)

- [X] AL1
- [X] AL2
- [ ] AL3

### Sector(s)

— ISIC-85 · Education, ISIC-N · Professional, scientific and technical activities

### Trust flows (optional)

_No response_

### Use case pattern in the Industry Function Graph (optional)

_No response_

### Other flow diagrams (optional)

_No response_

### Implementations, pilots and showcases (optional)

_No response_

### DIDAS Glossary terms (optional)

_No response_

### Related use cases (optional)

_No response_

### Upstream use cases (optional)

_No response_

### Downstream use cases (optional)

_No response_

### Lighthouse proposal (optional)

Selected as lighthouse (DIDAS decision)

### Why a lighthouse (optional)

DIDAS selection (backlog v2, 2026-11-09)

### Legal basis and governance (optional)

- **Legal basis**: BGEID (trust infrastructure open to any issuer, Art. 5); the education-law basis for awarding titles is not covered here
- **Trust frameworks and registries**: swiyu trust registry (BGEID Art. 3)
- **Verifier governance**: Employer requests only the qualification needed for the role
- **Sensitive attributes**: Grades and transcripts should not be requested unless needed

### Demand and value (optional)

- **Relying parties**: Employers, recruiters, staffing firms
- **Indicative scale**: no official figure
- **Value**: Faster onboarding; fewer forged diplomas; no calls to issuers

### Coordination needs and open questions (optional)

Universities and VET bodies to agree a common diploma schema; Decision whether public institutions are authoritative issuers (AL2); Employer associations to test verification in recruiting tools; Who maintains the list of recognised issuing institutions?; How are historic diplomas (issued before VCs) handled?; Relation to European diploma credentials for foreign degrees

**DE:**

Universitäten und Organe der Berufsbildung: ein gemeinsames Diplomschema vereinbaren; Entscheid, ob öffentliche Institutionen massgebliche Aussteller sind (AL2); Arbeitgeberverbände: die Prüfung in Recruiting-Tools testen; Wer führt die Liste der anerkannten ausstellenden Institutionen?; Wie werden ältere Diplome (vor VCs ausgestellt) behandelt?; Verhältnis zu europäischen Diplomnachweisen für ausländische Abschlüsse

### Proposed on behalf of (optional)

DIDAS

### Sources (optional)

industry-function-graph/data/flows.csv | 2026-09-14 (last commit) | https://github.com/DIDAS-swiss/industry-function-graph/blob/main/data/flows.csv | "An employer identifies a new hire, checks the qualifications the role requires and engages them." || didas.swiss – Blog: The E-ID and You – Youth Challenge | 2025-09-15 | https://www.didas.swiss/2025/09/15/4899/ | "Educational certificates such as diplomas" || swiyu – Ökosystem (official) | 2026-11-06 | https://swiyu.admin.ch/de/oekosystem | "Bildungsinstitutionen können Diplome ausstellen, Gesundheitseinrichtungen die Qualifikation einer Fachperson bestätigen" || swiyu – Behörden | accessed 2026-11-06 | https://swiyu.admin.ch/de/behoerden | "Ob Wohnsitzbestätigung oder Diplom: mit swiyu digital ausgestellt, ohne Gang zum Schalter." || BJ – Staatliche E-ID | accessed 2026-11-06 | https://www.bj.admin.ch/de/staatliche-e-id | "Unabhängig davon wird die Vertrauensinfrastruktur ihren Betrieb voraussichtlich im ersten Halbjahr 2027 aufnehmen können."

<!-- intake-body sha=a6a595f93ac6eeea -->