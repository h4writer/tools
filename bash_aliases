#
# To install: ln -s $(pwd)/bash_aliases ~/.bash_aliases
#

BUILD=$HOME"/"Build 

# Use this alias to reload the definitions upon making changes.
alias alias_reload='source $HOME/.bash_aliases'

# Notify something is done.
alias alert='notify-send --urgency=low -i "$([ $? = 0 ] && echo terminal || echo error)" "$(history|tail -n1|sed -e '\''s/^\s*[0-9]\+\s*//;s/[;&|]\s*alert$//'\'')"'
alias notify='echo "$(history|tail -n1|sed -e '\''s/^\s*[0-9]\+\s*//;s/[;&|]\s*notify$//'\'')" >> /tmp/alert'
#TODO; put token in config file!
alias notify='curl --data "$(history|tail -n1|sed -e '\''s/^\s*[0-9]\+\s*//;s/[;&|]\s*notify$//'\'')" $"https://uwsoftware.slack.com/services/hooks/slackbot?token=XXXXXXXXXXXXX&channel=%23h4writer-compiler"'

# Engines
alias js='$JS/dist/bin/js'
alias d8='$BUILD/v8/out/ia32.release/d8'

# Benchmarks
alias kraken='cd $BUILD/kraken'
alias octane='cd $BUILD/octane2.0'
alias ss='cd $BUILD/SunSpider'

#Tools
alias m='make -s -C $JS -j8 2>&1 | grep -iE "error|$"; alert "Compilation done"'
alias m='make -s -C $JS -j8 2>&1 | grep -iE "error|$"; notify "Compilation done"'
alias mb='cd $REPO; ./mach build; notify "Compilation done"'
alias val='valgrind --tool=cachegrind'
alias try='hg push -f ssh://hg.mozilla.org/try' 
alias untry='hg phase -f --draft qbase:tip'

REPO=$BUILD"/mozilla-inbound"
alias inbound='cd '$REPO'/js/src'
alias inbound32='        export JS="'$REPO'/js/src/build-32";                   export MOZCONFIG=mozconfig-fast;'
alias inbound32d='       export JS="'$REPO'/js/src/build-32-debug";             export MOZCONFIG=mozconfig-debug;'
alias inbound32p='       export JS="'$REPO'/js/src/build-32-parallel";          export MOZCONFIG=mozconfig-fast;'
alias inbound32do='      export JS="'$REPO'/js/src/build-32-debug-opt";         export MOZCONFIG=mozconfig-debug;'
alias inbound64='        export JS="'$REPO'/js/src/build-64";                   export MOZCONFIG=none;'
alias inbound64d='       export JS="'$REPO'/js/src/build-64-debug";             export MOZCONFIG=none;'
alias inbound64p='       export JS="'$REPO'/js/src/build-64-parallel";          export MOZCONFIG=none;'
alias inbound64do='      export JS="'$REPO'/js/src/build-64-debug-opt";         export MOZCONFIG=none;'
alias inboundTL='        export JS="'$REPO'/js/src/build-tracelogging";         export MOZCONFIG=none;'
alias inboundTLGGC='     export JS="'$REPO'/js/src/build-tracelogging-ggc";     export MOZCONFIG=none;'
alias inboundARM='       export JS="'$REPO'/js/src/build-arm";                  export MOZCONFIG=none;'
alias inboundARMd='      export JS="'$REPO'/js/src/build-arm-debug";            export MOZCONFIG=none;'
alias inboundARMdo='     export JS="'$REPO'/js/src/build-arm-debug-opt";        export MOZCONFIG=none;'
alias inboundBook='      export JS="'$REPO'/js/src/build-book";                 export MOZCONFIG=none;'
alias inboundBookd='     export JS="'$REPO'/js/src/build-book-debug";           export MOZCONFIG=none;'
alias inboundBookdo='    export JS="'$REPO'/js/src/build-book-debug-opt";       export MOZCONFIG=none;'
alias inboundSoftBook='  export JS="'$REPO'/js/src/build-soft-book";            export MOZCONFIG=none;'
alias inboundSoftBookd=' export JS="'$REPO'/js/src/build-soft-book-debug";      export MOZCONFIG=none;'
alias inboundSoftBookdo='export JS="'$REPO'/js/src/build-soft-book-debug-opt";  export MOZCONFIG=none;'

BUILD32CC='CC="gcc -m32" CXX="g++ -m32" AR=ar'
BUILD32='--target=i686-pc-linux-gnu'
NSPRPUB32=$REPO'/nsprpub/build-32/dist/'
NSPRPUB64=$REPO'/nsprpub/build-64/dist/'
NSPRPUBBOOK=$REPO'/nsprpub/build-book/dist/'
NSPR32='--enable-threadsafe --with-nspr-cflags="-I'$NSPRPUB32'/include/nspr" --with-nspr-libs="'$NSPRPUB32'/lib/libnspr4.a '$NSPRPUB32'/lib/libplc4.a '$NSPRPUB32'/lib/libplds4.a"'
NSPR64='--enable-threadsafe --with-nspr-cflags="-I'$NSPRPUB64'/include/nspr" --with-nspr-libs="'$NSPRPUB64'/lib/libnspr4.a '$NSPRPUB64'/lib/libplc4.a '$NSPRPUB64'/lib/libplds4.a"'
NSPRBOOK='--enable-threadsafe --with-nspr-cflags="-I'$NSPRPUBBOOK'/include/nspr" --with-nspr-libs="'$NSPRPUBBOOK'/lib/libnspr4.a '$NSPRPUBBOOK'/lib/libplc4.a '$NSPRPUBBOOK'/lib/libplds4.a"'
GGC='--enable-exact-rooting --enable-gcgenerational'
EXTRA='--disable-intl-api --without-intl-api'
NSPR32='--enable-build-nspr'

alias conf32='     cd $JS; '$BUILD32CC' ../configure '$BUILD32'           --disable-debug --enable-optimize  '$EXTRA
alias conf32d='    cd $JS; '$BUILD32CC' ../configure '$BUILD32' '$NSPR32' --enable-debug  --disable-optimize '$EXTRA
alias conf32p='    cd $JS; '$BUILD32CC' ../configure '$BUILD32' '$NSPR32' --disable-debug --enable-optimize  '$EXTRA
alias conf32do='   cd $JS; '$BUILD32CC' ../configure '$BUILD32' '$NSPR32' --enable-debug  --enable-optimize  '$EXTRA
alias conf32TL='   cd $JS; '$BUILD32CC' ../configure '$BUILD32' '$NSPR32' --disable-debug --enable-optimize  --enable-trace-logging '$EXTRA
alias conf32TLd='  cd $JS; '$BUILD32CC' ../configure '$BUILD32' '$NSPR32' --enable-debug  --disable-optimize --enable-trace-logging '$EXTRA
alias conf32TLdo=' cd $JS; '$BUILD32CC' ../configure '$BUILD32' '$NSPR32' --enable-debug  --enable-optimize  --enable-trace-logging '$EXTRA
alias conf32TLGGC='cd $JS; '$BUILD32CC' ../configure '$BUILD32' '$NSPR32' --disable-debug --enable-optimize  --enable-trace-logging '$GGC' '$EXTRA

alias conf64='     cd $JS; ../configure           --disable-debug --enable-optimize '$EXTRA
alias conf64d='    cd $JS; ../configure '$NSPR64' --enable-debug --disable-optimize '$EXTRA
alias conf64p='    cd $JS; ../configure '$NSPR64' --disable-debug --enable-optimize '$GGC' '$EXTRA
alias conf64do='   cd $JS; ../configure '$NSPR64' --enable-debug --enable-optimize  '$GGC' '$EXTRA
alias conf64TL='   cd $JS; ../configure '$NSPR64' --disable-debug --enable-optimize  --enable-trace-logging '$EXTRA
alias conf64TLGGC='cd $JS; ../configure '$NSPR64' --disable-debug --enable-optimize  --enable-trace-logging '$GGC' '$EXTRA

alias confClang='  cd $JS; CC="clang" CXX="clang++" ../configure --disable-debug --enable-optimize -Werror'

alias confBook=' cd $JS; ../configure '$NSPRBOOK' --disable-debug --enable-optimize --target=arm-linux-gnueabihf --with-arch=armv7-a --with-thumb --disable-intl-api --without-intl-api'
alias confBookd='cd $JS; ../configure '$NSPRBOOK' --enable-debug --disable-optimize --target=arm-linux-gnueabihf --with-arch=armv7-a --with-thumb --disable-intl-api --without-intl-api'
alias confSoftBook='cd $JS; ../configure --disable-debug --enable-optimize --target=arm-linux-gnueabi --with-arch=armv7-a --with-thumb --disable-intl-api -mfloat-abi=softfp'
alias confSoftBookd='cd $JS; CC="gcc -mfloat-abi=softfp" CXX="g++ -mfloat-abi=softfp" ../configure --enable-debug --disable-optimize --target=arm-linux-gnueabi --with-arch=armv7-a --with-thumb --disable-intl-api'
alias confARMd='cd $JS; ../configure --enable-debug --disable-optimize --target=arm-linux-gnueabi --with-arch=armv7-a --with-thumb --with-qemu-exe=/usr/bin/qemu-arm --with-cross-lib=/usr/arm-linux-gnueabi/lib --disable-intl-api'

alias confArmSim='     cd $JS; ../configure           --enable-simulator=arm --disable-debug --enable-optimize '$EXTRA
alias confArmSimd='    cd $JS; ../configure '$NSPR32' --enable-simulator=arm --enable-debug --disable-optimize '$EXTRA
alias confArmSimp='    cd $JS; ../configure '$NSPR32' --enable-simulator=arm --disable-debug --enable-optimize '$EXTRA
alias confArmSimdo='   cd $JS; ../configure '$NSPR32' --enable-simulator=arm --enable-debug --enable-optimize '$EXTRA


alias s='~/Build/stackato'

function setgov ()
{
    echo "$1" | sudo tee /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor 
}
