#!/usr/bin/env bash
service apache2 start
export T=$RANDOM
T=$RANDOM
echo $FLAG > /_$T
chmod 444 /_$T
export FLAG=not_flag
FLAG=not_flag
export T=$RANDOM
while test "1" = "1"
do
sleep 1000
done
/usr/bin/tail -f /dev/null
 