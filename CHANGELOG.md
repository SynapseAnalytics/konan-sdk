# Changelog

<!--next-version-placeholder-->

## v1.3.0 (2022-06-02)
### Feature
* **endpoints:** Add model switch endpoints ([`9cc2276`](https://github.com/SynapseAnalytics/konan-sdk/commit/9cc2276325c4298bf0bba635eb3f7869ae48fb8e))
* **endpoints:** Add get models endpoint ([`21ca037`](https://github.com/SynapseAnalytics/konan-sdk/commit/21ca0377d349191bf60bf8f95bf1ea709be18e5c))
* **endpoints:** Add delete model endpoint ([`e588451`](https://github.com/SynapseAnalytics/konan-sdk/commit/e588451ae10ef57a3549d7af6134a531004cefcd))
* **endpoints:** Add create model endpoint ([`b297b12`](https://github.com/SynapseAnalytics/konan-sdk/commit/b297b12b3276feaa1b0c660cbf1feaeb90d069c1))
* **deployment:** Add model to create deployments ([`db7c294`](https://github.com/SynapseAnalytics/konan-sdk/commit/db7c29431e9082c3e18947ea84395392bde623be))

### Fix
* **types:** Add total ordering for KonanModel ([`6b6ff62`](https://github.com/SynapseAnalytics/konan-sdk/commit/6b6ff62f669e9c0b379dd39adacda583904f3f5a))

## v1.2.6 (2022-03-24)
### Fix
* **konan-service:** Fix healthz response ([`48ffe50`](https://github.com/SynapseAnalytics/konan-sdk/commit/48ffe50d361d8712245ac9c2c8610d04c08cd8ef))
* **Evaluate:** Fix returning empty metrics ([`48d0c1a`](https://github.com/SynapseAnalytics/konan-sdk/commit/48d0c1a1dd4f28381bf67c0847cfddb13b733516))

## v1.2.5 (2022-02-14)
### Fix
* **docs:** Add more descriptive doc strings ([`344fc59`](https://github.com/SynapseAnalytics/konan-sdk/commit/344fc59f3401b76fbbd419ff6b98fad7a04520af))

## v1.2.4 (2022-01-26)
### Fix
* **Evaluate:** Fix returning empty metrics ([`39c6f15`](https://github.com/SynapseAnalytics/konan-sdk/commit/39c6f15effc9037a30fd2a4bd1fc060d3280d573))

## v1.2.3 (2022-01-26)
### Fix
* **Endpoints:** Fix handling endpoint without JSON response ([`d69a13f`](https://github.com/SynapseAnalytics/konan-sdk/commit/d69a13f1dbbbdfa5b02600c05299e16d01db53e3))
* **Metrics:** Fix creating a KonanCustomMetric ([`83b0601`](https://github.com/SynapseAnalytics/konan-sdk/commit/83b06017d23b44cc7d90e92c96376edf6596ad7c))

## v1.2.2 (2022-01-19)
### Fix
* **endpoints:** Fix endpoint paths with trailing slash ([`7d05b42`](https://github.com/SynapseAnalytics/konan-sdk/commit/7d05b42fa9edf7685061d57680f2786807656340))

## v1.2.1 (2022-01-19)

### Fix
* **endpoints:** Fix importing NoneType ([`d17786c`](https://github.com/SynapseAnalytics/konan-sdk/commit/d17786c5c447559f6e798c3276f9b1aa4f67f337))

## v1.2.0 (2022-01-17)
### Feature
* **endpoints:** Add delete deployment endpoint ([#13](https://github.com/SynapseAnalytics/konan-sdk/issues/13)) ([`63781b1`](https://github.com/SynapseAnalytics/konan-sdk/commit/63781b19c9e7c96a24c62e347c4ab9c82686a1e8))
* **endpoints:** Add create deployment endpoint ([`0089316`](https://github.com/SynapseAnalytics/konan-sdk/commit/00893162dc055fe817427789728799673b2d3539))

### Fix
* **base-endpoints:** Treat endpoint_path as property not func ([`f1e192c`](https://github.com/SynapseAnalytics/konan-sdk/commit/f1e192cdafb25148f27112cff054b1c12314f775))

## v1.1.0 (2022-01-12)
### Feature
* **endpoints:** Add evaluate endpoint ([`20aa0ef`](https://github.com/SynapseAnalytics/konan-sdk/commit/20aa0efd579d6493dead30949cc0723c7f178cd5))
* **endpoints:** Add create feedback endpoint ([`1a02bc4`](https://github.com/SynapseAnalytics/konan-sdk/commit/1a02bc411da19911f7433a7183d9991fc44211a1))
* **mlservice:** Add multi_label_confusion_matrix to pre-defined metrics ([`0896106`](https://github.com/SynapseAnalytics/konan-sdk/commit/0896106e0961ebe47177039711d921e98e2c67d6))
* **ml-service:** Add base classes for an ml-service ([`54ddc91`](https://github.com/SynapseAnalytics/konan-sdk/commit/54ddc919c3d03278ed91994d21fad501a602f50c))
* **ml-service:** Add evaluate endpoint ([`ca3437f`](https://github.com/SynapseAnalytics/konan-sdk/commit/ca3437fc2cd5c67e4eb1c85d872b1b5d51282448))
* **ml-service:** Add base classes for an ml-service ([`efbf75e`](https://github.com/SynapseAnalytics/konan-sdk/commit/efbf75e09edb7be8e203875b197001f9987a733f))

### Fix
* **mlservice:** Override ServiceFeedback.prediction ([`46d3750`](https://github.com/SynapseAnalytics/konan-sdk/commit/46d3750d61415ba85266092e61ffc3494edc30c1))
* **evaluate:** Fix typing and inheritance of Types ([`cb301bb`](https://github.com/SynapseAnalytics/konan-sdk/commit/cb301bb7fda102ed1e78f1013ba27f28cca2adba))

### Documentation
* Update links in pypoetry.toml ([`da9fb92`](https://github.com/SynapseAnalytics/konan-sdk/commit/da9fb925bd47de94353b4230aabb72628528d46c))
