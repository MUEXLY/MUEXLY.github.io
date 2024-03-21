---
title: "chemical_potential"
draft: false
date: 2022-08-27T09:16:45.000Z
description: "LAMMPS interface to compute and fit chemical potentials in a solid solution"
---

Chemical potentials (and in particular their composition dependence) characterize the thermodynamics of a solid solution.

We developed a lightweight [LAMMPS](https://www.lammps.org/) interface to calculate chemical potentials in a solid solution and fit according to a linear model:

$$
\mu_\alpha = \mu_\alpha^\circ + \sum_\beta A_{\alpha\beta}x_\beta
$$

where $\mu_\alpha$ is the chemical potential of species $\alpha$, $\mu_\alpha^\circ$ is a reference chemical potential, $x_\beta$ is the atomic fraction of species $\beta$, and $A_{\alpha\beta}$ is a fitting parameter.

The code can be viewed and installed from its [GitHub repository](https://github.com/MUEXLY/chemical_potential).