# ScatterBridge

<p align="center">
    <a href="https://github.com/gitUmaru/scatterbridge-" target="_blank">
    <img align="center" alt="ScatterBridge" src="assets/scatterbridge-logo.png" width="60%" height="auto"/>
    </a>
</p>

<p align="center">
Learning to translate between reflection-mode and transmission-mode optical scattering measurements of tissue, starting with careful data exploration.
</p>

## Objective

A single tissue sample is imaged at the same time by two microscope objectives: one collects light scattered backward (reflection) and one collects light scattered forward (transmission). The two views are co-registered on the same pixel grid but respond to different physics, so they carry different and partly complementary information.

The goal of this project is to build models that translate between the reflection and transmission channels: predict one channel from the other, and reconstruct the shared scattering structure that both channels observe. The reflection channel is the easier one to acquire in practice, so a reliable reflection-to-transmission map is the main target.

This repository is at the data-exploration stage. It inspects the dataset, verifies that the two channels are paired and aligned, and quantifies how they relate before any model is built. No model is trained yet.

## The optical setup

```mermaid
flowchart LR
    SRC["Pulsed laser<br/>266 nm / 405 nm"] -->|excitation| S

    subgraph SAMPLE["Tissue sample"]
        S(("Scattering<br/>particle"))
    end

    S -->|back-scattered light| RO["Reflection<br/>objective"]
    S -->|forward-scattered light| TO["Transmission<br/>objective"]

    RO --> RD["Reflection detector<br/>352-sample time trace / pixel"]
    TO --> TD["Transmission detector<br/>352-sample time trace / pixel"]

    RD --> RI["Reflection<br/>scattering image"]
    TD --> TI["Transmission<br/>scattering image"]

    RI -. same pixel grid .-> TI
```

The stage raster-scans the sample in a serpentine pattern. At every pixel both objectives record a short time-domain trace, and those traces are reduced to per-pixel scattering values that form two co-registered images of the same tissue.

### Why this is interesting

Reflection and transmission probe the sample differently. Forward scattering is sensitive to what the light passes through, while backward scattering is dominated by surface and near-surface structure. The two images therefore agree on gross tissue morphology but diverge in contrast and detail, which is exactly what makes a learned translation non-trivial: the mapping is neither identity nor a simple intensity rescale. A model that recovers transmission-like contrast from the more easily acquired reflection channel would let a reflection-only instrument stand in for a harder two-sided measurement.

## Data layout

Each patch is a folder `SNNNN` containing two HDF5 files and a few 8-bit TIF previews.

| File | Contents |
| --- | --- |
| `scan_data_extracted.h5` | Per-sample signals `sig_1`..`sig_8` and the pixel-to-sample index map `sig_9`. Time-domain traces live in `sig_3` (transmission) and `sig_6` (reflection), 352 samples per pixel. |
| `frame_exports.h5` | Derived transmission images, each `(2000, 1999)` float32. |

Signals tagged with `-reflection` are the reflection channel (`sig_5`, `sig_6`, `sig_7`); the matching untagged signals are transmission (`sig_1`..`sig_4`, `sig_8`). Reflection and transmission share one pixel grid and one index map, so they are paired and aligned per pixel.

## Getting started

This project uses [uv](https://docs.astral.sh/uv/) for environment and dependency management.

```bash
# install dependencies into a local .venv
uv sync --extra notebook

# run the exploration over a deterministic sample of patches
uv run python scripts/explore_dataset.py

# or open the walkthrough notebook
uv run jupyter lab notebooks/01_data_exploration.ipynb
```

The script writes figures to `output/figures/` and summary tables to `output/tables/`. The notebook reproduces the same analysis inline and averages across all patches for a dataset-wide view.

## Repository structure

```
scatterbridge/
  src/scatterbridge/
    data/          data loading, exploration, plots, statistics
  notebooks/       guided data-exploration notebook
  scripts/         command-line entry points
  output/
    figures/       generated plots
    tables/        generated summary tables
  pyproject.toml
```

The `data` subpackage holds the current exploration code. Future work such as models and training lives in sibling packages under `src/scatterbridge/`.

## License

See [LICENSE](LICENSE).