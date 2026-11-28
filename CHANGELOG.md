# Changelog

Each entry is `python -I extract/diff.py <previous build> <this build>`.

## android 357204

357.4 - Alpha. The wire format, kinds, models, gateway events, reducers
and cache tables are unchanged. 5 PropIds are appended (901 to 905), and
no existing id moved. The platform reads all 5, 4 of them as Bool and
`minHeightHold` as a Number.

The host gained a `SoundboardAudio` module (`loadPreview`, `trim`,
`isOpusEncoderAvailable`), the `@soundboardAudio` event and the
`dme_mobile_host_soundboard_ogg_opus` export. The guest gained the
`wasm-app-forwarding` and `wasm-app-guild-rail` modules. The new atoms
include `apks`, `expectedLibs`, `signers`, `integrity` and `installer`.
x86_64 no longer links `rand_chacha`. Only the host and
`libappmodules.so` changed.

```
abi/arm64-v8a/libs.tsv
  changed  libappmodules.so	2936816	b86770075438ad4433021f5653c298103a0f76a2c8346b341f9386e62057758d
        -> libappmodules.so	2935488	13fedb3bd3e48fff2e00d924a66a188cee12f0fc183008c5b51b75f7c976be72
  changed  liblibdiscord_wasm_host.so	111701832	26d6cf7cf9bb024b760b70760165e8dd2652c88fb86fde65132630b08a10d194
        -> liblibdiscord_wasm_host.so	112438024	1bf3843812b8da41e64fc5e3027582f2a37c2931474062bb8d0efbb9c52d5cbb

abi/armeabi-v7a/libs.tsv
  changed  libappmodules.so	2150448	56bd9f05f6d37b73a410214ae8d2529239158b16fb4646ad1889e775148bfdbe
        -> libappmodules.so	2149744	38069eb1a60d403d00ac9ad9d1efbe57b9f0fc658d1c74712fddcfb3e8956197
  changed  liblibdiscord_wasm_host.so	73817812	8c9b6286ab504dcbc9cef80fad23b44c8c7e0fbdde359c56c26b2e4eeb56c74c
        -> liblibdiscord_wasm_host.so	74302652	6f825b105c0375fb7edfb86402256ecc5c6550d395292b30a81bef2db62aaf72

abi/x86/libs.tsv
  changed  libappmodules.so	3293636	cd3c8093ce3b267c360b3658b407f62f478e27cfa1bee7b953752a5a7b177a65
        -> libappmodules.so	3292372	49bb58f615770baee59f4fff14fd2b1221adc72c6bc3fecad587775baa578d8c

abi/x86_64/crates.txt
  removed  rand_chacha@0.3.1

abi/x86_64/libs.tsv
  changed  libappmodules.so	3132576	c5665a49d016d6cb5e8c84d7a7411eed813c140c88217a1f5e0fcaa2e09c9e90
        -> libappmodules.so	3131328	89889edd2217100d6724209ce81d8f7c7750e4923b6c0c60252b4c8ba8be9974
  changed  liblibdiscord_wasm_host.so	125557136	be10d806a70debf09e798cfce2f8cd02a416556737f3e3684a737504d5810629
        -> liblibdiscord_wasm_host.so	126334560	862075d63d8858c24252613e502df3cae8271abedfe1bead1c04ccd31fe5af6f

atoms.tsv
  added    1611	history
  added    1846	audioUri
  added    1872	galleryName
  added    2062	signers
  added    2563	waveform
  added    2850	endMs
  added    2880	expectedLibs
  added    2951	integrity
  added    2967	initiator
  added    2981	waveformSampleCount
  added    2999	startMs
  added    3008	apks
  added    3402	installer
  added    3477	package

build.txt
  added    version-name	357.4 - Alpha
  added    version-code	357204
  removed  version-name	357.3 - Alpha
  removed  version-code	357203
  changed  apk	base	discord-357203-base.apk	sha256:95715d3277deebeca8c0ef091778300701012c4fa05099d89896a6d9413c0474
        -> apk	base	discord-357204-base.apk	sha256:93213a30a9bdb2399832e6d7df6d6c7b4edcc6785844b43638059f7d9190005c
  changed  apk	config.arm64_v8a	discord-357203-config.arm64_v8a.apk	sha256:1f69dfb7874ff0fc91ad7ad29de987d66c74033d7355280545a05da9430dd76f
        -> apk	config.arm64_v8a	discord-357204-config.arm64_v8a.apk	sha256:86cec6de95b541410a5214ce02fd0f398ab3797f53f98f0a17e153ac3ee4a740
  changed  apk	config.armeabi_v7a	discord-357203-config.armeabi_v7a.apk	sha256:5af63431da9d45adbf6a4d6d070f75444dbb51f40b64d445f011cc57ee58d4cf
        -> apk	config.armeabi_v7a	discord-357204-config.armeabi_v7a.apk	sha256:0536706a221cec2ddac9f4ee2cd6bfd5a7cb56c8e2c8e48ada1615e0b7e17e48
  changed  apk	config.x86	discord-357203-config.x86.apk	sha256:9613a6e7ea8f068a0ceef09dfbd179bbe4172a7fc73e648c61081bc81f9b19e2
        -> apk	config.x86	discord-357204-config.x86.apk	sha256:0e52534cce8f0d382e33e374bcfe99a9021d10e0aefe0044e50e449cc06cd89b
  changed  apk	config.x86_64	discord-357203-config.x86_64.apk	sha256:80585bf9dfe60a30f9e3d2afc76d8baace4105321757542bf1b8ddd50c630b1a
        -> apk	config.x86_64	discord-357204-config.x86_64.apk	sha256:8470912357d3ac2c73e8cf07a06ce4f3f651321537e0c9d056e05b0438fe4cdb

events.txt
  added    2369	@soundboardAudio

experiments.txt
  added    2026-11-nitro-trials-brand-refresh	host
  added    2026-11-phoenix-switch-entrypoint	bundle,host
  added    2026-11-shop-promotion-expiry-refetch	host
  removed  2026-10-profile-default-tab-with-content	host
  removed  2026-11-phoenix-switch-entrypoint	bundle

exports.txt
  added    dme_mobile_host_soundboard_ogg_opus

first-party-crates.txt
  added    wasm-app-forwarding
  added    wasm-app-guild-rail

guest-modules.txt
  added    wasm-app-forwarding
  added    wasm-app-guild-rail

host-calls.txt
  added    2060	CrashReporter.noteTestCrash
  added    2176	SoundboardAudio.loadPreview
  added    2285	SoundboardAudio.isOpusEncoderAvailable
  added    2417	SoundboardAudio.trim
  added    2455	SoundboardAudio
  added    2513	CrashReports.noteTestCrash

propid-types.tsv
  added    901	resourceDensity	Bool	n0.j
  added    902	accessibilityNoStop	Bool	n0.j
  added    903	runsUnderKeyboard	Bool	n0.j
  added    904	minHeightHold	Number	n0.j
  added    905	opensAtMinHeight	Bool	n0.j
  114 props read by other classes (jadx names; usually renaming)

propids.tsv
  added    901	resourceDensity
  added    902	accessibilityNoStop
  added    903	runsUnderKeyboard
  added    904	minHeightHold
  added    905	opensAtMinHeight

wire.txt
  added    propid-count	906	-	extracted	the host's PropId table and the platform's name array
  removed  propid-count	901	-	extracted	the host's PropId table and the platform's name array

```

## android 357203

357.3 - Alpha ships Phoenix again, with libdiscord unchanged. The diff
below is against 357201, the last build with Phoenix, whose Phoenix tables
357202 kept. The wire format, kinds, models, exports, gateway events,
reducers and cache tables are unchanged. 4 PropIds are appended (897 to
900), and no existing id moved. The platform reads one of them,
`accessibilityLeads`, as a Bool.

The host now links wasmtime 36.0.20 and cranelift 0.123.20, with
`pulley-interpreter` in place of cranelift's native backend on
armeabi-v7a, and `jpeg-encoder` is gone. Its strings reject a precompiled
module whose SHA-256 doesn't match a manifest, and name `worklets-*.cwasm`
files. No APK carries a `.wasm` or `.cwasm` file. The guest gained the
`wasm-app-channel-list` module. Apart from the host, which grew by 6.1 MB
on x86_64, only `libappmodules.so` changed since 357201.

```
abi/arm64-v8a/crates.txt
  added    allocator-api2@0.2.21
  added    bumpalo@3.20.3
  added    cranelift-bforest@0.123.20
  added    cranelift-bitset@0.123.20
  added    cranelift-codegen@0.123.20
  added    cranelift-entity@0.123.20
  added    cranelift-frontend@0.123.20
  added    cranelift-native@0.123.20
  added    crossbeam-epoch@0.9.21
  added    foldhash@0.1.5
  added    gimli@0.32.3
  added    hashbrown@0.15.5
  added    itertools@0.14.0
  added    object@0.37.3
  added    rayon-core@1.13.0
  added    rayon@1.12.0
  added    regalloc2@0.12.2
  added    semver@1.0.28
  added    target-lexicon@0.13.5
  added    wasmparser@0.236.1
  added    wasmtime-environ@36.0.20
  added    wasmtime-internal-cranelift@36.0.20
  added    wasmtime-internal-jit-icache-coherence@36.0.20
  added    wasmtime-internal-math@36.0.20
  added    wasmtime-internal-slab@36.0.20
  added    wasmtime-internal-unwinder@36.0.20
  added    wasmtime@36.0.20
  removed  jpeg-encoder@0.6.1

abi/arm64-v8a/libs.tsv
  changed  libappmodules.so	2934576	b00e2157d9521f0b7a8cc2bc6950b15fbe4779826e1df4aaf61212270a3eb3fc
        -> libappmodules.so	2936816	b86770075438ad4433021f5653c298103a0f76a2c8346b341f9386e62057758d
  changed  liblibdiscord_wasm_host.so	107024984	b03ec53614622b3a6706c88060db43b9a07d757443d865e5437a075e67ac9947
        -> liblibdiscord_wasm_host.so	111701832	26d6cf7cf9bb024b760b70760165e8dd2652c88fb86fde65132630b08a10d194

abi/armeabi-v7a/crates.txt
  added    allocator-api2@0.2.21
  added    bumpalo@3.20.3
  added    cranelift-bforest@0.123.20
  added    cranelift-bitset@0.123.20
  added    cranelift-codegen@0.123.20
  added    cranelift-entity@0.123.20
  added    cranelift-frontend@0.123.20
  added    crossbeam-epoch@0.9.21
  added    foldhash@0.1.5
  added    gimli@0.32.3
  added    hashbrown@0.15.5
  added    itertools@0.14.0
  added    object@0.37.3
  added    pulley-interpreter@36.0.20
  added    rayon-core@1.13.0
  added    rayon@1.12.0
  added    regalloc2@0.12.2
  added    semver@1.0.28
  added    target-lexicon@0.13.5
  added    wasmparser@0.236.1
  added    wasmtime-environ@36.0.20
  added    wasmtime-internal-cranelift@36.0.20
  added    wasmtime-internal-math@36.0.20
  added    wasmtime-internal-slab@36.0.20
  added    wasmtime-internal-unwinder@36.0.20
  added    wasmtime@36.0.20
  removed  jpeg-encoder@0.6.1

abi/armeabi-v7a/libs.tsv
  changed  libappmodules.so	2149248	fe4627eb61da814cd8c2f76eec07dd147b3efaccd778d34f78c085839acdac03
        -> libappmodules.so	2150448	56bd9f05f6d37b73a410214ae8d2529239158b16fb4646ad1889e775148bfdbe
  changed  liblibdiscord_wasm_host.so	71101860	3a14dbe02d98d693bbce9f4ca5027d827fafbfbd1b0b372c01da5214518d4f19
        -> liblibdiscord_wasm_host.so	73817812	8c9b6286ab504dcbc9cef80fad23b44c8c7e0fbdde359c56c26b2e4eeb56c74c

abi/x86/libs.tsv
  changed  libappmodules.so	3291316	4fb0ea0674ceab529c36e7f5f93c7184f5e2f7f102b2935121d1842100816caf
        -> libappmodules.so	3293636	cd3c8093ce3b267c360b3658b407f62f478e27cfa1bee7b953752a5a7b177a65

abi/x86_64/crates.txt
  added    allocator-api2@0.2.21
  added    bumpalo@3.20.3
  added    cranelift-assembler-x64@0.123.20
  added    cranelift-bforest@0.123.20
  added    cranelift-bitset@0.123.20
  added    cranelift-codegen@0.123.20
  added    cranelift-entity@0.123.20
  added    cranelift-frontend@0.123.20
  added    cranelift-native@0.123.20
  added    crossbeam-epoch@0.9.21
  added    foldhash@0.1.5
  added    gimli@0.32.3
  added    hashbrown@0.15.5
  added    itertools@0.14.0
  added    object@0.37.3
  added    rayon-core@1.13.0
  added    rayon@1.12.0
  added    regalloc2@0.12.2
  added    semver@1.0.28
  added    target-lexicon@0.13.5
  added    wasmparser@0.236.1
  added    wasmtime-environ@36.0.20
  added    wasmtime-internal-cranelift@36.0.20
  added    wasmtime-internal-math@36.0.20
  added    wasmtime-internal-slab@36.0.20
  added    wasmtime-internal-unwinder@36.0.20
  added    wasmtime@36.0.20
  removed  jpeg-encoder@0.6.1

abi/x86_64/libs.tsv
  changed  libappmodules.so	3130464	f7825f270b367d88484f0c2adcd977855e20f1b1a14d37e3d26f658820947212
        -> libappmodules.so	3132576	c5665a49d016d6cb5e8c84d7a7411eed813c140c88217a1f5e0fcaa2e09c9e90
  changed  liblibdiscord_wasm_host.so	119430624	db96393f7afa030f51eefa08bff10a58874f1531c64c8b4d255c8bb3329181c0
        -> liblibdiscord_wasm_host.so	125557136	be10d806a70debf09e798cfce2f8cd02a416556737f3e3684a737504d5810629

atoms.tsv
  added    1772	httpsOnly
  added    1915	keepFocus
  added    2725	train

build.txt
  added    version-name	357.3 - Alpha
  added    version-code	357203
  removed  version-name	357.1 - Alpha
  removed  version-code	357201
  changed  apk	base	discord-357201-base.apk	sha256:4c05eb19d087eb408b2e5f772349817d7333afc72f93ba8c1a1a111ee1480701
        -> apk	base	discord-357203-base.apk	sha256:95715d3277deebeca8c0ef091778300701012c4fa05099d89896a6d9413c0474
  changed  apk	config.arm64_v8a	discord-357201-config.arm64_v8a.apk	sha256:2d37434a1e9f2850fc527024ff6f986c9be9560788a7ea912408e26450178860
        -> apk	config.arm64_v8a	discord-357203-config.arm64_v8a.apk	sha256:1f69dfb7874ff0fc91ad7ad29de987d66c74033d7355280545a05da9430dd76f
  changed  apk	config.armeabi_v7a	discord-357201-config.armeabi_v7a.apk	sha256:63788fd5ea6cea663657041b1ccbd1e53dcacd35ed63bb827d5d6c9556719a5e
        -> apk	config.armeabi_v7a	discord-357203-config.armeabi_v7a.apk	sha256:5af63431da9d45adbf6a4d6d070f75444dbb51f40b64d445f011cc57ee58d4cf
  changed  apk	config.x86	discord-357201-config.x86.apk	sha256:2ae803c3170479b1e8a34bcbf8e7ddecc2bb140da38b648d7c764d63524c33c8
        -> apk	config.x86	discord-357203-config.x86.apk	sha256:9613a6e7ea8f068a0ceef09dfbd179bbe4172a7fc73e648c61081bc81f9b19e2
  changed  apk	config.x86_64	discord-357201-config.x86_64.apk	sha256:ec963a886ad54d8bb5bcba5d6c6f703a4731548af1f1c22229c926329d445784
        -> apk	config.x86_64	discord-357203-config.x86_64.apk	sha256:80585bf9dfe60a30f9e3d2afc76d8baace4105321757542bf1b8ddd50c630b1a

drawables.tsv
  added    adx_ic_other_sign_in	-	vector
  added    ic_splash_logo_light	v31	inset
  added    splash_logo_light	v31	inset

experiments.txt
  added    2026-11-app-block	host
  added    2026-11-badge-social-comparison	host
  added    2026-11-badge-social-comparison-mobile	bundle,host
  removed  2026-09-edit-profile-collectibles-ordering	host
  removed  2026-09-mobile-nitro-upsell-in-shop-feed	bundle,host
  removed  2026-09-mobile-nitro-upsell-in-shop-pdp	host
  removed  2026-11-badge-social-comparison-mobile	bundle

first-party-crates.txt
  added    wasm-app-channel-list

guest-modules.txt
  added    wasm-app-channel-list

propid-types.tsv
  added    897	linkInBackdrop	-	unread
  added    898	accessibilityLeads	Bool	n0.j
  added    899	keepScreenFocus	-	unread
  added    900	drawDistance	-	unread
  392 props read by other classes (jadx names; usually renaming)

propids.tsv
  added    897	linkInBackdrop
  added    898	accessibilityLeads
  added    899	keepScreenFocus
  added    900	drawDistance

wire.txt
  added    propid-count	901	-	extracted	the host's PropId table and the platform's name array
  removed  propid-count	897	-	extracted	the host's PropId table and the platform's name array

```

## android 357202

357.2 - Alpha ships no Phoenix. No ABI split carries
`liblibdiscord_wasm_host.so`, and `classes.dex` has no
`com/discord/nativeapp` classes. The React Native bundle still names
`2026-11-phoenix-rollout`. Apart from the host, only `libappmodules.so`
changed, so this is 357201 with Phoenix taken out. The last 9 `ic_mana_*`
drawables went with it (517 drawables).

The Phoenix tables (PropIds, kinds, wire, host calls, models and the rest)
are still 357201's. `build.txt`, the ABI tables, `drawables.tsv` and
`experiments.txt` are 357202's. 149 experiment names that only the host
held are gone from `experiments.txt`, and the host column is gone from the
rest. That section is left out below.

```
abi/arm64-v8a/libs.tsv
  removed  liblibdiscord_wasm_host.so	107024984	b03ec53614622b3a6706c88060db43b9a07d757443d865e5437a075e67ac9947
  changed  libappmodules.so	2934576	b00e2157d9521f0b7a8cc2bc6950b15fbe4779826e1df4aaf61212270a3eb3fc
        -> libappmodules.so	2936816	b86770075438ad4433021f5653c298103a0f76a2c8346b341f9386e62057758d

abi/arm64-v8a/rustc.txt
  removed  liblibdiscord_wasm_host.so	comment	Android (12285214, +pgo, +bolt, +lto, +mlgo, based on r522817b) clang version 18.0.2 (https://android.googlesource.com/toolchain/llvm-project d8003a456d14a3deb8054cdaa529ffbf02d9b262)
  removed  liblibdiscord_wasm_host.so	comment	rustc version 1.99.0-nightly (73dc9167f 2026-08-01)
  removed  liblibdiscord_wasm_host.so	comment	Linker: LLD 18.0.2
  removed  liblibdiscord_wasm_host.so	rustc-commit	73dc9167f1cd099e525c9ade2e068d1907b78564

abi/armeabi-v7a/libs.tsv
  removed  liblibdiscord_wasm_host.so	71101860	3a14dbe02d98d693bbce9f4ca5027d827fafbfbd1b0b372c01da5214518d4f19
  changed  libappmodules.so	2149248	fe4627eb61da814cd8c2f76eec07dd147b3efaccd778d34f78c085839acdac03
        -> libappmodules.so	2150448	56bd9f05f6d37b73a410214ae8d2529239158b16fb4646ad1889e775148bfdbe

abi/armeabi-v7a/rustc.txt
  removed  liblibdiscord_wasm_host.so	comment	Android (12285214, +pgo, +bolt, +lto, +mlgo, based on r522817b) clang version 18.0.2 (https://android.googlesource.com/toolchain/llvm-project d8003a456d14a3deb8054cdaa529ffbf02d9b262)
  removed  liblibdiscord_wasm_host.so	comment	rustc version 1.99.0-nightly (73dc9167f 2026-08-01)
  removed  liblibdiscord_wasm_host.so	comment	Linker: LLD 18.0.2
  removed  liblibdiscord_wasm_host.so	rustc-commit	73dc9167f1cd099e525c9ade2e068d1907b78564

abi/x86/libs.tsv
  changed  libappmodules.so	3291316	4fb0ea0674ceab529c36e7f5f93c7184f5e2f7f102b2935121d1842100816caf
        -> libappmodules.so	3293636	cd3c8093ce3b267c360b3658b407f62f478e27cfa1bee7b953752a5a7b177a65

abi/x86_64/libs.tsv
  removed  liblibdiscord_wasm_host.so	119430624	db96393f7afa030f51eefa08bff10a58874f1531c64c8b4d255c8bb3329181c0
  changed  libappmodules.so	3130464	f7825f270b367d88484f0c2adcd977855e20f1b1a14d37e3d26f658820947212
        -> libappmodules.so	3132576	c5665a49d016d6cb5e8c84d7a7411eed813c140c88217a1f5e0fcaa2e09c9e90

abi/x86_64/rustc.txt
  removed  liblibdiscord_wasm_host.so	comment	Android (12285214, +pgo, +bolt, +lto, +mlgo, based on r522817b) clang version 18.0.2 (https://android.googlesource.com/toolchain/llvm-project d8003a456d14a3deb8054cdaa529ffbf02d9b262)
  removed  liblibdiscord_wasm_host.so	comment	rustc version 1.99.0-nightly (73dc9167f 2026-08-01)
  removed  liblibdiscord_wasm_host.so	comment	Linker: LLD 18.0.2
  removed  liblibdiscord_wasm_host.so	rustc-commit	73dc9167f1cd099e525c9ade2e068d1907b78564

build.txt
  added    version-name	357.2 - Alpha
  added    version-code	357202
  removed  version-name	357.1 - Alpha
  removed  version-code	357201
  changed  apk	base	discord-357201-base.apk	sha256:4c05eb19d087eb408b2e5f772349817d7333afc72f93ba8c1a1a111ee1480701
        -> apk	base	discord-357202-base.apk	sha256:87dfd79a265e5a0e6f1233d2759ea5a18fa29ca4c7a74ef2d4e6dd8e1ca17e7b
  changed  apk	config.arm64_v8a	discord-357201-config.arm64_v8a.apk	sha256:2d37434a1e9f2850fc527024ff6f986c9be9560788a7ea912408e26450178860
        -> apk	config.arm64_v8a	discord-357202-config.arm64_v8a.apk	sha256:9ab2c827a77ba62cb47333e4fe956ac099543c47058e497e72bf4e2f120e168a
  changed  apk	config.armeabi_v7a	discord-357201-config.armeabi_v7a.apk	sha256:63788fd5ea6cea663657041b1ccbd1e53dcacd35ed63bb827d5d6c9556719a5e
        -> apk	config.armeabi_v7a	discord-357202-config.armeabi_v7a.apk	sha256:85b2b32d52e95d5eeca1102fdf2e0a519fdd7978ab51fe884768c6c67f533e61
  changed  apk	config.x86	discord-357201-config.x86.apk	sha256:2ae803c3170479b1e8a34bcbf8e7ddecc2bb140da38b648d7c764d63524c33c8
        -> apk	config.x86	discord-357202-config.x86.apk	sha256:73ef00d33fec6538da88f060e43e7b9edd68acfb7f61a96fd3da64e98aec1e8c
  changed  apk	config.x86_64	discord-357201-config.x86_64.apk	sha256:ec963a886ad54d8bb5bcba5d6c6f703a4731548af1f1c22229c926329d445784
        -> apk	config.x86_64	discord-357202-config.x86_64.apk	sha256:69f373918e64688706bceb29d101c8aee1ce39a7a5ad754b319ee31e7050b745
  changed  abi	arm64-v8a	45 libs	host
        -> abi	arm64-v8a	44 libs	no host
  changed  abi	armeabi-v7a	45 libs	host
        -> abi	armeabi-v7a	44 libs	no host
  changed  abi	x86_64	45 libs	host
        -> abi	x86_64	44 libs	no host

drawables.tsv
  added    ic_splash_logo_light	v31	inset
  removed  $guild_profile_empty_state__0	-	gradient
  removed  $guild_profile_empty_state__1	-	gradient
  removed  $guild_profile_empty_state__2	-	gradient
  removed  $guild_profile_empty_state__3	-	gradient
  removed  appeal_check_with_stars	xxhdpi	png
  removed  boost_marketing_stars	-	vector
  removed  boost_marketing_wave	-	vector
  removed  emoji_picker_placeholder	-	shape
  removed  guild_profile_empty_state	-	vector
  removed  ic_app_icon_default	-	vector
  removed  ic_bad_connection_strong	-	vector
  removed  ic_bad_connection_weak	-	vector
  removed  ic_circle_fill	-	vector
  removed  ic_mana_flower_star	-	vector
  removed  ic_mana_headphones	-	reference
  removed  ic_mana_headphones_slash	-	reference
  removed  ic_mana_microphone	-	reference
  removed  ic_mana_microphone_slash	-	reference
  removed  ic_mana_synchronize	-	vector
  removed  ic_mana_video	-	reference
  removed  ic_mana_video_slash	-	reference
  removed  ic_mana_x_small	-	reference
  removed  ic_media_playback_24dp	-	vector
  removed  ic_rn_boost_gem_pixel	-	vector
  removed  ic_rn_quest_skip_backward	-	vector
  removed  ic_rn_quest_skip_forward	-	vector
  removed  ic_rn_toolbar_up	-	vector
  removed  ic_thread_spine_curve	-	vector
  removed  ic_video_disabled_local_body	-	vector
  removed  ic_video_disabled_local_slash	-	vector
  removed  img_nitro_subheader_mobile	xhdpi	png
  removed  img_tier_0_subheader_mobile	xhdpi	png
  removed  menu_surface	-	shape
  removed  nitro_icon	-	vector
  removed  pinot_notice_caret_border	-	vector
  removed  pinot_notice_caret_fill	-	vector
  removed  powerups_boost_gem	-	vector
  removed  premium_group_wordmark	-	vector
  removed  premium_role_unavailable	xxhdpi	webp
  removed  premium_tier_0_logo_small	-	vector
  removed  premium_tier_2_logo_small	-	vector
  removed  progress_ring	-	rotate
  removed  rn_gift_game_placeholder	-	reference
  removed  rn_gift_premium	-	reference
  removed  rn_gift_premium_classic	-	reference
  removed  rn_gifting_blocked_dark	-	reference
  removed  rn_gifting_blocked_light	-	reference
  removed  rn_ic_check_24px	-	reference
  removed  rn_img_discord_nitro_logo_left	-	reference
  removed  rn_notif_preview_voice	-	reference
  removed  rn_nuf_add	-	reference
  removed  rn_platform_img_bungie_dark	nodpi	reference
  removed  rn_platform_img_bungie_white	-	reference
  removed  rn_platform_img_roblox_dark	nodpi	reference
  removed  rn_platform_img_roblox_white	-	reference
  removed  rn_premium_img_tier_0_clouds	-	reference
  removed  rn_premium_img_tier_0_mobile	-	reference
  removed  rn_premium_img_tier_2_clouds	-	reference
  removed  rn_premium_img_wumpus_nitro	-	reference
  removed  rn_scrollbar_thumb	-	shape
  removed  splash_dark	-	layer-list
  removed  splash_light	-	layer-list
  removed  splash_logo	v31	inset
  removed  tenure_badge_bronze_small	xxhdpi	png
  removed  tenure_badge_diamond_small	xxhdpi	png
  removed  tenure_badge_emerald_small	xxhdpi	png
  removed  tenure_badge_gold_small	xxhdpi	png
  removed  tenure_badge_opal_small	xxhdpi	png
  removed  tenure_badge_platinum_small	xxhdpi	png
  removed  tenure_badge_ruby_small	xxhdpi	png
  removed  tenure_badge_silver_small	xxhdpi	png
  removed  voice_message_bubble_fill	-	vector
  removed  voice_message_bubble_outline	-	vector
  removed  void_warning_circle	-	vector
  removed  welcome_bg	xxhdpi	webp
```

## android 357201

357.1 - Alpha, libdiscord unchanged. The wire format, kinds, models,
gateway events, reducers and cache tables are unchanged. 26 PropIds are
appended (871 to 896), and no existing id moved. The platform reads 12 of
them. `placeholderPool`, `pool` and `all` lost their platform handlers.
19 of the 45 arm64-v8a libraries changed; the host grew by 3.4 MB.

The host now renders Lottie and sticker frames itself, with `ldh_lottie_*`
and `ldh_sticker_*` exports and the `lottie` and `sticker-frames` crates,
and `fancy-regex`, `kurbo` and `lz4_flex` are new dependencies. The
guest gained the `wasm-app-kit` module. `CheckpointCharacterImage` and
`MediaPicker.splice` are new host methods.

277 `ic_mana_*` vector icons left the base APK (591 drawables, 9 of them
`ic_mana_*`). The platform's turn version check moved out of the op
decoder into a method of its own.

```
abi/arm64-v8a/crates.txt
  added    aho-corasick@1.1.5
  added    bit-set@0.5.3
  added    bit-vec@0.6.3
  added    fancy-regex@0.13.0
  added    kurbo@0.13.1
  added    lz4_flex@0.11.7
  added    regex-automata@0.4.18
  added    regex-syntax@0.8.11

abi/arm64-v8a/libs.tsv
  changed  libNitroModules.so	684968	bcbad9a413a7d012100e18e33ccf61da50f7e9ee50ab65d0caf84ce535544314
        -> libNitroModules.so	684968	66f8dc3f8d1d7f889167d42dae1767d7f9472df12e76ed8848a7346d5b11592e
  changed  libappmodules.so	2931424	05da2ecb4746ef40791796638f3e3af99e7525e66618d765814de5b354a73ac1
        -> libappmodules.so	2934576	b00e2157d9521f0b7a8cc2bc6950b15fbe4779826e1df4aaf61212270a3eb3fc
  changed  libcrash-reporting.so	56376	5812b7f2668c7d01bb4b75cde5f9603a8b84368a48c2d2b495c99ef3c5e8d5f7
        -> libcrash-reporting.so	56376	e2fa62b884b8cef6b4238be833caf9e598f63fa6c6299adce4c83e88b4a90a30
  changed  libgesturehandler.so	74944	9c4942bb89784cbc23dad710c34b84e081e1f4e6ca0aead1ebe33959c0791886
        -> libgesturehandler.so	74944	d5ea72137cb5a81a74f18b01d19d6ac4c8feb13181944c7020361b6290da29f0
  changed  libhermestooling.so	141480	62bbf747191ee99483fe22813c770870ad978ecaade2e3927cd079a3372193dd
        -> libhermestooling.so	141480	5e7c040f6b496369f74ac0c055f05d3cd81962f7c521d2870a6b62e85e6c21db
  changed  libjsi.so	412568	70baccf513dae49a1a56f13e31924d2aa19cf116017764f1003c5d5299fcdf49
        -> libjsi.so	412568	121b01a3ed19e6b3d3c0906ea1ab5867c35158ed52b529a2f0ac1b2826b9c695
  changed  liblibdiscord_wasm_host.so	103669784	36e1cfd3dc32badcb5fc0a814c118a973e8987e29fa3032d1e26c7cdff108d29
        -> liblibdiscord_wasm_host.so	107024984	b03ec53614622b3a6706c88060db43b9a07d757443d865e5437a075e67ac9947
  changed  libreact_codegen_RNCSlider.so	175024	b22c807f5bfc18595582835be3f056e65653ca53465ac4674e04f56f095978ce
        -> libreact_codegen_RNCSlider.so	175024	63580c58a373ea08d79ba7bbe245bca2d6ce3b15b6525ce401c94f5ba815b8e4
  changed  libreact_codegen_RNKC.so	114912	f7f81d804c61fb223c1bd0e16f997c8c9ba46255c0c9628a37cec13b52c93c0c
        -> libreact_codegen_RNKC.so	114912	58cbcd7e86e38deaa502b6930a1973036bfbe187c3cf9e5ecf7429ebc0da24d1
  changed  libreact_codegen_rngesturehandler_codegen.so	269632	77932f8c2ace408c40d002d575c15f2eefca8211397d0a5256fba94b1a41f441
        -> libreact_codegen_rngesturehandler_codegen.so	269632	cfa3d130fac63668580a20786e81d299b3d845f486b32efa0aae7efd93aa3295
  changed  libreact_codegen_rnscreens.so	825392	502b183b72bffffd1291fafbd6395b3e9e4f56fdfe2c6d3fe156539f8c18e421
        -> libreact_codegen_rnscreens.so	825392	caf0121ced7f80d6224a430b4e226adc9ee2a37175f226f26cd3f49a7c008456
  changed  libreact_codegen_rnsvg.so	606272	d77049bf47e41a837f665db308c7b09878174750163a6ae7fcdc76fa205d2a10
        -> libreact_codegen_rnsvg.so	606272	69d12330c1269aa73408180eb74c777638f2b9463f1c53e0228bc117a6b83951
  changed  libreact_codegen_safeareacontext.so	120536	c589eee100866da97661b09320400b06c782ad47a1fa4dc86a4448c75c4be9e0
        -> libreact_codegen_safeareacontext.so	120536	a486c4055fcfe63ea25478858cdf9badde36d8f586720c9122fdd4c9b0d56428
  changed  libreactnative.so	7070272	9f830bb87d8d0bfc018f09d0e17ad3859d752d7bf780efa24cfc1a56d40eb54c
        -> libreactnative.so	7070272	03e8bbc266b8f9670a052aa73274f393926a9c161971868b264244fbcce0af51
  changed  libreanimated.so	1658032	6400a045a9be584904ff1c9d8f0fa51a303afa7476fa5b5789e72e09e3c704c4
        -> libreanimated.so	1658032	1f06bea28c71e1d3a21a42ec0f99029dc5e2c54d7212bde0740eb64902349dde
  changed  librive.so	2320512	1f8e2aa04d1e7ec9e6e9dfaac5a670345e67c63eb83977c4c90120c400dccb47
        -> librive.so	2320512	22edfa800781fe66e08d3e27f9cab575a84ab8e390ff9f1d6692f70f8b798912
  changed  librnscreens.so	86752	3fc3977a57bb81a501073aca51a65118aa8b28d6675dccfb587ffbf2ebc74bc1
        -> librnscreens.so	86752	f799abc4d9f3f7d4f8789471b9710cadde431d1fe71284141aee8a0d28ca17cf
  changed  libsizing_util.so	28216	6ebf4a86e068d6fabea7c5ffa2c7aa1cda6199c30a04dfae86b292ae0450086d
        -> libsizing_util.so	28216	87c6d2dc3e8eb7cac1e622955025f6b0f6c53f31a4b0353c73f710b75e5ef3c8
  changed  libworklets.so	935904	e870339a00b409b9cb088e6a8d89b711ca7512eaa979cee17bf5f9cc93da5e2b
        -> libworklets.so	935904	e39f99d0c652b85d0df9dd116548238545cde442a3e1aaf2c2d5854fdd36fc21

abi/armeabi-v7a/crates.txt
  added    aho-corasick@1.1.5
  added    bit-set@0.5.3
  added    bit-vec@0.6.3
  added    fancy-regex@0.13.0
  added    kurbo@0.13.1
  added    lz4_flex@0.11.7
  added    regex-automata@0.4.18
  added    regex-syntax@0.8.11

abi/armeabi-v7a/libs.tsv
  changed  libNitroModules.so	477608	efe879c39844b87c8b3d19c2a8d4f346c6b7b40b41ce93e388aa35aac2087cfc
        -> libNitroModules.so	477608	afb988784b379cbca44860b166446ce5d26790b8c01156241bbd8f8dad3c4594
  changed  libappmodules.so	2146860	ca16757c9dafb81c45a7a36ee725a9808a6d05f393b53b946ad44d98f580430f
        -> libappmodules.so	2149248	fe4627eb61da814cd8c2f76eec07dd147b3efaccd778d34f78c085839acdac03
  changed  libcrash-reporting.so	25256	e8409580efe1065986b9f5a6640c8c34da409b277b5856e202bd5eee0ffc2e8f
        -> libcrash-reporting.so	25256	7fa2db3bd76bee6611e33abafd34dd39cc625d1a77c25b35917c01934f2d9178
  changed  libgesturehandler.so	35656	7e09d9c1b6e3aa0b75eb31a170bb5a61fc24cf7d6a510261a7780636b4662e83
        -> libgesturehandler.so	35656	b8a2d42c3be60df5da171b96e95aa5cfec3e3811eb81153d09d69dd4848e06d0
  changed  libhermestooling.so	76596	9b291121a5e444354170bba00dbe42f822fbfc7421bb394b09da06cf7253fe94
        -> libhermestooling.so	76596	3e35b27966b9bc2a21e615e16e2ba634a969088a3c8ecb25f61702a825500f75
  changed  libjsi.so	289652	592fb539f2934d3dba68a277a04f346fb2608bb1db31001706a4d67e256fc4e3
        -> libjsi.so	289652	74ef52d7df9885a1e4226ee49a5b45cbf690dc61b075236337c09375a8b88e03
  changed  liblibdiscord_wasm_host.so	68775676	7650157bba6fa0f5b99df282e3cd0450ef01cc845426570c4bab708541d3a43a
        -> liblibdiscord_wasm_host.so	71101860	3a14dbe02d98d693bbce9f4ca5027d827fafbfbd1b0b372c01da5214518d4f19
  changed  libreact_codegen_RNCSlider.so	117868	dd457bea1556c59b7b31862ad1e70701d5f53b7d56e93da731de0efecb363413
        -> libreact_codegen_RNCSlider.so	117868	2e48e525a15ae56d1a1fbd3d5d95a220d149a985b8610621686d8f17d24ff077
  changed  libreact_codegen_RNKC.so	67212	23535add4b3383511c43510be3a8f7b0fb8f69c289d4c4a903d24efbc2c2a9e9
        -> libreact_codegen_RNKC.so	67212	e015a71063bca293064b55f2e999aed245e7cb2de7a496a85f4dbb2ef2a77253
  changed  libreact_codegen_rngesturehandler_codegen.so	185276	b6309315f5941ac858b22c4f2ca6ed18ae4d04bb545d5212a530a453aa86a417
        -> libreact_codegen_rngesturehandler_codegen.so	185276	c36efc4167e28f9d7e0a71a16be1fa58533ad18c5268f5cf31f3f5ad7066b793
  changed  libreact_codegen_rnscreens.so	573952	6603f9e221dc3580fb1d2c02f258472dc16909368424a92b93d6899c064d8db8
        -> libreact_codegen_rnscreens.so	573952	36342ce6aff6e14f72cf9144eddf7b4b642f72b95c26249aae507f753b9fd98e
  changed  libreact_codegen_rnsvg.so	435228	84833ee9e9e0c6111ea12176298d00d45b66c61fcc411b3a388b2f3d5dfff3bb
        -> libreact_codegen_rnsvg.so	435228	3352710411ad7d5e86cd39cd74f050161cbc4b47f5aa25e89db8c26d644fe5cd
  changed  libreact_codegen_safeareacontext.so	70860	4ba90430e689cf7840c30cd0d084227317f26c0782f7a87f0c33392d139f45f5
        -> libreact_codegen_safeareacontext.so	70860	d029adc87582660ce203ebc74377e684b3c5a53a724f86a6c49a7b9503c85b07
  changed  libreactnative.so	4905856	be39ae60d41fec33e25d64efd55df1af150500b4ccb934c4b24269e0f824007a
        -> libreactnative.so	4905856	4c7231f798a437bfad63856a9265fb9b0a8866733f874b30ad4a5d164336f064
  changed  libreanimated.so	1123032	cbf52d13b7b47beb76400dadba7ced21384f55e1c49d04090fa81bfe12344a40
        -> libreanimated.so	1123032	f235bddd23f4539201d5de918a18062bb3e591f2af2b5d7e2722391efe480dff
  changed  librive.so	1671128	06c7beea209c5415f1d88f31881b1b1e0a5edad1f3b0132642e15bee283a0999
        -> librive.so	1671128	bb2067c2ef84c139e9028152215b4f890b6c9b567a4b64aacb8b0a35000d4df7
  changed  librnscreens.so	43776	b2eb0ff5e33dc99f7d129c89d9851919a53367984c423fb56a9390f28a628fc5
        -> librnscreens.so	43776	a191f545ee9b2995ee16990afda2a162995c3ceff62094992f70bcbf4824dc5c
  changed  libsizing_util.so	3596	b09efae464866f1eb23cfd81873944d420805f4b0d58d2d0a27e93baa2b940ee
        -> libsizing_util.so	3596	84451b42720a5cd0551ea23e0081e4bdbe719c24242016725ebaf25c137277f8
  changed  libworklets.so	621128	9591f356a42dd78f57675a6741ad0c35c4cd505cc02a7b3a6db1b90e18f8fbe8
        -> libworklets.so	621128	210643e1881fa0f92ddb0873ae589bce8089dd0bddd2c0e4e3c08dffd6cff663

abi/x86/libs.tsv
  changed  libNitroModules.so	684648	84e55974b3e73c8e11f548ee52a0b416bc12888cd3ab1a0d5296b9989d494e8f
        -> libNitroModules.so	684648	3f892b9242ae75c21e232206a097dffec87de14ffabd8bf98f480d5c4260bbdc
  changed  libappmodules.so	3287352	fdf5336aeac716d165f700c7d8f97e509491b185b01b356950596909ba9ce3a2
        -> libappmodules.so	3291316	4fb0ea0674ceab529c36e7f5f93c7184f5e2f7f102b2935121d1842100816caf
  changed  libcrash-reporting.so	54396	4fbf17355f86cb8d56f7a652c1163b4098a456e097e272537404b8eb5417a3a5
        -> libcrash-reporting.so	54396	9cd32f6a8b747f6ba90e86d536a7f7ab3874cae24b026662d890558139c7b85a
  changed  libgesturehandler.so	69420	8fe50497a2d36835687fd0e071a42184533b58f9b77d8d896a733577eaa02f7a
        -> libgesturehandler.so	69420	2155ff4666c7cde7b684a925aef02bd3694271aa5950d7f86be7ed9653c3dcb3
  changed  libhermestooling.so	136796	84f34926a219b44b06f6623dfabf0e336d8da6ac1e51e30155072ea0938541ca
        -> libhermestooling.so	136796	452a7c1b48250af09031483e693aaa7cb624fff7528a563d3996bb12bc3f0071
  changed  libjsi.so	437100	b94d675968b2072905c40ec534de099552b02761ad559de954081079deb91b00
        -> libjsi.so	437100	5c8c0ee998ca5513c8868f14619f6b0291e40ff4f02f8820177f7aa281ba46b1
  changed  libreact_codegen_RNCSlider.so	191412	662d557d5d79be3b7a03ada337d85da650b299ddbded591c56203b7d61c1261b
        -> libreact_codegen_RNCSlider.so	191412	2396798ac7354be67ad272711ec73f31d27635c7d1bf22b0171f136541582b1b
  changed  libreact_codegen_RNKC.so	118716	13a5d4b52a52654e9b1885c74ecd8d43850786d5470606efbe07761234d04998
        -> libreact_codegen_RNKC.so	118716	fd106c5ca634f83c686749a7ca87f76e138af99211ee278ac32ad109d793caab
  changed  libreact_codegen_rngesturehandler_codegen.so	299128	35ce0afe6e70a80c6212adc55223c87f89bce486b9e24c095b284d7855715bfd
        -> libreact_codegen_rngesturehandler_codegen.so	299128	8ac1697067f3e62ead688304a587a19bf7f2da9636a97a882b1e9032318fdef5
  changed  libreact_codegen_rnscreens.so	886916	b09f5638b6cffe6b8cdb6250e07c64a1fa8fd6a89e7c4865df4e5abf36389ed9
        -> libreact_codegen_rnscreens.so	886916	d2f9d77d0cb78c290c63447a9cf151483e9ec1a3955c5d21b770f93ed444984f
  changed  libreact_codegen_rnsvg.so	741488	f034230b2e5fc709bc99a1f0567d8d6d1e1b48c38847d705532642a6df02dcf4
        -> libreact_codegen_rnsvg.so	741488	a00cf9dfe8146bcda3a075fe7b6507d41e0a63c681e08aaec8f073320a1cb809
  changed  libreact_codegen_safeareacontext.so	120564	824f072e9310fbc24bb6a3812b173811e9f914c0f69028d8e2c39a4616c35a6f
        -> libreact_codegen_safeareacontext.so	120564	3839d499ec828c9c7ee59e1cce9d055c1181234d83ec0c46b500ffdbc7c079bf
  changed  libreactnative.so	7430968	febc3f250e581cf8826a8198feb75aed1687fcc4d1515520d2d79e4ee42f9434
        -> libreactnative.so	7430968	bab00750fe9578df02fb7f71f6866c0106e34a2b08220af122ca996acb1972db
  changed  libreanimated.so	1680636	aa552c686e9398ee40998a13bfe38e470022db6ba7e2ca3e51db10acebaae51b
        -> libreanimated.so	1680636	8b564cd9d864a8672f1f9c8d6f26c54a21f29c15221607bf873cd7e4ad38e561
  changed  librive.so	2299016	bb832b547e93c39c0a4a9a1b56dd831d4bf6d8fff058816b89bb597eb84b4af6
        -> librive.so	2299016	06d439dddfc7bd0e0322013ef78cf0a90a3223ea8ecb092f2cffd18b3b5caea5
  changed  librnscreens.so	81748	5ba2ab0fd98ce7b4a04cdca3e40cfbb237aeac1bd733cd29a70665f65be06fd5
        -> librnscreens.so	81748	8d1c8a42ad10b7fdbab32eca74c0687435dd48f36ebb84be4150c8bc830368f2
  changed  libsizing_util.so	28064	89ae38a9832192d9c7da8523ea7e9ccb2a084d477fad6ccbfed2c461dbf435b3
        -> libsizing_util.so	28064	82d629b80d0b8a0cadf62d6342d2d552c03f3ff699ed2ffc5669fc29a1e33add
  changed  libworklets.so	859448	8648ab15fbc4971e68e20f9343efb3ee72a0983b2598c6c1d481fd11f90e1687
        -> libworklets.so	859448	9bc63da8e06f7a4fca0becd9175a438e788edc95706b3c0d4db885452990c366

abi/x86_64/crates.txt
  added    aho-corasick@1.1.5
  added    bit-set@0.5.3
  added    bit-vec@0.6.3
  added    fancy-regex@0.13.0
  added    kurbo@0.13.1
  added    lz4_flex@0.11.7
  added    regex-automata@0.4.18
  added    regex-syntax@0.8.11

abi/x86_64/libs.tsv
  changed  libNitroModules.so	689552	d4727a1579ea90e6190fc34ca78791f328752db87a9e6f784a0153d769c71221
        -> libNitroModules.so	689552	a4d0be8efd4d9fb8257d8b08185a38be61062e4107c190b5bdbfb03b0bc006db
  changed  libappmodules.so	3127280	4aa0e0ba24418a2b4c3d3d8748c3270e275d096739ccde4c2e2d4ffe6b013c38
        -> libappmodules.so	3130464	f7825f270b367d88484f0c2adcd977855e20f1b1a14d37e3d26f658820947212
  changed  libcrash-reporting.so	56064	77de1f556637618f8f61a10fe3d8e649e6a934c912bf7f40265eba79ca784ae4
        -> libcrash-reporting.so	56064	6f1ef04a6ddf9d48c90aa28e3717741365f15f6f5a23f7df8424fbd172db8c49
  changed  libgesturehandler.so	71296	ba04c43599d39eb7ccbf4d9e5bdf108b95865f38840468e44fc7bad062d32a8f
        -> libgesturehandler.so	71296	e36922b194e3f8d82bca4ff376c20c9122e898dc66c0f8d175250d6bd66bb67d
  changed  libhermestooling.so	138208	fe69e408d2c900fa20051477e756edabd235c82a6bf45fdedbe5c4f685a644dc
        -> libhermestooling.so	138208	9a98b840ae862c05811e607997bbdba304bbf6e61eafa164b1f78537a34df42c
  changed  libjsi.so	418808	529f7a00de8b4be2fcc766f9afa0a3a6c2311b787f03b829bf1b9b64e25c1770
        -> libjsi.so	418808	8f71fbcb08e0bbaf6c21ba039071c24cf10802876d8f19c4682b5b70c38870c1
  changed  liblibdiscord_wasm_host.so	115683536	b1553100356b2594639d6c17cd849460cc04af564f43050424ec4b8e484f1715
        -> liblibdiscord_wasm_host.so	119430624	db96393f7afa030f51eefa08bff10a58874f1531c64c8b4d255c8bb3329181c0
  changed  libreact_codegen_RNCSlider.so	185520	bdc45cdda38427040c6929dd96b9fc3b270b5ae51a6aba63319efabe4e83006b
        -> libreact_codegen_RNCSlider.so	185520	24cb67aa9ea07a1ead3553241611a92055cd7743df0e889c3bc649463ad416e1
  changed  libreact_codegen_RNKC.so	115344	066beaf5a2329d3d972e80fab3dd5d2bf0c5814bb91aba1e28a504cb714e8e02
        -> libreact_codegen_RNKC.so	115344	6e7ad1b268e34f439124cb14e66645db5b20cfa0d11aa122ec6b6d5da4e0144d
  changed  libreact_codegen_rngesturehandler_codegen.so	280048	744b48341468c7e412218506239621b5c0727ee5fe865589f75da9b6d0f29120
        -> libreact_codegen_rngesturehandler_codegen.so	280048	01e2f44048851213ed18de62520737c4331b729267788c6e5f61495b4c9afcb0
  changed  libreact_codegen_rnscreens.so	860032	4e5fdabc2d3bbf78f817d46207da27c36f6bd71665ff934008a9b29dd5d3bc29
        -> libreact_codegen_rnscreens.so	860032	b0cdb05ca2da1aa7cef68df2bccc286b2e622cf23bc0ee8df5a16dce47b48635
  changed  libreact_codegen_rnsvg.so	693888	cfacaeeff378fe2fc6299e7f6b3e80dd0cfc3f7c08184177873bac163f257bde
        -> libreact_codegen_rnsvg.so	693888	226de92e8743b1e87e54a9105c7c7441277b7370d2c72f5e83e2567c7c985785
  changed  libreact_codegen_safeareacontext.so	122984	a74c7972020d4e692d8e38eb4a48212122f19ebc7c789efc51cdbd489a908569
        -> libreact_codegen_safeareacontext.so	122984	0097ce87717e28e71a76a4eab0917e0ece70e8c7c54a010e4aa37a02f583c3d1
  changed  libreactnative.so	7170592	3afbe24410879819baa3d47abd66ca24c1994e24fc02f9bfe60741cfb6dd294b
        -> libreactnative.so	7170592	1adc61515f57fdbf7ded31f7f36f374110b8e5a0060d95f82029e955538011a7
  changed  libreanimated.so	1714040	ed066526cc3f0d0500ed4031e222dae10ee298f4344d9b85639284233b3e508a
        -> libreanimated.so	1714040	c445d98e2df79dccef1851195ba37c701c8391a5fc8797abd5e20602fd6c0694
  changed  librive.so	2340344	f03b2198f373ded369fb62ab5e0d3af932279ba3c9cb41ba67efb494a5cb4553
        -> librive.so	2340344	b90e81b679293fa140cc5a1c3d1b992b73c88292b68ca41ccc979ca48c8e8eb8
  changed  librnscreens.so	83688	68b0ea1cbca1586d4a4e9cca33be60d26ed1044e11e86cc040697148e49d75bd
        -> librnscreens.so	83688	f1a31351cb45472ba6013831ef99c16265174df2fb74617fda2a34a64c10e768
  changed  libsizing_util.so	28168	16aa77f13252403a5d9fcd4e3ba19f56ebb82ffafef214416db91a3eeb586f83
        -> libsizing_util.so	28168	ae2c3f0bea1fc1f9a04c3f52888840da908e50ab2aa29f166e912944a143de8e
  changed  libworklets.so	900632	d7b6832a87933318c638a37c43ff9d27033f6e22c6e3a1ff9c24b57b53895b93
        -> libworklets.so	900632	7d0a00ad7609ddf8a7455a3f7c73fc41a8a80ee4f0467b558f4167a83e632052

atoms.tsv
  added    1799	layerUrls
  added    1821	videoExpiryEverySecs
  added    1871	apiMemory
  added    1946	imageMaxAgeSecs
  added    2034	then
  added    2122	pixelSize
  added    2217	barLeft
  added    2274	modelMs
  added    2364	alwaysOnCaptions
  added    2397	copyOffset
  added    2633	copyLen
  added    2674	pieces
  added    2765	frame
  added    2804	presentMs
  added    2990	send_label
  added    2998	buttons
  added    3030	actionKinds
  added    3058	apiDisk
  added    3074	hostNowMs
  added    3130	barRight
  added    3155	ios
  added    3258	cdnHost
  added    3263	bodyLen
  added    3422	videoMaxAgeSecs

build.txt
  added    version-name	357.1 - Alpha
  added    version-code	357201
  removed  version-name	357.0 - Alpha
  removed  version-code	357200
  changed  apk	base	discord-357200-base.apk	sha256:1f3876502a004bbc7533bd21cf6b724350b191d92d4e3eb907f0a80db7ee9922
        -> apk	base	discord-357201-base.apk	sha256:4c05eb19d087eb408b2e5f772349817d7333afc72f93ba8c1a1a111ee1480701
  changed  apk	config.arm64_v8a	discord-357200-config.arm64_v8a.apk	sha256:51b92e03be15e94bbd5c3fcda5f38a3adfed29b47d36cedcbcfbddb3f2575381
        -> apk	config.arm64_v8a	discord-357201-config.arm64_v8a.apk	sha256:2d37434a1e9f2850fc527024ff6f986c9be9560788a7ea912408e26450178860
  changed  apk	config.armeabi_v7a	discord-357200-config.armeabi_v7a.apk	sha256:3f862b5c14c1e3d8a162d7011ee11a4a34be173a14d0afd5fc640dfc7877a362
        -> apk	config.armeabi_v7a	discord-357201-config.armeabi_v7a.apk	sha256:63788fd5ea6cea663657041b1ccbd1e53dcacd35ed63bb827d5d6c9556719a5e
  changed  apk	config.x86	discord-357200-config.x86.apk	sha256:3edaf1027dad0034ae9eef5de1de7ad4b85ae2aea2e1ee4c0103aedb1521ef91
        -> apk	config.x86	discord-357201-config.x86.apk	sha256:2ae803c3170479b1e8a34bcbf8e7ddecc2bb140da38b648d7c764d63524c33c8
  changed  apk	config.x86_64	discord-357200-config.x86_64.apk	sha256:a72f862486a0f0b7b0b0a15b2eca9b90ac204f2df370d949cdb841cb2c37510a
        -> apk	config.x86_64	discord-357201-config.x86_64.apk	sha256:ec963a886ad54d8bb5bcba5d6c6f703a4731548af1f1c22229c926329d445784

drawables.tsv
  added    _node_modules_pnpm_reactnavigationelements2934_uvkordladmmn2jfdjahig4vaii_node_modules_reactnavigation_elements_lib_module_assets_backiconmask	mdpi	png
  added    slider_track	-	layer-list
  added    slider_track_shape	-	selector
  removed  _node_modules_pnpm_reactnavigationelements2934_shb2al3n4oohkkhnm35rfpv56i_node_modules_reactnavigation_elements_lib_module_assets_backiconmask	mdpi	png
  removed  ic_mana_a	-	vector
  removed  ic_mana_activities_plus	-	vector
  removed  ic_mana_airplay	-	vector
  removed  ic_mana_angle_brackets	-	vector
  removed  ic_mana_announcements_chat	-	vector
  removed  ic_mana_announcements_web	-	vector
  removed  ic_mana_apple_brand_light	-	vector
  removed  ic_mana_arrow_angle_down_left	-	vector
  removed  ic_mana_arrow_angle_left_down	-	vector
  removed  ic_mana_arrow_angle_right_down	-	vector
  removed  ic_mana_arrow_angle_up_left	-	vector
  removed  ic_mana_assist	-	vector
  removed  ic_mana_asterisk	-	vector
  removed  ic_mana_b	-	vector
  removed  ic_mana_bank	-	vector
  removed  ic_mana_battlenet_brand	-	vector
  removed  ic_mana_bluesky_brand	-	vector
  removed  ic_mana_bluetooth	-	vector
  removed  ic_mana_bold	-	vector
  removed  ic_mana_book	-	vector
  removed  ic_mana_boost_tier1_simple	-	vector
  removed  ic_mana_boost_tier2_simple	-	vector
  removed  ic_mana_boost_tier3_simple	-	vector
  removed  ic_mana_browser	-	vector
  removed  ic_mana_browser_checkered	-	vector
  removed  ic_mana_browser_link	-	vector
  removed  ic_mana_browser_plus	-	vector
  removed  ic_mana_browser_question_mark	-	vector
  removed  ic_mana_calendar_retry	-	vector
  removed  ic_mana_calendar_x	-	vector
  removed  ic_mana_camera_swap	-	vector
  removed  ic_mana_candy	-	vector
  removed  ic_mana_channel_list_minus	-	vector
  removed  ic_mana_channel_list_retry	-	vector
  removed  ic_mana_chat_eye	-	vector
  removed  ic_mana_chat_minus	-	vector
  removed  ic_mana_chat_notification	-	vector
  removed  ic_mana_chat_notification__secondary	-	vector
  removed  ic_mana_chat_retry	-	vector
  removed  ic_mana_chat_slow_mode	-	vector
  removed  ic_mana_chat_speak	-	vector
  removed  ic_mana_clapperboard	-	vector
  removed  ic_mana_clips_auto	-	vector
  removed  ic_mana_clips_automontage	-	vector
  removed  ic_mana_clips_gallery	-	vector
  removed  ic_mana_cloud_upload	-	vector
  removed  ic_mana_collapse_list	-	vector
  removed  ic_mana_collection	-	vector
  removed  ic_mana_contacts	-	vector
  removed  ic_mana_crop	-	vector
  removed  ic_mana_crunchyroll_brand_light	-	vector
  removed  ic_mana_door_enter	-	vector
  removed  ic_mana_double_chevron_small_left	-	vector
  removed  ic_mana_dpad	-	vector
  removed  ic_mana_dying_rose	-	vector
  removed  ic_mana_emo	-	vector
  removed  ic_mana_emoji_anguished_face	-	vector
  removed  ic_mana_emoji_astonished_face	-	vector
  removed  ic_mana_emoji_blase_face	-	vector
  removed  ic_mana_emoji_confounded_face	-	vector
  removed  ic_mana_emoji_confused_face	-	vector
  removed  ic_mana_emoji_deadpan_face	-	vector
  removed  ic_mana_emoji_disappointed_face	-	vector
  removed  ic_mana_emoji_dotted_line_face	-	vector
  removed  ic_mana_emoji_elated_face	-	vector
  removed  ic_mana_emoji_enraged_face	-	vector
  removed  ic_mana_emoji_expressionless_face	-	vector
  removed  ic_mana_emoji_face_blowing_a_kiss	-	vector
  removed  ic_mana_emoji_face_savoring_food	-	vector
  removed  ic_mana_emoji_face_with_crossed_out_eyes	-	vector
  removed  ic_mana_emoji_face_with_diagonal_mouth	-	vector
  removed  ic_mana_emoji_face_with_head_bandage	-	vector
  removed  ic_mana_emoji_face_with_medical_mask	-	vector
  removed  ic_mana_emoji_face_with_open_mouth	-	vector
  removed  ic_mana_emoji_face_with_raised_eyebrow	-	vector
  removed  ic_mana_emoji_face_with_tears_of_joy	-	vector
  removed  ic_mana_emoji_face_with_tongue	-	vector
  removed  ic_mana_emoji_face_without_mouth	-	vector
  removed  ic_mana_emoji_frowning_face_with_open_mouth	-	vector
  removed  ic_mana_emoji_grimacing_face	-	vector
  removed  ic_mana_emoji_grinning_face	-	vector
  removed  ic_mana_emoji_grinning_face_with_big_eyes	-	vector
  removed  ic_mana_emoji_grinning_face_with_smiling_eyes	-	vector
  removed  ic_mana_emoji_grinning_face_with_sweat	-	vector
  removed  ic_mana_emoji_grumpy_face	-	vector
  removed  ic_mana_emoji_happy_winking_face	-	vector
  removed  ic_mana_emoji_hot_face	-	vector
  removed  ic_mana_emoji_joking_face	-	vector
  removed  ic_mana_emoji_kissing_face	-	vector
  removed  ic_mana_emoji_kissing_face_with_closed_eyes	-	vector
  removed  ic_mana_emoji_nauseated_face	-	vector
  removed  ic_mana_emoji_neutral_face	-	vector
  removed  ic_mana_emoji_people	-	vector
  removed  ic_mana_emoji_persevering_face	-	vector
  removed  ic_mana_emoji_relieved_face	-	vector
  removed  ic_mana_emoji_sad_face_with_crossed_out_eyes	-	vector
  removed  ic_mana_emoji_sleeping_face	-	vector
  removed  ic_mana_emoji_slightly_frowning_face	-	vector
  removed  ic_mana_emoji_smiling_face_with_halo	-	vector
  removed  ic_mana_emoji_smiling_face_with_smiling_eyes	-	vector
  removed  ic_mana_emoji_smiling_face_with_tear	-	vector
  removed  ic_mana_emoji_smirking_face	-	vector
  removed  ic_mana_emoji_sneezing_face	-	vector
  removed  ic_mana_emoji_tired_face	-	vector
  removed  ic_mana_emoji_unamused_face	-	vector
  removed  ic_mana_emoji_weary_face	-	vector
  removed  ic_mana_emoji_winking_face	-	vector
  removed  ic_mana_emoji_winking_face_with_tongue	-	vector
  removed  ic_mana_emoji_worried_face	-	vector
  removed  ic_mana_epic_games_brand_dark	-	vector
  removed  ic_mana_expand_gif	-	vector
  removed  ic_mana_experimental_banner	-	vector
  removed  ic_mana_experimental_banner_plus	-	vector
  removed  ic_mana_experimental_confetti	-	vector
  removed  ic_mana_experimental_couch	-	vector
  removed  ic_mana_experimental_create_emoji	-	vector
  removed  ic_mana_experimental_graph_major_negative	-	vector
  removed  ic_mana_experimental_graph_minor	-	vector
  removed  ic_mana_experimental_graph_minor__secondary	-	vector
  removed  ic_mana_experimental_graph_moderate	-	vector
  removed  ic_mana_experimental_graph_moderate__secondary	-	vector
  removed  ic_mana_experimental_lootbox	-	vector
  removed  ic_mana_experimental_microphone_sparkle	-	vector
  removed  ic_mana_experimental_microphone_sparkle_muted	-	vector
  removed  ic_mana_experimental_microphone_speaking	-	vector
  removed  ic_mana_experimental_microphone_speaking__secondary	-	vector
  removed  ic_mana_experimental_pineapple_house	-	vector
  removed  ic_mana_experimental_snowflake	-	vector
  removed  ic_mana_eye_plus	-	vector
  removed  ic_mana_fandom_brand	-	vector
  removed  ic_mana_fandom_brand__secondary	-	vector
  removed  ic_mana_file_deny	-	vector
  removed  ic_mana_filter	-	vector
  removed  ic_mana_flag_minus	-	vector
  removed  ic_mana_flag_plus	-	vector
  removed  ic_mana_flag_retry	-	vector
  removed  ic_mana_flip_horizontal	-	vector
  removed  ic_mana_flip_vertical	-	vector
  removed  ic_mana_fullscreen_exit	-	vector
  removed  ic_mana_goal	-	vector
  removed  ic_mana_google_play_brand	-	vector
  removed  ic_mana_google_play_brand__quaternary	-	vector
  removed  ic_mana_google_play_brand__secondary	-	vector
  removed  ic_mana_google_play_brand__tertiary	-	vector
  removed  ic_mana_grid_horizontal	-	vector
  removed  ic_mana_grid_vertical	-	vector
  removed  ic_mana_group_arrow_right	-	vector
  removed  ic_mana_group_minus	-	vector
  removed  ic_mana_group_retry	-	vector
  removed  ic_mana_hammer_minus	-	vector
  removed  ic_mana_hammer_plus	-	vector
  removed  ic_mana_hammer_retry	-	vector
  removed  ic_mana_hammer_x	-	vector
  removed  ic_mana_hd	-	vector
  removed  ic_mana_home_slash	-	vector
  removed  ic_mana_image_file_up	-	vector
  removed  ic_mana_image_spoiler	-	vector
  removed  ic_mana_italic	-	vector
  removed  ic_mana_itch_brand	-	vector
  removed  ic_mana_joystick	-	vector
  removed  ic_mana_laptop	-	vector
  removed  ic_mana_league_of_legends_brand	-	vector
  removed  ic_mana_linkshell	-	vector
  removed  ic_mana_magnifying_glass_minus	-	vector
  removed  ic_mana_magnifying_glass_plus	-	vector
  removed  ic_mana_mana	-	vector
  removed  ic_mana_mastodon_brand	-	vector
  removed  ic_mana_microphone_warning	-	vector
  removed  ic_mana_minecraft_brand	-	vector
  removed  ic_mana_minecraft_brand__quaternary	-	vector
  removed  ic_mana_minecraft_brand__secondary	-	vector
  removed  ic_mana_minecraft_brand__tertiary	-	vector
  removed  ic_mana_minimize	-	vector
  removed  ic_mana_minus	-	vector
  removed  ic_mana_mobile_phone_controller	-	vector
  removed  ic_mana_mobile_phone_plus	-	vector
  removed  ic_mana_mobile_phone_speaker	-	vector
  removed  ic_mana_mobile_phone_video	-	vector
  removed  ic_mana_music_album	-	vector
  removed  ic_mana_music_artist	-	vector
  removed  ic_mana_nearby_scan	-	vector
  removed  ic_mana_new_user_simple	-	vector
  removed  ic_mana_paintbrush_thick	-	vector
  removed  ic_mana_paintbrush_thick_minus	-	vector
  removed  ic_mana_paintbrush_thick_plus	-	vector
  removed  ic_mana_paintbrush_thick_retry	-	vector
  removed  ic_mana_paintbrush_thin_minus	-	vector
  removed  ic_mana_paintbrush_thin_plus	-	vector
  removed  ic_mana_paintbrush_thin_retry	-	vector
  removed  ic_mana_panel_closed	-	vector
  removed  ic_mana_panel_open	-	vector
  removed  ic_mana_paper_clock	-	vector
  removed  ic_mana_paper_lock	-	vector
  removed  ic_mana_pin_upright	-	vector
  removed  ic_mana_plane	-	vector
  removed  ic_mana_plane_travel	-	vector
  removed  ic_mana_playback_off	-	vector
  removed  ic_mana_playback_on	-	vector
  removed  ic_mana_potion	-	vector
  removed  ic_mana_privacy_and_safety	-	vector
  removed  ic_mana_puzzle_piece_minus	-	vector
  removed  ic_mana_puzzle_piece_plus	-	vector
  removed  ic_mana_puzzle_piece_retry	-	vector
  removed  ic_mana_quests_arena	-	vector
  removed  ic_mana_quests_bounties	-	vector
  removed  ic_mana_quests_missions	-	vector
  removed  ic_mana_quests_notification	-	vector
  removed  ic_mana_quests_notification__secondary	-	vector
  removed  ic_mana_reaction_minus	-	vector
  removed  ic_mana_reaction_plus	-	vector
  removed  ic_mana_receipt	-	vector
  removed  ic_mana_remix	-	vector
  removed  ic_mana_remove_reaction	-	vector
  removed  ic_mana_riot_games_brand	-	vector
  removed  ic_mana_roblox_brand_dark	-	vector
  removed  ic_mana_rotate	-	vector
  removed  ic_mana_screen_deny	-	vector
  removed  ic_mana_screen_slash	-	vector
  removed  ic_mana_screen_system_requirements	-	vector
  removed  ic_mana_settings_arrow_up	-	vector
  removed  ic_mana_settings_circle	-	vector
  removed  ic_mana_settings_plus	-	vector
  removed  ic_mana_shield_at	-	vector
  removed  ic_mana_shop_circle	-	vector
  removed  ic_mana_shop_minus	-	vector
  removed  ic_mana_shop_plus	-	vector
  removed  ic_mana_shop_sparkle	-	vector
  removed  ic_mana_skip_backward	-	vector
  removed  ic_mana_skip_forward	-	vector
  removed  ic_mana_skull	-	vector
  removed  ic_mana_slash_minus	-	vector
  removed  ic_mana_slash_plus	-	vector
  removed  ic_mana_slash_retry	-	vector
  removed  ic_mana_soundboard_deny	-	vector
  removed  ic_mana_spotify_brand	-	vector
  removed  ic_mana_stage_list	-	vector
  removed  ic_mana_stage_minus	-	vector
  removed  ic_mana_stage_plus	-	vector
  removed  ic_mana_stage_retry	-	vector
  removed  ic_mana_stage_spoiler	-	vector
  removed  ic_mana_stage_warning	-	vector
  removed  ic_mana_stage_x	-	vector
  removed  ic_mana_star_shooting	-	vector
  removed  ic_mana_steam_brand_dark	-	vector
  removed  ic_mana_steam_brand_light	-	vector
  removed  ic_mana_sticker_dead	-	vector
  removed  ic_mana_sticker_minus	-	vector
  removed  ic_mana_sticker_retry	-	vector
  removed  ic_mana_sticker_sad	-	vector
  removed  ic_mana_sticker_small	-	vector
  removed  ic_mana_sticker_wink1	-	vector
  removed  ic_mana_sticker_wink2	-	vector
  removed  ic_mana_strikethrough	-	vector
  removed  ic_mana_text_user	-	vector
  removed  ic_mana_thread_retry	-	vector
  removed  ic_mana_thread_spoiler	-	vector
  removed  ic_mana_thread_warning	-	vector
  removed  ic_mana_transcript	-	vector
  removed  ic_mana_underline	-	vector
  removed  ic_mana_user_arrow_diagonal_bottom_right	-	vector
  removed  ic_mana_user_circle_status	-	vector
  removed  ic_mana_user_play	-	vector
  removed  ic_mana_user_retry	-	vector
  removed  ic_mana_user_status	-	vector
  removed  ic_mana_user_warning	-	vector
  removed  ic_mana_vein	-	vector
  removed  ic_mana_video_lock	-	vector
  removed  ic_mana_view_reaction	-	vector
  removed  ic_mana_voice_bluetooth	-	vector
  removed  ic_mana_watering_can	-	vector
  removed  ic_mana_widgets_minus	-	vector
  removed  ic_mana_widgets_plus	-	vector
  removed  ic_mana_widgets_retry	-	vector
  removed  ic_mana_window_return	-	vector
  removed  ic_mana_window_top_outline	-	vector
  removed  ic_mana_x_xsmall	-	vector
  removed  ic_mana_x_xsmall_bold	-	vector
  changed  ic_mana_headphones	-	vector
        -> ic_mana_headphones	-	reference
  changed  ic_mana_headphones_slash	-	vector
        -> ic_mana_headphones_slash	-	reference
  changed  ic_mana_microphone	-	vector
        -> ic_mana_microphone	-	reference
  changed  ic_mana_microphone_slash	-	vector
        -> ic_mana_microphone_slash	-	reference
  changed  ic_mana_video	-	vector
        -> ic_mana_video	-	reference
  changed  ic_mana_video_slash	-	vector
        -> ic_mana_video_slash	-	reference
  changed  ic_mana_x_small	-	vector
        -> ic_mana_x_small	-	reference

events.txt
  added    2592	@alwaysOnCaptions
  added    2957	@checkpointCharacterImage
  added    3534	@sideBars
  added    3564	@spliced

experiments.txt
  added    2026-09-edit-profile-collectibles-ordering	host
  added    2026-09-mobile-nitro-upsell-in-shop-pdp	host
  added    2026-10-mobile-image-load-metrics	bundle
  added    2026-10-orb-void	host
  added    2026-11-ad-refresh-immediate-on-focus	bundle,host
  added    2026-11-badge-social-comparison-mobile	bundle
  added    2026-11-game-stats-widget-skip-connect-modal	host
  added    2026-11-mobile-did-background-app-native	bundle,host
  added    2026-11-mobile-quest-bar-closed-state	bundle,host
  added    2026-11-norbs	host
  added    2026-11-norbs-2	host
  added    2026-11-premium-group-continuation-40	host
  added    2026-11-profile-edit-sheet-nitro-updates	bundle,host
  added    2026-11-quest-home-hero-shared-ad-refresh	bundle,host
  added    2026-11-stream-drawing	bundle,host
  added    2026-11-stream-drawing-guild	bundle,host
  added    2026-11-user-profile-mobile-editing-refresh	bundle,host
  added    2026-11-voice-dtx-forward-all	host
  added    2026-11-voicemod-3p	host
  added    2026-11-voicemod-non-sub-marketing	host
  removed  2025-05-search-results-feedback	bundle,host
  removed  2025-11-defer-load-late-lazy-cache	bundle
  removed  2026-08-find-coded-links-regex	bundle,host
  removed  2026-09-edit-profile-collectibles-ordering	bundle,host
  removed  2026-09-mobile-nitro-upsell-in-shop-pdp	bundle,host
  removed  2026-11-ad-refresh-immediate-on-focus	bundle
  removed  2026-11-dtx-forward-all-kill	host
  removed  2026-11-mobile-did-background-app-native	bundle
  removed  2026-11-profile-edit-sheet-nitro-updates	bundle
  removed  2026-11-stream-drawing	host

exports.txt
  added    Java_com_discord_nativeapp_modules_RustLottie_nativeClose
  added    Java_com_discord_nativeapp_modules_RustLottie_nativeDraw
  added    Java_com_discord_nativeapp_modules_RustLottie_nativeEmbedded
  added    Java_com_discord_nativeapp_modules_RustLottie_nativeEmbeddedBytes
  added    Java_com_discord_nativeapp_modules_RustLottie_nativeImage
  added    Java_com_discord_nativeapp_modules_RustLottie_nativeLook
  added    Java_com_discord_nativeapp_modules_RustLottie_nativeOpen
  added    Java_com_discord_nativeapp_modules_RustLottie_nativeSetEmbedded
  added    Java_com_discord_nativeapp_modules_RustStickerFrames_nativeClose
  added    Java_com_discord_nativeapp_modules_RustStickerFrames_nativeDrawBitmap
  added    Java_com_discord_nativeapp_modules_RustStickerFrames_nativeOpen
  added    Java_com_discord_nativeapp_modules_RustStickerFrames_nativeSetBudget
  added    Java_com_discord_nativeapp_modules_RustStickerFrames_nativeTiming
  added    ldh_lottie_close
  added    ldh_lottie_draw
  added    ldh_lottie_embedded_at
  added    ldh_lottie_embedded_count
  added    ldh_lottie_image
  added    ldh_lottie_look
  added    ldh_lottie_open
  added    ldh_lottie_set_embedded
  added    ldh_sticker_close
  added    ldh_sticker_draw
  added    ldh_sticker_forget
  added    ldh_sticker_open
  added    ldh_sticker_timing

first-party-crates.txt
  added    lottie
  added    net-seam
  added    sticker-frames
  added    wasm-app-kit

guest-modules.txt
  added    wasm-app-kit

host-calls.txt
  added    1580	CheckpointCharacterImage.share
  added    2049	MediaPicker.splice
  added    2721	CheckpointCharacterImage
  added    3369	CheckpointCharacterImage.write
  added    3545	CheckpointCharacterImage.save

propid-types.tsv
  added    871	focusWithoutKeyboard	Bool	k9.e
  added    872	textRounding	Bool	k9.e
  added    873	fitFontSize	Bool	mh.r2
  added    874	disableTextTracks	Bool	mh.m1
  added    875	spaceWidth	key:Any	com.discord.nativeapp.modules.props.b
  added    876	accessibilityTapUnmarked	Bool	k9.e
  added    877	inkCentred	Bool	mh.r2
  added    878	linkPressLook	key:String	mh.o1
  added    879	linkHoldless	-	unread
  added    880	inTree	-	unread
  added    881	passBack	-	unread
  added    882	popoverLayer	Bool	k9.e
  added    883	inLayer	-	unread
  added    884	caretBottom	-	unread
  added    885	stickyHeader	Bool	k9.e
  added    886	thumbImage	String	k9.e
  added    887	thumbPressedSize	Number	k9.e
  added    888	bgHeight	-	unread
  added    889	bgLabelScale	-	unread
  added    890	borderOffGrid	-	unread
  added    891	gridOrigin	-	unread
  added    892	statusBarSystem	-	unread
  added    893	stopInBackground	-	unread
  added    894	onTint	-	unread
  added    895	flips	-	unread
  added    896	linkBackdrop	-	unread
  changed  213	from	key:Int/key:Any -> key:Int
  changed  356	placeholderPool	String -> -
  changed  366	pool	String/key:Any -> -
  changed  524	to	key:Int/key:Any -> key:Int
  changed  687	all	key:Any -> -
  376 props read by other classes (jadx names; usually renaming)

propids.tsv
  added    871	focusWithoutKeyboard
  added    872	textRounding
  added    873	fitFontSize
  added    874	disableTextTracks
  added    875	spaceWidth
  added    876	accessibilityTapUnmarked
  added    877	inkCentred
  added    878	linkPressLook
  added    879	linkHoldless
  added    880	inTree
  added    881	passBack
  added    882	popoverLayer
  added    883	inLayer
  added    884	caretBottom
  added    885	stickyHeader
  added    886	thumbImage
  added    887	thumbPressedSize
  added    888	bgHeight
  added    889	bgLabelScale
  added    890	borderOffGrid
  added    891	gridOrigin
  added    892	statusBarSystem
  added    893	stopInBackground
  added    894	onTint
  added    895	flips
  added    896	linkBackdrop

wire.txt
  added    propid-count	897	-	extracted	the host's PropId table and the platform's name array
  removed  propid-count	871	-	extracted	the host's PropId table and the platform's name array
  changed  turn-op	10	childEdits	spec	code: the platform decoder's switch; name: manual (a "childEdits ..." error string exists)
        -> turn-op	10	childEdits	extracted	code: the platform decoder's switch; name: the platform's op-name array
```

## android 357200

357.0 - Alpha, libdiscord unchanged. The wire format, kinds, models and
exports' C ABI shape are unchanged. 16 PropIds are appended (855 to 870),
and no existing id moved. 21 of the 45 arm64-v8a libraries changed; the
host grew by 1.3 MB. `resvg`/`usvg` 0.46 to 0.50 and `tiny-skia` 0.11 to
0.12 in the host, and `prost` 0.14.5 is new. The motion engine's
rows-committed/rows-settled callbacks are gone. `Updates.verify`,
`Updates.rootPath` and `Ota.verify` are new host methods.

4 drawables are new (862 to 866 entries), none of them an `ic_mana_*`
icon. The platform reads 404 of 871 PropIds. Of the 16 new PropIds it
reads 4, and `selectionColor` gained a Number handler. Gateway events,
reducers and cache tables are unchanged.

```
atoms.tsv
  added    1542	notificationClient
  added    1627	paymentMode
  added    1708	mediaEngineStore
  added    1732	loadFailureUrl
  added    1750	mmkvToken
  added    1840	types
  added    1881	notificationSettings
  added    1920	jankStatsExpectedMs
  added    2021	successes
  added    2233	discounts
  added    2349	inAppMessageSounds
  added    2504	uiFontMetricsSizes
  added    2658	selectedBrowser
  added    2761	jankStatsMs
  added    2795	requestData
  added    2819	mobileVoiceOverlayStore
  added    2828	verification
  added    2869	currencySymbol
  added    2879	localizedPrice
  added    3001	conversationSuggestions
  added    3071	valid
  added    3095	subscriptionPeriod
  added    3098	accessibilityStore
  added    3136	noLogin
  added    3426	localCopy
  added    3434	titleMinRoom
  added    3478	applied
  added    3483	numberOfPeriods

drawables.tsv
  added    design_components_slider_native_images_sliderthumbdark	mdpi	png
  added    design_components_slider_native_images_sliderthumblight	mdpi	png
  added    rn_notif_preview_voice	-	reference
  added    splash_dark	-	layer-list

events.txt
  added    3002	@appIconCurrent

experiments.txt
  added    2025-08-animated-keyboard-android	bundle
  added    2025-12-windows-audio-effects	bundle,host
  removed  2025-08-animated-keyboard-android	bundle,host
  removed  2025-12-windows-audio-effects	bundle

exports.txt
  added    dme_mobile_host_guest_event_routed
  removed  Java_com_discord_nativeapp_motion_MotionNative_nativeRowsCommitted
  removed  Java_com_discord_nativeapp_motion_MotionNative_nativeRowsSettled
  removed  ldh_motion_rows_committed
  removed  ldh_motion_rows_settled

host-calls.txt
  added    1639	Updates.verify
  added    2167	Updates.rootPath
  added    3462	Ota.verify

propid-types.tsv
  added    855	measureFontPadding	Bool	lh.a
  added    856	topBarShown	Number	lh.a
  added    857	expandedRest	-	unread
  added    858	scrollOffsetLayout	Bool	lh.a
  added    859	roundEachLine	-	unread
  added    860	sheetKeyboardCovers	-	unread
  added    861	firstTop	-	unread
  added    862	user	-	unread
  added    863	closeAtOnce	-	unread
  added    864	borderCurve	-	unread
  added    865	openSpring	-	unread
  added    866	below	key:Double	n7.i
  added    867	linkLongPressEnd	-	unread
  added    868	sheetOpenAtLayout	-	unread
  added    869	drawLineHeight	-	unread
  added    870	uiFontMetrics	-	unread
  changed  844	selectionColor	- -> Number
  342 props read by other classes (jadx names; usually renaming)

propids.tsv
  added    855	measureFontPadding
  added    856	topBarShown
  added    857	expandedRest
  added    858	scrollOffsetLayout
  added    859	roundEachLine
  added    860	sheetKeyboardCovers
  added    861	firstTop
  added    862	user
  added    863	closeAtOnce
  added    864	borderCurve
  added    865	openSpring
  added    866	below
  added    867	linkLongPressEnd
  added    868	sheetOpenAtLayout
  added    869	drawLineHeight
  added    870	uiFontMetrics

wire.txt
  added    propid-count	871	-	extracted	the host's PropId table and the platform's name array
  removed  propid-count	855	-	extracted	the host's PropId table and the platform's name array
abi/arm64-v8a/crates.txt
  added    imagesize@0.15.0
  added    prost@0.14.5
  added    resvg@0.50.0
  added    tiny-skia-path@0.12.0
  added    tiny-skia@0.12.0
  added    usvg@0.50.0
  removed  imagesize@0.14.0
  removed  resvg@0.46.0
  removed  tiny-skia-path@0.11.4
  removed  tiny-skia@0.11.4
  removed  usvg@0.46.0

```

## android 356207

356.7 - Alpha, libdiscord 90.0.42-dave-pairwise-fingerprint. The baseline:
every table starts here. The host registers 89 gateway events and 86
reducers in 32 domains, and its cache store has 23 tables. The base APK
has 862 drawables, 286 of them `ic_mana_*`. The platform reads 399 of the
855 PropIds.
