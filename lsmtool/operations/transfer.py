#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This operation implements transferring of patches from one sky model to another
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

import logging

logging.debug('Loading TRANSFER module.')


def run(step, parset, LSM):

    import numpy as np

    patchFile = parset.getString('.'.join(["LSMTool.Steps", step, "PatchFile"]), '' )
    outFile = parset.getString('.'.join(["LSMTool.Steps", step, "OutFile"]), '' )

    transfer(LSM, patchFile)

    # Write to outFile
    if outFile == '' or outFile is None:
        outFile = LSM._fileName
    LSM.writeFile(outFile, clobber=True)

    return 0


def transfer(LSM, patchFile):

    from .. import skymodel

    masterLSM = skymodel.SkyModel(patchFile)
    masterNames = masterLSM.getColValues('Name')
    masterPatchNames = masterLSM.getColValues('Patch')

    # Group LSM by source. This ensures that any sources not in the master
    # sky model are given a patch of their own
    LSM.group('single')
    names = LSM.getColValues('Name')
    patchNames = LSM.getColValues('Patch')

    for i, name in enumerate(names):
        if name in masterNames:
            indx = masterNames.tolist().index(name)
            patchNames[i] = masterPatchNames[indx]

    LSM.setColValues('Patch', patchNames)
