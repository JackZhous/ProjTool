#!/bin/bash
#shell工作内容 解包 合包 并且改变其debug模式

apkfile=$(readlink -f $1)

bname=$(basename "$apkfile")
outdir=${bname%.apk}_debug
outfile=${bname/.apk/-debug.apk}

tmpdir=$(mktemp -d --suffix _apkdebug)
pushd .
cd $tmpdir

apktool d -d "$apkfile" -o "$outdir"

sed -ri 's#android:debuggable="(true|false)"##g;s#<application #&android:debuggable="true" #' $outdir/AndroidManifest.xml
sed -ri 's#<meta-data android:name="HJR_DATA_URL_DEBUG" android:value="false"#<meta-data android:name="HJR_DATA_URL_DEBUG" android:value="true"#g' $outdir/AndroidManifest.xml

apktool b -d $outdir -o "$outfile"

~/scripts/signer "$outfile"
popd
#cp $tmpdir/$outfile .
echo $tmpdir

