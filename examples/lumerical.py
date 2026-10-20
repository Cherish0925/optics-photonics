import numpy as np
import lumapi

with lumapi.FDTD(hide=True) as sim:
    sim.load("device.fsp")
    sim.switchtolayout()
    sim.setnamed("core", "x span", 450e-9)
    sim.run()
    result = sim.getresult("transmission", "T")
    np.savez("result.npz",
             wavelength_m=result["lambda"], T=result["T"])
