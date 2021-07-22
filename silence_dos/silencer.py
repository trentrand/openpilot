#!/usr/bin/env python3
import os

from common.basedir import BASEDIR
from silence_dos.pandaext import PandaExtended

PANDA_KILL_FW_FN = os.path.join(BASEDIR, "silence_dos", "silent_dos_panda.bin.signed")
PANDA_RESTORE_FW_FN = os.path.join(BASEDIR, "silence_dos", "panda.bin.signed")


def main() -> None:
  a = input("(k)ill or (r)estore?: ")
  if a == "k":
    fn = PANDA_KILL_FW_FN
  else:
    fn = PANDA_RESTORE_FW_FN
  panda_list = PandaExtended.list()
  if len(panda_list) > 0:
    for tmp_panda in panda_list:
      panda = PandaExtended(tmp_panda)
      if panda.is_dos():
        panda.flash(fn=fn)
        panda.reset()


if __name__ == "__main__":
  main()
