#! /bin/sh

egrep 'chap[0-9]|render time' $1 | grep -v help | grep -v hello | \
  awk '/python/{mode=$5;}/render time/{if(mode!=""){t=$(NF);sub(/[ \t\r\n]+$/, "", t);printf("| [%s](img/%s.png) | %.3f |\n",mode,mode,t); mode="";}}'
