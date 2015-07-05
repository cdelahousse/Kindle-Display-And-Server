#!/bin/sh

SERVER=''
PORT=9876
PNG_FNAME=img.png
INDEX_FNAME=index
CUTOFF_NUMBER=1000

# Prevent the screen saver and the kindle shutdown
lipc-set-prop com.lab126.powerd preventScreenSaver 1
/etc/init.d/netwatchd stop

#Check for the existence of the file
if [ ! -e $INDEX_FNAME ];
then
        echo 'Creating index file'
        touch $INDEX_FNAME
        echo 0 > $INDEX_FNAME
fi

INDEX=`cat $INDEX_FNAME`

#Let's not let the number get too big
if [ $INDEX -gt $CUTOFF_NUMBER ];
then
        echo 'Resetting index'
        INDEX=0
fi

rm -f $PNG_FNAME
wget -O $PNG_FNAME $SERVER:$PORT/$INDEX
eips -c
eips -c
eips -g $PNG_FNAME

echo $((INDEX + 1)) > $INDEX_FNAME

