import numpy as np
from tmm import coh_tmm

wavelength_nm = np.linspace(450, 750, 301)
n = [1.0, 1.45, 1.52]  # 示例常数；真实材料应用色散数据
d_nm = [np.inf, 110.0, np.inf]
R = np.array([coh_tmm("s", n, d_nm, 0.0, wl)["R"]
              for wl in wavelength_nm])
np.savez("thinfilm.npz", wavelength_nm=wavelength_nm, R=R)
