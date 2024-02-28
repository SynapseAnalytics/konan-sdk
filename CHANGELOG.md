# CHANGELOG



## v1.5.0 (2024-02-28)

### Chore

* chore(actions): bump relekang/python-semantic-release to v8.3.0

Signed-off-by: Mohamed Tawfik &lt;mtawfik@synapse-analytics.io&gt; ([`7f0af12`](https://github.com/SynapseAnalytics/konan-sdk/commit/7f0af120738116aa0284bb887bd9b22b8aacff31))

### Feature

* feat(predictions): retrieve outputs correctly

Signed-off-by: Mohamed Tawfik &lt;mtawfik@synapse-analytics.io&gt; ([`66be7ed`](https://github.com/SynapseAnalytics/konan-sdk/commit/66be7ed91b0d63e24a18e51ae01e66f13c347866))


## v1.4.2 (2022-12-18)

### Fix

* fix(predictions): fix token expiry with too many

Signed-off-by: Mohamed Tawfik &lt;mtawfik@synapse-analytics.io&gt; ([`33d4f85`](https://github.com/SynapseAnalytics/konan-sdk/commit/33d4f85ff00ed3cc177c6c135e511b5865a536cd))

* fix(predictions): remove duplicate query params

Signed-off-by: Mohamed Tawfik &lt;mtawfik@synapse-analytics.io&gt; ([`1b562ac`](https://github.com/SynapseAnalytics/konan-sdk/commit/1b562ace11adee0a01a99110b06d7d4e0808759f))

### Refactor

* refactor(endpoints): split REST endpoints objects

Signed-off-by: Mohamed Tawfik &lt;mtawfik@synapse-analytics.io&gt; ([`7bec780`](https://github.com/SynapseAnalytics/konan-sdk/commit/7bec78060d9d62aa91de260e510e80958314cb5d))


## v1.4.1 (2022-09-27)

### Chore

* chore(actions): update semantic-release ([`ffa37c5`](https://github.com/SynapseAnalytics/konan-sdk/commit/ffa37c5fefebb4d8b0efceb283bbf9d0c3363fb0))

### Fix

* fix(project): fix minor bug ([`d3af031`](https://github.com/SynapseAnalytics/konan-sdk/commit/d3af031bf3396cad281e0ba2660024a583da581e))


## v1.4.0 (2022-09-25)

### Chore

* chore(endpoints): add pagination mixin ([`868a011`](https://github.com/SynapseAnalytics/konan-sdk/commit/868a0112521bcedc982f09eee1cc9f221bb43921))

### Documentation

* docs(integration): clarify some comments ([`e56b1cc`](https://github.com/SynapseAnalytics/konan-sdk/commit/e56b1cc0174aade5976a568cccd3e16b7df7db2e))

### Feature

* feat(project): create project alongisde live model ([`ca6c8ba`](https://github.com/SynapseAnalytics/konan-sdk/commit/ca6c8babe6596f4fca4edb77e7a081f15cbeae89))

* feat(auth): add API Key authentication ([`b05d8d9`](https://github.com/SynapseAnalytics/konan-sdk/commit/b05d8d94df982f0c058bf602d063f4417a2ba18b))

* feat(sdk): add listing predictions via pagination ([`3248d54`](https://github.com/SynapseAnalytics/konan-sdk/commit/3248d54e4a62ca1927ba0e99fec72ed5d6a8ba64))


## v1.3.0 (2022-06-02)

### Chore

* chore(sdk): refactor switch_model_state ([`71efc09`](https://github.com/SynapseAnalytics/konan-sdk/commit/71efc099fc98849f358bf331b8c22a0ef5f211d0))

* chore(endpoints): remove extra debugging messages ([`4b71ca7`](https://github.com/SynapseAnalytics/konan-sdk/commit/4b71ca7118ff1d237f4379eb757190a98d75c6b1))

* chore: add python-dotenv dev dependency ([`7f3e2be`](https://github.com/SynapseAnalytics/konan-sdk/commit/7f3e2be7815b9f248b5af73664e24fc7fdf1fe0f))

* chore(license): update Copyright owner ([`12607db`](https://github.com/SynapseAnalytics/konan-sdk/commit/12607db45b55bd15f816cc80684a1a7d80428852))

* chore(git): remove version from develop branches ([`a2f1c3e`](https://github.com/SynapseAnalytics/konan-sdk/commit/a2f1c3effc77494e474549b71ba1eb877b65ae17))

* chore(git): refactor merge tree
Exclude version commits from develop branch and any subsquent branches ([`809ab0c`](https://github.com/SynapseAnalytics/konan-sdk/commit/809ab0c74c292366ecd608fa79e16b02a1765a5d))

### Feature

* feat(endpoints): add model switch endpoints ([`9cc2276`](https://github.com/SynapseAnalytics/konan-sdk/commit/9cc2276325c4298bf0bba635eb3f7869ae48fb8e))

* feat(endpoints): add get models endpoint ([`21ca037`](https://github.com/SynapseAnalytics/konan-sdk/commit/21ca0377d349191bf60bf8f95bf1ea709be18e5c))

* feat(endpoints): add delete model endpoint ([`e588451`](https://github.com/SynapseAnalytics/konan-sdk/commit/e588451ae10ef57a3549d7af6134a531004cefcd))

* feat(endpoints): add create model endpoint ([`b297b12`](https://github.com/SynapseAnalytics/konan-sdk/commit/b297b12b3276feaa1b0c660cbf1feaeb90d069c1))

* feat(deployment): add model to create deployments ([`db7c294`](https://github.com/SynapseAnalytics/konan-sdk/commit/db7c29431e9082c3e18947ea84395392bde623be))

### Fix

* fix(types): add total ordering for KonanModel ([`6b6ff62`](https://github.com/SynapseAnalytics/konan-sdk/commit/6b6ff62f669e9c0b379dd39adacda583904f3f5a))

### Style

* style(sdk): add a space before an inline comment ([`2488a17`](https://github.com/SynapseAnalytics/konan-sdk/commit/2488a175402352d54c4262101d7e5a38f4b6a124))


## v1.2.6 (2022-03-24)

### Chore

* chore(imports): remove extra import ([`c15409c`](https://github.com/SynapseAnalytics/konan-sdk/commit/c15409ccb8a060bad204bfa49541dd6c3d81001f))

* chore(releases): all manual release ([`a728401`](https://github.com/SynapseAnalytics/konan-sdk/commit/a7284018d177828d20c84a84ef5592a02b573319))

### Fix

* fix(konan-service): fix healthz response ([`48ffe50`](https://github.com/SynapseAnalytics/konan-sdk/commit/48ffe50d361d8712245ac9c2c8610d04c08cd8ef))

### Unknown

* Merge pull request #24 from SynapseAnalytics/develop

Allow manual release ([`940e78a`](https://github.com/SynapseAnalytics/konan-sdk/commit/940e78ac45806d6bb140a0bcc70abfc365dc55e5))

* Fix `healthz` response (#23)

* fix(Evaluate): fix returning empty metrics

* chore(docs): add docs with sphinx and ReadTheDocs (#18)

* fix(konan-service): fix healthz response

Co-authored-by: Mohamed Tawfik &lt;mtawfik@syanpse-analytics.io&gt; ([`6d69349`](https://github.com/SynapseAnalytics/konan-sdk/commit/6d69349c4cd13bdc75e7ba222ac865fda7e913bf))

* Merge branch &#39;main&#39; into develop ([`a7ff65c`](https://github.com/SynapseAnalytics/konan-sdk/commit/a7ff65c28dcc778189cbfe120885eacf19a95f56))


## v1.2.5 (2022-02-14)

### Chore

* chore(docs): add docs with sphinx and ReadTheDocs (#18) ([`4ec16c0`](https://github.com/SynapseAnalytics/konan-sdk/commit/4ec16c04531d58768d8ca8ed76dbb79995e5b937))

* chore(docs): add docs with sphinx and ReadTheDocs (#18) ([`0ead10f`](https://github.com/SynapseAnalytics/konan-sdk/commit/0ead10f0c0454351fb95411bbd17eead06178cee))

### Fix

* fix(docs): Add more descriptive doc strings ([`344fc59`](https://github.com/SynapseAnalytics/konan-sdk/commit/344fc59f3401b76fbbd419ff6b98fad7a04520af))

### Unknown

* Merge branch &#39;main&#39; into develop ([`d29c459`](https://github.com/SynapseAnalytics/konan-sdk/commit/d29c4592de222ad27c02659532fd3c1b69956825))


## v1.2.4 (2022-01-26)

### Fix

* fix(Evaluate): fix returning empty metrics ([`39c6f15`](https://github.com/SynapseAnalytics/konan-sdk/commit/39c6f15effc9037a30fd2a4bd1fc060d3280d573))

* fix(Evaluate): fix returning empty metrics ([`48d0c1a`](https://github.com/SynapseAnalytics/konan-sdk/commit/48d0c1a1dd4f28381bf67c0847cfddb13b733516))


## v1.2.3 (2022-01-26)

### Chore

* chore(poetry): add pyyaml as dev dependency ([`0665ed1`](https://github.com/SynapseAnalytics/konan-sdk/commit/0665ed158781c50b3d16250fd363debc35213da1))

### Fix

* fix(Endpoints): fix handling endpoint without JSON response ([`d69a13f`](https://github.com/SynapseAnalytics/konan-sdk/commit/d69a13f1dbbbdfa5b02600c05299e16d01db53e3))

* fix(Metrics): fix creating a KonanCustomMetric ([`83b0601`](https://github.com/SynapseAnalytics/konan-sdk/commit/83b06017d23b44cc7d90e92c96376edf6596ad7c))

### Unknown

* Merge pull request #15 from SynapseAnalytics/develop

Hotfixes for endpoints ([`f9ad647`](https://github.com/SynapseAnalytics/konan-sdk/commit/f9ad647a7d2ae286bbe079f339329320d5cd3c23))


## v1.2.2 (2022-01-19)

### Fix

* fix(endpoints): fix endpoint paths with trailing slash ([`7d05b42`](https://github.com/SynapseAnalytics/konan-sdk/commit/7d05b42fa9edf7685061d57680f2786807656340))

* fix(endpoints): fix endpoint paths ([`5be21b7`](https://github.com/SynapseAnalytics/konan-sdk/commit/5be21b751644eb5b3f22c6a4af969fa09eddc7d1))

* fix(endpoint): fix json and slash in URLs ([`2b43c72`](https://github.com/SynapseAnalytics/konan-sdk/commit/2b43c72fceae57fdcd5b24da644726b29541e446))

* fix(endpoints): Fix importing NoneType ([`d17786c`](https://github.com/SynapseAnalytics/konan-sdk/commit/d17786c5c447559f6e798c3276f9b1aa4f67f337))

### Unknown

* 1.2.1 [skip-ci] ([`cd4ca48`](https://github.com/SynapseAnalytics/konan-sdk/commit/cd4ca48eafb2f27871dc8915defe14ca99d909e1))


## v1.2.0 (2022-01-17)

### Feature

* feat(endpoints): add delete deployment endpoint (#13) ([`63781b1`](https://github.com/SynapseAnalytics/konan-sdk/commit/63781b19c9e7c96a24c62e347c4ab9c82686a1e8))

### Refactor

* refactor(endpoints): refactor operations on endpoints (#12) ([`6c6dbcc`](https://github.com/SynapseAnalytics/konan-sdk/commit/6c6dbcc1347d7041f0b1d1e654c859a3a53b98b1))

### Unknown

* Merge pull request #14 from SynapseAnalytics/develop

Release new `konan-sdk` version ([`319b59e`](https://github.com/SynapseAnalytics/konan-sdk/commit/319b59e86d8252a3b966484dc0bd2f57eee42137))

* Merge pull request #9 from SynapseAnalytics/KONAN-891-create-deployment

Konan 891 create deployment ([`834967a`](https://github.com/SynapseAnalytics/konan-sdk/commit/834967ad1bcb61cf9ecb61c13c7b1a119fc85c6f))


## v1.1.0 (2022-01-12)

### Chore

* chore(ci): use python-semantic-release action with version ([`9fef03a`](https://github.com/SynapseAnalytics/konan-sdk/commit/9fef03a382f39fdaea0dde2871f397199dbd01da))

* chore(workflow): use python-semantic-release action ([`c434b96`](https://github.com/SynapseAnalytics/konan-sdk/commit/c434b96cc56f78643cd418bde76d0c92702dc4c8))

* chore(ci): skip releases for now ([`37fd141`](https://github.com/SynapseAnalytics/konan-sdk/commit/37fd141b0f2cf09df4021a2638a9ebebf9b2e7b5))

* chore(workflow): fix poetry and pypi settings ([`c63fe36`](https://github.com/SynapseAnalytics/konan-sdk/commit/c63fe36cad6fe7fb00d579e0dcf9b7c1f9190ac2))

* chore(actions): remove redundant check in release ([`7d1e3da`](https://github.com/SynapseAnalytics/konan-sdk/commit/7d1e3daafb3fd3cb669e25b5638a9d06a44b9efd))

* chore(pypi): temporarily don&#39;t release to PyPI ([`dd251bd`](https://github.com/SynapseAnalytics/konan-sdk/commit/dd251bd3d9be5b02fd6820e75d8704740b1cb65a))

* chore(workflows): fix linting command ([`7ae293f`](https://github.com/SynapseAnalytics/konan-sdk/commit/7ae293f126414179e8a5aaace4bc32cd16c8b959))

* chore(workflows): run quality worfklow on all branches ([`37f5ddd`](https://github.com/SynapseAnalytics/konan-sdk/commit/37f5ddd82fb6538adc3e710b263e3327e58711ff))

* chore(sdk): fix linting issues ([`ded402d`](https://github.com/SynapseAnalytics/konan-sdk/commit/ded402d313fad980ad83e5d74e6716a3efdfed6d))

* chore(linting): adjust flake8 exclude paths ([`1a93d71`](https://github.com/SynapseAnalytics/konan-sdk/commit/1a93d715e8cc761cbd255a1a5555b8159a356241))

* chore(ci): add semantic release ([`52a4a13`](https://github.com/SynapseAnalytics/konan-sdk/commit/52a4a136926c79bafe00bed2bb16d346819fd0cb))

* chore: bump version to 1.0.0 ([`a2e8204`](https://github.com/SynapseAnalytics/konan-sdk/commit/a2e8204cbc127a87c02277b9f2bf33059fc11fac))

* chore(gitignore): add vscode to gitignore ([`e935b97`](https://github.com/SynapseAnalytics/konan-sdk/commit/e935b97bda761f000318cff05fecc9fdd8f17ba3))

* chore: change python version to ^3.7 ([`71c75db`](https://github.com/SynapseAnalytics/konan-sdk/commit/71c75dbbc8b27ba9c805fc41f88e498564b6d016))

* chore: update poetry.lock file ([`31c6e0c`](https://github.com/SynapseAnalytics/konan-sdk/commit/31c6e0c2481682648ae1351c4053f0d9ee170352))

* chore: update python version to include 3.7 ([`0808c69`](https://github.com/SynapseAnalytics/konan-sdk/commit/0808c69fc86f0b6a37073f428c8d0418190cc428))

### Documentation

* docs: update links in pypoetry.toml ([`da9fb92`](https://github.com/SynapseAnalytics/konan-sdk/commit/da9fb925bd47de94353b4230aabb72628528d46c))

### Feature

* feat(endpoints): add create deployment endpoint ([`0089316`](https://github.com/SynapseAnalytics/konan-sdk/commit/00893162dc055fe817427789728799673b2d3539))

* feat(endpoints): add evaluate endpoint ([`20aa0ef`](https://github.com/SynapseAnalytics/konan-sdk/commit/20aa0efd579d6493dead30949cc0723c7f178cd5))

* feat(endpoints): add create feedback endpoint ([`1a02bc4`](https://github.com/SynapseAnalytics/konan-sdk/commit/1a02bc411da19911f7433a7183d9991fc44211a1))

* feat(mlservice): add multi_label_confusion_matrix to pre-defined metrics ([`0896106`](https://github.com/SynapseAnalytics/konan-sdk/commit/0896106e0961ebe47177039711d921e98e2c67d6))

* feat(ml-service): add base classes for an ml-service ([`54ddc91`](https://github.com/SynapseAnalytics/konan-sdk/commit/54ddc919c3d03278ed91994d21fad501a602f50c))

* feat(ml-service): add evaluate endpoint ([`ca3437f`](https://github.com/SynapseAnalytics/konan-sdk/commit/ca3437fc2cd5c67e4eb1c85d872b1b5d51282448))

* feat(ml-service): add base classes for an ml-service ([`efbf75e`](https://github.com/SynapseAnalytics/konan-sdk/commit/efbf75e09edb7be8e203875b197001f9987a733f))

* feat: adjust endpoints to new api version ([`f0f4307`](https://github.com/SynapseAnalytics/konan-sdk/commit/f0f4307191378492749240f4f01a0c6b67696580))

* feat: made predict function take either a dict or a string ([`9e5582a`](https://github.com/SynapseAnalytics/konan-sdk/commit/9e5582a010bb8e17265481de3c9c7e22fbf1e2a3))

### Fix

* fix(base-endpoints): treat endpoint_path as property not func ([`f1e192c`](https://github.com/SynapseAnalytics/konan-sdk/commit/f1e192cdafb25148f27112cff054b1c12314f775))

* fix(mlservice): override ServiceFeedback.prediction ([`46d3750`](https://github.com/SynapseAnalytics/konan-sdk/commit/46d3750d61415ba85266092e61ffc3494edc30c1))

* fix(evaluate): Fix typing and inheritance of Types ([`cb301bb`](https://github.com/SynapseAnalytics/konan-sdk/commit/cb301bb7fda102ed1e78f1013ba27f28cca2adba))

* fix: fix konan-sdk not working with python 3.7 ([`a68faed`](https://github.com/SynapseAnalytics/konan-sdk/commit/a68faed1983d503423444884443dd98db10f2d3b))

* fix: fix access / refresh token not being correctly refreshed ([`ccc350d`](https://github.com/SynapseAnalytics/konan-sdk/commit/ccc350d469ab16c97f55219ac3d7b0ff939e9ee5))

### Unknown

* Merge pull request #11 from SynapseAnalytics/develop

Release new SDK version ([`9d65adb`](https://github.com/SynapseAnalytics/konan-sdk/commit/9d65adb8b55e381b9a68bcab480bb0426fdcd321))

* Merge branch &#39;main&#39; into develop ([`78c3ab4`](https://github.com/SynapseAnalytics/konan-sdk/commit/78c3ab453ec737e8a71f9b9230f1e05fc39d615f))

* Merge pull request #10 from SynapseAnalytics/develop

Release new SDK version Tag ([`e9b4394`](https://github.com/SynapseAnalytics/konan-sdk/commit/e9b439410517fd6e43a1a7decbce80ce30bedf03))

* hotfix(github-ci): move workflow files to correct path ([`36e9033`](https://github.com/SynapseAnalytics/konan-sdk/commit/36e90339a2eed9d597bb07ad77c3d3c804552531))

* Merge branch &#39;main&#39; into develop ([`356f467`](https://github.com/SynapseAnalytics/konan-sdk/commit/356f4673d87e29e443307f23435d7835d60d02c5))

* Konan 792 sdk refactoring (#4)

refactor: refactor konan sdk endpoints ([`dc64fa4`](https://github.com/SynapseAnalytics/konan-sdk/commit/dc64fa4b03acfca3b8d6796cadae3396b31c605a))

* Merge pull request #3 from SynapseAnalytics/KONAN-811

feat(ml-service): add evaluate endpoint ([`3e7e37b`](https://github.com/SynapseAnalytics/konan-sdk/commit/3e7e37b9d0eb0f388ce65238187eb1d33963a0e3))

* Merge branch &#39;develop&#39; into KONAN-811 ([`188daba`](https://github.com/SynapseAnalytics/konan-sdk/commit/188dabac60951c042c99c69054e87feeadab0fa5))

* Merge pull request #2 from SynapseAnalytics/KONAN-763

feat(mlservice): add base classes for an ml-service ([`f3acf38`](https://github.com/SynapseAnalytics/konan-sdk/commit/f3acf38dd0a69604394e7f4aab8150e3876f5a5f))

* Merge pull request #1 from SynapseAnalytics/chore/semantic-release

Chore/semantic release ([`a6968ac`](https://github.com/SynapseAnalytics/konan-sdk/commit/a6968ac38cc6a676a668961585ca8b1356be2d4b))

* Initial commit ([`fb2ada0`](https://github.com/SynapseAnalytics/konan-sdk/commit/fb2ada0401020f859601b24a40353304e109d228))
