---
title: "pbc_distance_calculator"
draft: false
date: 2024-04-23T17:09:21+0000
description: "Periodic boundary condition distance calculator"
---

Computing the minimum-image distance between two particles is crucial for atomistic simulations.

We have developed a Python package for computing the minimum-image distance between two particles for any arbitrary crystal. This package is fully vectorized, so all distances can be computed in one go, and has Jax and PyTorch support, letting users perform the calculations on CPUs, GPUs, and TPUs.

This package is published on the Python Package Index as ``pbc-distance-calculator``, and thus can be installed with pip:

```bash
pip install pbc-distance-calculator
```
