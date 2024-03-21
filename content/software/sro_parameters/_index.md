---
title: "sro_parameters"
draft: false
date: 2022-08-27T09:16:45.000Z
description: "OVITO modifier for Cowley short range order parameter"
---

The Cowley short range order parameter measures the tendency for atoms to form ordered phases in a solid solution.

Traditionally, the Cowley short range order parameter is expressed in terms of the number of nearest neighbors of a given atom. However, a more general definition is useful for studying amorphous phases. In our case, this was useful for grain boundaries.

As such, we developed an equivalent order parameter calculation in terms of a distance cutoff as an [OVITO](https://www.ovito.org/) modifier. This is on the Python Package Index as [cowley-sro-parameters](https://pypi.org/project/cowley-sro-parameters/), and can therefore be installed with ``pip``:

```bash
pip install cowley-sro-parameters
```

An example usage is included in the package's [GitHub repository](https://github.com/muexly/cowley_sro_parameters).