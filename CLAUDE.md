# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repository is

A student's weekly lab repository for a bioinformatics lab course (생물정보학실험), run in GitHub Codespaces. There is no build system, package manager, linter, or test suite — work consists of small standalone Bash and Python scripts that process FASTA/text files. All docs, comments, and program output are in Korean; keep new content in Korean to match.

## Layout and conventions

- `labNN/` — one folder per week, created by copying `lab-template/` (`cp -r lab-template labNN`). Each has:
  - `data/` input data (FASTA etc.), `doc/` reports and result files (`.tsv`, `.md`), `src/` the student's scripts.
- `resources/` — instructor-provided sample data (`resources/data/`) and example scripts (`resources/src/`).
- Scripts are run **from the lab folder**, with paths relative to it, e.g.:
  ```
  cd lab07
  python3 src/summary.py data/seqs.fasta doc/summary.tsv
  bash src/gc.sh data/seqs.fasta
  ```
- Scripts take file paths via `sys.argv` / `$1`; there is no argparse or packaging.
- Students often record run commands and outputs as trailing `#` comments at the bottom of scripts (assignment answers). Preserve these when editing.
- Each week's work is committed with messages like `lab07 완료` / `N번 전`.

## Python code (lab07 onward)

From lab07 the FASTA logic is centralized in `lab07/src/fasta.py` (`read_fasta`, `write_fasta`, `gc_content`, `reverse_complement`, `length_stats`; documented in `lab07/src/README.md`). Other lab07 scripts import it with `from fasta import ...`, so they must be run as `python3 src/<script>.py` (the script's directory is on `sys.path`). Note `read_fasta` uppercases every line, including header names. Running `python3 src/fasta.py <file>` also runs its built-in assert self-test. lab06 uses the earlier style where each script duplicates its own FASTA parsing.

Keep code at a beginner level consistent with the course (plain loops, dicts, `open`), not idiomatic-advanced Python or third-party libraries.

## Environment

- Dev containers in `.devcontainer/` are chosen per week: `1-basic` (weeks 02–07, Python + shell), `2-conda` (micromamba), `3-seq` (seqkit, blast, mafft, iqtree, fastqc, fastp), `4-genome` (adds shovill, prokka). `.devcontainer/check.sh` prints which tools are present.
- `$MYHOME` is the workspace root; plain `cd` returns there.
- Don't install tools yourself (except in the conda week, where installing is the assignment).
- Sequencing reads (`*.fastq*`, `*.sra`) and assembly/annotation output dirs (`shovill_out/`, `prokka_out/`, …) are gitignored; re-download data with `wget` rather than committing it.
