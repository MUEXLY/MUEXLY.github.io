---
title: "arrhenius_rate"
draft: false
date: 2024-04-23T17:15:01+0000
description: "Arrhenius rate law computation"
---

We have developed a lightweight [LAMMPS](https://en.wikipedia.org/wiki/LAMMPS) interface for computing the [Arrhenius rate parameters](https://en.wikipedia.org/wiki/Arrhenius_equation) for a given process:

$$
r = \nu \exp\left(-\frac{E_a}{k_BT}\right)
$$

where $k_B$ is the Boltzmann constant, $T$ is temperature, and $\nu$ and $E_a$ are respectively the rate prefactor and activation energy of the process.

Our interface computes both $\nu$ and $E_a$ by performing a [nudged elastic band](https://pubs.acs.org/doi/10.1021/acs.jctc.1c00462) calculation, followed by a dynamical matrix calculation to calculate the Vineyard prefactor.

The code and interface are installable from [GitHub](https://github.com/MUEXLY/arrhenius_rate).
