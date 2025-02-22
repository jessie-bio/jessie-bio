
# Numpy
import numpy as np

# Para dataframes
import pandas as pd

# Visualizaciones
import matplotlib.pyplot as plt1
import matplotlib as mpl
import matplotlib.pylab as plt # Para gráficos

import seaborn as sns


!pip install neurolib

import neurolib
from functools import partial
from neurolib.models.aln import ALNModel
from neurolib.utils.loadData import Dataset
from neurolib.utils.signal import RatesSignal, BOLDSignal

import scipy

# Importamos el modelo ALN
from neurolib.models.aln import ALNModel

# Importar funciones de la libreria
import neurolib.utils.functions as func

# Colormap
plt.rcParams['image.cmap'] = 'viridis'

ds = Dataset("hcp")

#Como se ve el modelo ALN
model = ALNModel()
model.params['sigma_ou'] = 0.1 # add some noise

model.run()
plt.plot(model['t'], model['rates_exc'].T, lw=2, c='k')
plt.xlabel("t [ms]")
plt.ylabel("Rate [Hz]")
plt.xlim(1000, 2000);

plt.plot(model['t'], model['rates_exc'].T)
plt.xscale("log")

plt.yscale("log")

plt.xlabel("t [ms]")
plt.ylabel("Rate [Hz]")


plt.show()

#nuevos parametros para el modelo
model = ALNModel(Cmat = ds.Cmat, Dmat = ds.Dmat)

model2 = ALNModel()
model.params['duration'] = 3*60*1000
# Info: value 0.2*60*1000 is low for testing
# use 5*60*1000 for real simulation
model.params['mue_ext_mean'] = 1.57
model.params['mui_ext_mean'] = 1.6
# We set an appropriate level of noise
model.params['sigma_ou'] = 0.09
# And turn on adaptation with a low value of spike-triggered adaptation currents.
model.params['b'] = 5.0

# Plot the structural connectivity matrix by calling model.params['Cmat'] and fiber length matrix by calling model.params['lengthMat']. *"""

from matplotlib.colors import LogNorm
fig, axs = plt.subplots(1, 3, figsize=(12,8), dpi=75)
fig.subplots_adjust(wspace=0.28)

im = axs[0].imshow(model.params['Cmat'], norm=LogNorm(vmin=10e-5, vmax=np.max(model.params['Cmat'])))
axs[0].set_title("Fiber count matrix")
fig.colorbar(im, ax=axs[0],fraction=0.046, pad=0.04)
im = axs[1].imshow(model.params['lengthMat'], cmap='viridis')
axs[1].set_title("Fiber lenght matrix")
fig.colorbar(im, ax=axs[1],fraction=0.046, pad=0.04)
im = axs[2].imshow(ds.FCs[0], cmap='viridis')
axs[2].set_title("Empirical RS'FC")
fig.colorbar(im, ax=axs[2],fraction=0.046, pad=0.04)

#Cmat fiber count matrix
#Dmat fiber lenght matrix
#Empirical FC / empirical RS-fc

#Analysis of spontaneously correlated low-frequency activity fluctuations across the brain using functional (MRI)- (RSFC)
model.run(chunkwise=True, chunksize = 100000, bold=True)

# Plot functional connectivity and BOLD timeseries (z-scored)
fig, axs = plt.subplots(1, 2, figsize=(10, 4), dpi=75, gridspec_kw={'width_ratios' : [1, 1.5]})
axs[0].imshow(func.fc(model.BOLD.BOLD[:, 5:]))
axs[1].imshow(scipy.stats.mstats.zscore(model.BOLD.BOLD[:, model.BOLD.t_BOLD>10000], axis=1), aspect='auto', extent=[model.BOLD.t_BOLD[model.BOLD.t_BOLD>10000][0], model.BOLD.t_BOLD[-1], 0, model.params['N']]);

axs[0].set_title("FC")
axs[0].set_xlabel("Brain area")
axs[0].set_ylabel("Brain area")
fig.colorbar(im, ax=axs[0],fraction=0.046, pad=0.04)
axs[1].set_title("resultados modelo de BOLD")
axs[1].set_xlabel("t [ms]")
fig.colorbar(im, ax=axs[1],fraction=0.046, pad=0.04)

# the results of the model are also accesible through an xarray DataArray
fig, axs = plt.subplots(1, 1, figsize=(12, 4), dpi=75)

plt.plot(model.xr().time, model.xr().loc['rates_exc'].T);

fig, axs = plt.subplots(1, 1, figsize=(12, 4), dpi=75)


plt.plot(model.xr().time, model.xr().loc['rates_exc'].T);
plt.xlabel('t [ms]')
plt.ylabel('Rate [Hz]')

# displaying the title
plt.title("Neural activity")

# correlacion entre datos empiricos FC vs modelo
scores = [func.matrix_correlation(func.fc(model.BOLD.BOLD[:, 5:]), fcemp) for fcemp in ds.FCs]

print("Correlation per subject:", [f"{s:.2}" for s in scores])
print(f"Mean FC/FC correlation: {np.mean(scores):.2}")

def plot_output_and_spectrum(model, individual=False, vertical_mark=None):
    """A simple plotting function for the timeseries
    and the power spectrum of the activity.
    """
    fig, axs = plt.subplots(
        1, 2, figsize=(8, 2), dpi=150, gridspec_kw={"width_ratios": [2, 1]}
    )
    axs[0].plot(model.t, model.output.T, lw=1)
    axs[0].set_xlabel("Time [ms]")
    axs[0].set_ylabel("Activity [Hz]")

    frs, powers = func.getMeanPowerSpectrum(model.output, dt=model.params.dt)
    axs[1].plot(frs, powers, c="k")

    if individual:
        for o in model.output:
            frs, powers = func.getPowerSpectrum(o, dt=model.params.dt)
            axs[1].plot(frs, powers)

    axs[1].set_xlabel("Frequency [Hz]")
    axs[1].set_ylabel("Power")

    plt.show()

    plot_output_and_spectrum(model)

#esta explota
plot_output_and_spectrum(model)

#este es el gráfico a fitear con lineal
# el x e y son los graficados en el espectro de potencia arriba:
#x=frs
#y = powers

for o in model.output:
            frs, powers = func.getPowerSpectrum(o, dt=model.params.dt)

def power_law(x, a, b):
    return a * np.power(x, -b)



plt.plot(frs, powers)

plt.xscale("log")

plt.xlim(10^1, )

plt.yscale("log")
plt.xlabel("Frequency [Hz]")
plt.ylabel("Power")

plt.show()

a = np.log(frs)
b = np.log(powers)
plt.plot(a, b)
plt.show()

type (frs)

frs.shape

frs2 = np.log(frs)

powers2 = np.log(powers)

for o in model.output:
            frs, powers = func.getPowerSpectrum(o, dt=model.params.dt)

def power_law(x, a, b):
    return a * np.power(x, -b)



plt.plot(frs2, powers2)

plt.xlabel("Frequency [Hz]")
plt.ylabel("Power")
plt.show()


splot = sns.regplot(frs2, powers2)

def power_law(x, a, b):
    return a * np.power(x, -b)
from scipy.optimize import curve_fit

popt, pcov = curve_fit(power_law, frs, powers, p0=[1, 1], bounds=[[1e-3, 1e-3], [1e20, 50]])

plt.plot(power_law(frs, *popt), label='power law')

plt.legend()
plt.show()
