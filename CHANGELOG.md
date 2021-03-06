# Compliance-trestle changelog


<!--next-version-placeholder-->

## v0.6.2 (2021-01-17)
### Fix
* Corrected branch for mkdocs deploy. (#304) ([#305](https://github.com/IBM/compliance-trestle/issues/305)) ([`be3f13a`](https://github.com/IBM/compliance-trestle/commit/be3f13a89d44c3f773ad7e372e4116eb609c8f5d))

## v0.6.1 (2021-01-15)
### Fix
* Extra unit tests and cleanup to close more significant gaps ([#298](https://github.com/IBM/compliance-trestle/issues/298)) ([`2abcaad`](https://github.com/IBM/compliance-trestle/commit/2abcaadc1bc14419111e1778bbb1fab61d633d5e))
* Changed split to not write empty files after split. Implemented circular split-merge test ([#295](https://github.com/IBM/compliance-trestle/issues/295)) ([`1ebbeb2`](https://github.com/IBM/compliance-trestle/commit/1ebbeb20db1e25852dd58f7fa7a4ed909e995ef0))

### Documentation
* Initial setup of documentation website. ([#234](https://github.com/IBM/compliance-trestle/issues/234)) ([`a51081b`](https://github.com/IBM/compliance-trestle/commit/a51081bd93cb43b02135b72f00e16cf805eacba9))

## v0.6.0 (2021-01-07)
### Feature
* Force update of version ([`fc0357b`](https://github.com/IBM/compliance-trestle/commit/fc0357b297bb59d64ad28af23fe2404c31364010))
* Update to OSCAL 1.0.0rc1 and simplified models. ([#286](https://github.com/IBM/compliance-trestle/issues/286)) ([`992b317`](https://github.com/IBM/compliance-trestle/commit/992b31743f4d1c4ce11d5b8c1ee69995856d0056))
* Distributed load and trestle merge.(#272) ([`dceae85`](https://github.com/IBM/compliance-trestle/commit/dceae854c9e96ef2e66931efa9a0263b0470003e))
* Misc cleanups of code for typing, unsafe functions, and other issues. ([#274](https://github.com/IBM/compliance-trestle/issues/274)) ([`0652392`](https://github.com/IBM/compliance-trestle/commit/06523929944351ce90ba83a85d57f0b04b323660))

### Fix
* Correct semantic release behaviour ([`c25d5be`](https://github.com/IBM/compliance-trestle/commit/c25d5be7448ee956cd848a1476b5c9c70d72ab33))
* Correct semantic release behaviour. ([`caba993`](https://github.com/IBM/compliance-trestle/commit/caba993013fed5b70ced84fc58d34345e042cb6c))
* Refactor to use python and pytest internals for temporary paths and creating directories. ([`1d99ca2`](https://github.com/IBM/compliance-trestle/commit/1d99ca2ac96d76dfa777a0c514be582b382504de))
* Small typo fix. ([`2168bb2`](https://github.com/IBM/compliance-trestle/commit/2168bb2b4d8fa79fbf93687a41265379cba608b8))

## v0.4.0 (2020-11-24)
### Feature
* Validation of duplicates now uses object factory (#216) ([`cf00f8b`](https://github.com/IBM/compliance-trestle/commit/cf00f8bb0ea4f0a7c039e1399525ede8d8d0ace8))
* Completed trestle create implementation. ([`a73538f`](https://github.com/IBM/compliance-trestle/commit/a73538f57f5bf4142c27f65a0b05834650f00cd7))

### Fix
* Additional test for trestle add (#227) ([`479413f`](https://github.com/IBM/compliance-trestle/commit/479413f1e0d4f90ae3c89833f71ce3fbd7a3db69))
* For issue 229, another Any] still present in file (#230) ([`428b270`](https://github.com/IBM/compliance-trestle/commit/428b270861873d5983551cd5a3d980e6dc728700))
* Improvements in typing and return codes. (#224) ([`c382cb5`](https://github.com/IBM/compliance-trestle/commit/c382cb593bf8b2f2b69810650320fdea544ed803))
* Refactor to adopt FileContentType consistently (#223) ([`793ea7c`](https://github.com/IBM/compliance-trestle/commit/793ea7c353e4445b9a8911f3455656403cca0ca0))
* Handle anomalous GroupItems that were generating empty classes (#220) ([`8fae9dc`](https://github.com/IBM/compliance-trestle/commit/8fae9dcc74f6067fe01fae0caee167e09a8b5d0f))
* Versioning tag was malformed. (#199) ([`5c84d59`](https://github.com/IBM/compliance-trestle/commit/5c84d59c539773b18709968405cbe77ce27e6a99))

### Documentation
* Updated developer documentation with DCO and merge workflow. ([`041a7aa`](https://github.com/IBM/compliance-trestle/commit/041a7aa8b2183a261827e5ee9d7d562849329e12))

## v0.3.0 (2020-10-26)
### Feature
* Implements `add` functionality for trestle cmd. (#184) ([`eb42656`](https://github.com/IBM/compliance-trestle/commit/eb42656c60c0697ff2de806d4a57ee7b246363de))

### Fix
* Versioning tag was malformed. (#199) (#200) ([`957fe0b`](https://github.com/IBM/compliance-trestle/commit/957fe0bf08a358e5ab21eb93c60dba65cc486b24))
* Support contextual element path like groups.* during split (#192) ([`c9536b2`](https://github.com/IBM/compliance-trestle/commit/c9536b2bcc6404fa9dab8787fcbf97e8590e4402))
* Correct directory names of sub models during split (#189) ([`6b18237`](https://github.com/IBM/compliance-trestle/commit/6b18237fda53f91f936fc122fdbf74da8e4db65e))
* Reference to inexistent function (#182) ([`9605a51`](https://github.com/IBM/compliance-trestle/commit/9605a5101507e3d1c79218328424bdf115c435ca))
* Infer wrapper alias from input in Element constructor ([`82820fd`](https://github.com/IBM/compliance-trestle/commit/82820fde423c1982a5aa02965d897f04093187bb))
* Explicitly use contextual_model argument in path parsing util function ([`1ae3b12`](https://github.com/IBM/compliance-trestle/commit/1ae3b12e8a3786aa8f7516ca631070fb289be949))
* Do not create empty place holder file after splitting a dict or list ([`cb9fa8b`](https://github.com/IBM/compliance-trestle/commit/cb9fa8be810c915198b094785ce581b89a54ce99))
* Create main model alias directory during split ([`7656e42`](https://github.com/IBM/compliance-trestle/commit/7656e420acedf5b2e61c5fb27b448196a362c521))
* Incorrect file indexing during split #148 ([`ad7b2e6`](https://github.com/IBM/compliance-trestle/commit/ad7b2e63125fa3508254bd0c579e072f1e260fad))
* Utility method to write/read Oscal List and Dict object to/from file correctly (#161) ([`43c7bdf`](https://github.com/IBM/compliance-trestle/commit/43c7bdf5c30d88056999776e5df5fc9957842122))
* Updating fetch of NIST content. ([`85a852a`](https://github.com/IBM/compliance-trestle/commit/85a852a20fa33c1546a7f6cc64201809fb845fea))
* Merge pull request #158 from IBM/fix/issue_149b ([`75b11ca`](https://github.com/IBM/compliance-trestle/commit/75b11ca91e0a23778511ac285b4655fbe12bd9f8))

### Documentation
* Initial caching structure documentation (#143) ([`d1a73f3`](https://github.com/IBM/compliance-trestle/commit/d1a73f314d42201fb7b9cbe79775a41b465ef6c7))
* Updated readme to document current level of support for file formats (#179) ([`1df2110`](https://github.com/IBM/compliance-trestle/commit/1df2110eb9fb89816871ce70ceb72d5f3be18049))
* Change of trestle model directory structure (#169) ([`ed2ab36`](https://github.com/IBM/compliance-trestle/commit/ed2ab36c64ddb45297974bb851819322477c0fd2))