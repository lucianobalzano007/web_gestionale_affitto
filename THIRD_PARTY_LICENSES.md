# Third-Party Licenses

This document lists third-party software identified as being used by, or distributed with, **web_gestionale_affitto**.

The source code of `web_gestionale_affitto` is licensed separately under the **MIT License**. That license does not replace or modify the licenses of third-party components listed below.

> **Important:** This inventory is based on the dependencies declared by the project and on the container license scan supplied for the `python:3.12.16-alpine`-based image. The authoritative inventory for a specific released container image should be its generated SPDX SBOM. Package versions and transitive dependencies may change when rebuilding an image if dependencies are not pinned.

## Direct Python dependencies

The project declares these direct Python dependencies in `requirements.txt`:

| Component | License | Notes |
| --- | --- | --- |
| Flask | BSD-3-Clause | Web framework |
| pandas | BSD-3-Clause | Data processing |
| PyMongo | Apache-2.0 | MongoDB Python driver |
| ReportLab | BSD-style | PDF generation toolkit |

All copyright notices and license terms belonging to these projects remain the property of their respective copyright holders.

## Container and operating-system components

The application container is based on `python:3.12.16-alpine`. The following components and licenses were reported by the supplied container scan.

| Component | Observed version | License(s) |
| --- | --- | --- |
| alpine-baselayout-data | 3.7.2-r1 | GPL-2.0-only |
| alpine-baselayout | 3.7.2-r1 | GPL-2.0-only |
| apk-tools | 3.0.8-r0 | GPL-2.0-only |
| busybox-binsh | 1.37.0-r31 | GPL-2.0-only |
| busybox | 1.37.0-r31 | GPL-2.0-only |
| ca-certificates-bundle | 20261020-r0 | MPL-2.0 |
| ca-certificates | 20261020-r0 | MPL-2.0 |
| e2fsprogs | 1.47.4-r0 | GPL-2.0-or-later |
| gdbm | 1.26-r0 | GPL-3.0-or-later |
| gettext | 1.0-r0 | LGPL-2.1-or-later |
| keyutils-libs | 1.6.3-r4 | GPL-2.0-or-later |
| keyutils | 1.6.3-r4 | GPL-2.0-or-later |
| libapk | 3.0.8-r0 | GPL-2.0-only |
| libcom_err | 1.47.4-r0 | GPL-2.0-or-later |
| libintl | 1.0-r0 | LGPL-2.1-or-later |
| musl-utils | 1.2.6-r3 | GPL-2.0-or-later (as reported by scanner) |
| musl | 1.2.6-r3 | GPL-2.0-or-later (as reported by scanner; verify against package/file-level metadata) |
| pax-utils | 1.3.9-r1 | GPL-2.0-only |
| readline | 8.3.3-r1 | GPL-3.0-or-later |
| scanelf | 1.3.9-r1 | GPL-2.0-only |
| ssl_client | 1.37.0-r31 | GPL-2.0-only |
| xz-libs | 5.8.4-r0 | GPL-2.0-or-later; LGPL-2.1-or-later |
| xz | 5.8.4-r0 | GPL-2.0-or-later; LGPL-2.1-or-later |
| fribidi | 1.0.17 | LGPL-2.1-or-later |
| libimagequant | 4.4.1 | GPL-3.0-or-later |

### Note about scanner results

Some operating-system packages may contain files under more than one license, or scanners may report package-level licensing differently from upstream project-level licensing. In particular, the `musl` result above should be verified against the SPDX SBOM and the license metadata shipped in the exact container image before using this document as a legal attribution record.

## MongoDB

The application uses PyMongo to communicate with MongoDB. The MongoDB server is deployed as a separate container in `compose.yml` and is not relicensed by this project's MIT License. Users and redistributors should review the license applicable to the exact MongoDB image and version they deploy.

## License texts and notices

Redistributors of a container image should retain all copyright notices, license notices, disclaimers, and corresponding source offers or other materials required by each applicable third-party license.

This file is an inventory and attribution aid. It is **not** a substitute for the full license texts. For release artifacts, preserve the license files shipped by the third-party packages and attach an SPDX SBOM to the published container image.

## Reproducible license inventory

For each container release, generate an SBOM and provenance during the build, for example:

```bash
docker buildx build \
  --sbom=true \
  --provenance=mode=max \
  -t lucianobalzano/web_gestionale_affitto:latest \
  --push \
  .
```

The SPDX SBOM generated for the released image should be treated as the definitive package inventory for that release, while this document provides a human-readable overview.

## Project license

`web_gestionale_affitto` is licensed under the MIT License. See the repository's `LICENSE` file for the complete terms applicable to the project's own source code.
