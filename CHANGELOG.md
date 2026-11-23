# Changelog

Each entry is `python -I extract/diff.py <previous build> <this build>`.

## extractor: gateway, reducers, cache tables, drawables, prop types

Five new tables, written for 357200 and checked against 356207 with the
same extractor. On both builds the host registers 89 gateway events and
86 reducers in 32 domains, in the same order, and its cache store has 23
tables. Every ABI that ships the host agrees; armeabi-v7a has no cache
tables (see the README). 357200 adds four drawables (862 to 866 entries)
and no `ic_mana_*` icon (286 in both). The platform reads 399 of 855
PropIds in 356207 and 404 of 871 in 357200; of the 16 new PropIds it
reads 4, and `selectionColor` gained a Number handler.

```
drawables.tsv
  added    design_components_slider_native_images_sliderthumbdark	mdpi	png
  added    design_components_slider_native_images_sliderthumblight	mdpi	png
  added    rn_notif_preview_voice	-	reference
  added    splash_dark	-	layer-list

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
```

## android 357200

357.0 - Alpha, libdiscord unchanged. The wire format, kinds, models and
exports' C ABI shape are unchanged. 16 PropIds are appended (855 to 870),
and no existing id moved. 21 of the 45 arm64-v8a libraries changed; the
host grew by 1.3 MB. `resvg`/`usvg` 0.46 to 0.50 and `tiny-skia` 0.11 to
0.12 in the host, and `prost` 0.14.5 is new. The motion engine's
rows-committed/rows-settled callbacks are gone. `Updates.verify`,
`Updates.rootPath` and `Ota.verify` are new host methods.

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
every table starts here.
