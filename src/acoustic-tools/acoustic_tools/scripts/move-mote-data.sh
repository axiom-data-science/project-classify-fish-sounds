#!/bin/bash
# Move data to loc/sub-loc/yyyy/mm/dd
# Name for files are either:
# - <name>-<sub-source>_yyyy-mm-ddThh-mm-ss.wav for datasets with hierarchy in raw data
# - <src>_yyyy-mm-ddThh-mm-ss.wav for datasets without heirarchy
# bermuda processed from gdrive-data and not listed here
set -e

BIN=rename_training_set_files.py
OUT=../reorg-new

script_start=`date +%s`

# EXXON
SRC=exxon-template-tower
SUBSRC=exxon-tower
NAME=exxon
echo "Moving $SRC/$SUBSRC to $OUT/$SRC/$SUBSRC"
start=`date +%s`
python $BIN $SRC/$SUBSRC $OUT/$SRC/$SUBSRC $NAME-$SUBSRC &
end=`date +%s`
time=$((end-start))
#echo "- time: $time"

SUBSRC=navy-tower
echo "Moving $SRC/$SUBSRC to $OUT/$SRC/$SUBSRC"
start=`date +%s`
python $BIN $SRC/$SUBSRC $OUT/$SRC/$SUBSRC $NAME-$SUBSRC &
end=`date +%s`
time=$((end-start))
#echo "- time: $time"

# GOLIATH 
SRC=goliath-jupiter-gulf
NAME=goliath

SUBSRC=fantastico-gg-gulf
echo "Moving $SRC/$SUBSRC to $OUT/$SRC/$SUBSRC"
start=`date +%s`
python $BIN $SRC/$SUBSRC $OUT/$SRC/$SUBSRC $NAME-$SUBSRC &
end=`date +%s`
time=$((end-start))
#echo "- time: $time"

SUBSRC=jupiter
echo "Moving $SRC/$SUBSRC to $OUT/$SRC/$SUBSRC"
start=`date +%s`
# name different to distinguish with jupter below
python $BIN $SRC/$SUBSRC $OUT/$SRC/$SUBSRC $NAME-$SUBSRC &
end=`date +%s`
time=$((end-start))
#echo "- time: $time"

SUBSRC=stoney-gg-gom
echo "Moving $SRC/$SUBSRC to $OUT/$SRC/$SUBSRC"
start=`date +%s`
python $BIN $SRC/$SUBSRC $OUT/$SRC/$SUBSRC $NAME-$SUBSRC &
end=`date +%s`
time=$((end-start))
#echo "- time: $time"

# JUPITER
SRC=jupiter
NAME=jupiter
echo "Moving $SRC to $OUT/$SRC"
start=`date +%s`
python $BIN $SRC $OUT/$SRC $NAME &
end=`date +%s`
time=$((end-start))
#echo "- time: $time"

# PORT MANATEE
SRC=port-manatee
NAME=port-manatee
echo "Moving $SRC to $OUT/$SRC"
start=`date +%s`
python $BIN $SRC $OUT/$SRC $NAME &
end=`date +%s`
time=$((end-start))
#echo "- time: $time"

# PUERTO RICO 
# Uses a different format for files -> perhaps toshiba
# SRC=puerto-rico
# NAME=puerto-rico
# python $BIN $SRC $OUT/$SRC $NAME

# RILEYS HUMP 
SRC=rileys-hump
NAME=rileys-hump
echo "Moving $SRC to $OUT/$SRC"
start=`date +%s`
python $BIN $SRC $OUT/$SRC $NAME &
end=`date +%s`
time=$((end-start))
#echo "- time: $time"

# USF GLIDER 
SRC=usf-glider
NAME=usf-glider
echo "Moving $SRC to $OUT/$SRC"
start=`date +%s`
python $BIN $SRC $OUT/$SRC $NAME &
end=`date +%s`
time=$((end-start))
#echo "- time: $time"

wait
script_end=`date +%s`
script_time=$((script_end-script_start))
echo "Total time: $script_time"
