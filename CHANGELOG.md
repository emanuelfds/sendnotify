# Changelog

## [1.2.5](https://github.com/emanuelfds/sendnotify/compare/v1.2.4...v1.2.5) (2026-07-16)


### Bug Fixes

* remove ZAP active scan, fix Trivy image ref and add SARIF fallback ([746e21e](https://github.com/emanuelfds/sendnotify/commit/746e21e07a4ece181afccc08c49d024a6d8dc4c8))

## [1.2.4](https://github.com/emanuelfds/sendnotify/compare/v1.2.3...v1.2.4) (2026-07-16)


### Bug Fixes

* correct ZAP action repo name and add Bandit SARIF fallback ([fed4b63](https://github.com/emanuelfds/sendnotify/commit/fed4b63b11e38f24461cfb43c55137b1508fc543))

## [1.2.3](https://github.com/emanuelfds/sendnotify/compare/v1.2.2...v1.2.3) (2026-07-16)


### Bug Fixes

* adiciona startupProbe, PDB, cosign, SBOM e migra testes para pytest ([7f5311f](https://github.com/emanuelfds/sendnotify/commit/7f5311f7b34e02caa95a7ceb9157b5734317b345))
* resolve duplicate 'if' condition in Bandit SARIF upload step ([70a3c8f](https://github.com/emanuelfds/sendnotify/commit/70a3c8fd68e152480ed65b3305659c2bab15de5c))

## [1.2.2](https://github.com/emanuelfds/sendnotify/compare/v1.2.1...v1.2.2) (2026-07-14)


### Bug Fixes

* adiciona environment protection no deploy-argocd ([9776b79](https://github.com/emanuelfds/sendnotify/commit/9776b79dfcd459306ab0f1d6afb51f415c6e5e4b))

## [1.2.1](https://github.com/emanuelfds/sendnotify/compare/v1.2.0...v1.2.1) (2026-07-14)


### Bug Fixes

* adiciona token PAT no checkout do deploy-argocd ([90f828f](https://github.com/emanuelfds/sendnotify/commit/90f828fbaa4eb971ffd4e40b1a3e1d102763d884))
* corrige deploy-argocd e adiciona notificações Slack diferenciadas ([de2958e](https://github.com/emanuelfds/sendnotify/commit/de2958ea7f59c3e84e65139b287636fd8ce6ab98))

## [1.2.0](https://github.com/emanuelfds/sendnotify/compare/v1.1.3...v1.2.0) (2026-07-14)


### Features

* adiciona notificação Slack para builds de sucesso ([6b46d5e](https://github.com/emanuelfds/sendnotify/commit/6b46d5e729a5c04cf29eeba0e700caf0918fe783))


### Bug Fixes

* adiciona validação de variáveis de ambiente no startup ([c233195](https://github.com/emanuelfds/sendnotify/commit/c233195b0684a7cb69e4328b46c0c54edf04b5bb))

## [1.1.3](https://github.com/emanuelfds/sendnotify/compare/v1.1.2...v1.1.3) (2026-07-13)


### Bug Fixes

* remove o warning do node20 depreciado ([b09d27d](https://github.com/emanuelfds/sendnotify/commit/b09d27d9c21fd53db69fea844609c435010e983b))

## [1.1.2](https://github.com/emanuelfds/sendnotify/compare/v1.1.1...v1.1.2) (2026-07-13)


### Bug Fixes

* atualiza googleapis/release-please-action ([95551ef](https://github.com/emanuelfds/sendnotify/commit/95551eff8e86d9ebc3f8d93e15377febe47e51b2))

## [1.1.1](https://github.com/emanuelfds/sendnotify/compare/v1.1.0...v1.1.1) (2026-07-13)


### Bug Fixes

* adiciona type annotations e ajusta mypy no CI ([7641489](https://github.com/emanuelfds/sendnotify/commit/76414891359ce3100250903cb446fb2a2bce5d79))

## [1.1.0](https://github.com/emanuelfds/sendnotify/compare/v1.0.0...v1.1.0) (2026-07-13)


### Features

* add aplication ([5832001](https://github.com/emanuelfds/sendnotify/commit/583200146a2b04615fdc1d626e10bf78efb3bd7b))
* ajustando o logo ([4c23508](https://github.com/emanuelfds/sendnotify/commit/4c235088bd8e793e283e8c1898aa66f1fb258b51))
* ajustando o logo ([d6433da](https://github.com/emanuelfds/sendnotify/commit/d6433da4319501c73d07fb7b0aa073c7e610d0e6))
* ajustando o logo ([6bb844d](https://github.com/emanuelfds/sendnotify/commit/6bb844dee2f7f05518fcb67c6cff81326ae50a81))
* suporte multi-cloud (OCI, AWS, Azure) + refatoração completa do build ([36421c6](https://github.com/emanuelfds/sendnotify/commit/36421c60768bb8457a8e12264c3e45f9566aec5f))


### Bug Fixes

* auth via Secret, node affinity e documentação ([9fde7d1](https://github.com/emanuelfds/sendnotify/commit/9fde7d1dc5d672e0208c9209a2bc022335c02fcd))
* bump python to 3.12-alpine and copy providers into docker image ([705ed47](https://github.com/emanuelfds/sendnotify/commit/705ed47c3c8fbba6f64119a9c2cffc04b42a224b))
* correct namespace from 'monitoring' to 'obsevability' in all manifests ([d5113ab](https://github.com/emanuelfds/sendnotify/commit/d5113ab5f3334703d68705c7f070a512c0216c83))
* correct namespace to observability and harden deployment security ([1ef8e4c](https://github.com/emanuelfds/sendnotify/commit/1ef8e4c61f2dd12be5f310cfa31650498ae30fed))
* replace sensitive/OCIR config with generic values for dev/hml ([a3e4c26](https://github.com/emanuelfds/sendnotify/commit/a3e4c2602795fa0d6db426844378038c8235ae25))
* replace sensitive/OCIR config with generic values for dev/hml ([c786eab](https://github.com/emanuelfds/sendnotify/commit/c786eabe2fbc2cd63c1ac47d47366b07fe29c283))
