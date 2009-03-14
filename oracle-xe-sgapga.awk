#!/bin/awk -f
#
# Author: Pawel Zuzelski <pawelz@pld-linux.org>

function min(a, b) {return ((a < b)?a:b)}
function max(a, b) {return ((a > b)?a:b)}

BEGIN {
  sgamin=146800640
  pgamin=16777216
  sgamax=805306368
  pgamax=268435456
}

/^MemTotal:/ {
  mem=$2;
  tm=mem/1024*0.4;
  tmsp=mem/1024*0.4-40;
  sga=min(sgamin, 0.75*tmsp*1048576);
  pga=min(pgamin, 0.25*tmsp*1048576);
  if (sga + pga > sgamax + pgamax) {
    sga=max(sga, sgamax);
    pga=max(pga, pgamax);
  }
}

END {
  printf ("eval sga=%i\n", sga);
  printf ("eval pga=%i\n", pga);
}
