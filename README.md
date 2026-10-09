# Term Project: Behavioral and EEG Analysis of Learning Difficulties

## Project Overview

This project investigates behavioral performance and
electroencephalography (EEG) activity in children with reading or
mathematics learning difficulties. The dataset was collected to study
children who used assistive technology to strengthen reading and
mathematics skills. The experimental group used Smartick over a
three-month period, with a control group available for comparison.

The broader goal is to examine behavioral changes between
pre-intervention (PRE) and post-intervention (POST) assessments and
investigate whether EEG activity provides additional information about
neural patterns associated with those changes.

**Scope note:** This is an interim analysis. The analyses described
below do not establish that the intervention caused greater improvement
than the control condition. EEG analyses are ongoing, and no final
neural findings are claimed.

## Research Questions

1.  What changes in behavioral and psychometric outcomes are observed
    between PRE and POST?
2.  Do multivariate patterns of behavioral change differ between
    experimental and control groups?
3.  What EEG features and channel-level patterns can be observed during
    reading-related tasks?
4.  Do channel- and event-related EEG patterns appear consistent across
    children within the same subgroup?
5.  Are EEG patterns different between PRE and POST, or between
    experimental and control groups?
6.  Are EEG changes associated with behavioral changes?

These are guiding questions, not results already established.

## Dataset Structure

The dataset contains 76 children and separates participants into
reading-difficulty (R) and mathematics-difficulty (M) groups. Each
domain includes experimental and control subgroups.

-   **Sessions:** `ses-1` corresponds to PRE and `ses-2` corresponds to
    POST.
-   **File format:** EEG recordings are stored as EEGLAB `.set` files.
-   **Reading recordings:** `run-1` is resting state; `run-2` is the
    reading/comprehension task.
-   **Mathematics recordings:** `run-1` is resting state; `run-2` and
    `run-3` are arithmetic task blocks.
-   **Intervention:** The experimental group used Smartick for three
    months; the control group did not.

The dataset also includes psychometric/behavioral information. Reading
outcomes include orthographic errors, phonological errors, reading
speed, comprehension and selective attention. Mathematics outcomes
include WRAT-4, hits/accuracy, reaction time and selective attention.
Demographic or background variables include group, gender, age and IQ.

EEG data quality varies across files. Some recordings are flagged as
having inconsistent quality, and some are unavailable because of
technical problems. These issues need to be considered in preprocessing
and analysis.

## Work Completed So Far

### Behavioral and Statistical Analysis

-   Reviewed the available behavioral and psychometric variables.
-   Investigated PRE--POST changes.
-   Compared experimental and control groups.
-   Created plots showing standardized PRE--POST changes across
    individual outcomes.
-   Conducted within-group multivariate tests using Hotelling's
    T-squared for reading and mathematics.
-   Conducted multivariate comparisons of experimental versus control
    change patterns and visualized participant change patterns using
    PCA.

### Current Statistical Findings

The current within-group Hotelling's T-squared results indicate
statistically significant joint PRE--POST changes in both groups for
both domains:

  ------------------------------------------------------------------------
  Domain                Group                             Reported p-value
  --------------------- --------------------- ----------------------------
  Mathematics           Control                                     0.0009

  Mathematics           Experimental           Displayed as 0.0000; verify
                                                       the unrounded value

  Reading               Control                                     0.0002

  Reading               Experimental                                0.0015
  ------------------------------------------------------------------------

The current between-group MANOVA comparisons of multivariate change
vectors were not statistically significant:

  Domain          Reported p-value
  ------------- ------------------
  Mathematics               0.3772
  Reading                   0.5030

These findings should be interpreted carefully. Significant within-group
PRE--POST change does not demonstrate that Smartick caused the change.
The between-group tests did not establish a statistically significant
difference in multivariate change patterns. Nonsignificance also does
not establish that the groups are equivalent or that there is no
intervention effect.

Before reporting these analyses as final, verify the test
implementation, assumptions, handling of missing data, and exact
unrounded p-values in the analysis code.

## EEG Data Inspection

An example reading-task EEG file inspected during the project had the
following properties:

-   **Channels:** 32
-   **Sampling frequency:** 256 Hz
-   **Duration:** approximately 184.28 seconds
-   **Samples:** 47,177
-   **Format:** EEGLAB `.set`

The channel names extracted from that file were:

`FP1, FP2, F7, F3, Fz, F4, F8, FT10, FT9, T7, FC5, C3, FC1, FC2, FC6, C4, Cz, CP1, CP5, TP9, CP2, CP6, TP10, T8, P7, P3, Pz, P4, P8, O1, Oz, O2`

These properties describe the inspected example file and should not
automatically be assumed for every recording without checking.

## EEG Analysis Plan

The EEG work is intended to progress from individual recordings to
group-level comparisons.

1.  **Inspect individual recordings.** Load and visualize EEG signals
    and review recording quality.
2.  **Examine channels.** Investigate channel-level behavior without
    assuming in advance which channels will be informative.
3.  **Examine task events.** Align analysis with available event markers
    and inspect signal behavior around relevant events.
4.  **Explore EEG features.** Candidate features may include time-domain
    characteristics (such as amplitude and variability),
    frequency-domain measures (such as spectral power), and
    time--frequency changes around events. These are features under
    consideration, not all confirmed or finalized.
5.  **Compare participants within subgroups.** Determine whether
    observed patterns recur across children in the same domain and
    experimental/control subgroup.
6.  **Compare experimental and control groups.** Evaluate group
    differences using appropriate statistical methods.
7.  **Compare PRE and POST.** Investigate whether EEG features or
    patterns differ between sessions.
8.  **Relate EEG to behavioral change.** Where data quality and sample
    size permit, examine associations between EEG changes and changes in
    behavioral performance.

The current methodological principle is to inspect individual and
channel-level responses around task events before deciding which
patterns can be meaningfully summarized across participants.

## Planned Work

-   Continue validating EEG file loading, event information and channel
    metadata.
-   Review data quality and missing recordings before group comparisons.
-   Finalize a defensible set of EEG features and analysis windows.
-   Inspect individual-channel and event-related patterns.
-   Assess whether patterns are reproducible within each subgroup.
-   Compare PRE--POST and experimental--control patterns.
-   Relate EEG results to behavioral outcomes where appropriate.
-   Document statistical methods, assumptions, effect estimates and
    uncertainty.

## Interpretation and Limitations

-   Behavioral change and intervention-specific effects are different
    questions.
-   Within-group PRE--POST significance alone does not establish a
    causal intervention effect.
-   PCA plots are visual summaries; PCA axes are combinations of
    variables and are not direct measures of improvement.
-   Nonsignificant between-group tests do not prove equivalence.
-   EEG is high-dimensional, and individual variability, recording
    quality, missing data, event timing and multiple comparisons need to
    be considered.
-   Reading and mathematics should initially be analyzed separately
    because their tasks and behavioral outcomes differ.
-   No specific brain region, channel, frequency band or neural
    mechanism is claimed to explain improvement until the analysis
    supports that conclusion.

## Project Narrative

The project follows this progression:

**Behavioral description → within-group PRE--POST analysis →
experimental--control comparison → EEG file and channel inspection →
event- and feature-level EEG analysis → subgroup and session comparisons
→ brain--behavior relationships.**

The behavioral analysis characterizes whether and how measured
performance changes. The EEG analysis is intended to investigate neural
activity patterns associated with those changes, without assuming in
advance that a particular pattern or intervention effect will be found.

## Dataset Reference

Corona-González, C. E., Stefano-Ramos, C. R. D., Rosado-Aíza, J. P.,
Ibarra-Zarate, D. I., Gómez-Velázquez, F. R., & Alonso-Valerdi, L. M.
(2026). *Dataset of psychophysiological data from children with learning
difficulties who strengthen reading and math skills through assistive
technology* (Version 1.0.0) \[Data set\]. NEMAR.
https://doi.org/10.82901/nemar.on006260

Dataset page: https://nemar.org/dataset/on006260

Associated paper: *Enhancing learning skills in children by using
assistive technology: A psychophysiological database.*
https://pmc.ncbi.nlm.nih.gov/articles/PMC12522821/

**Citation note:** Verify the associated paper's full bibliographic
details (including publication year, journal, and DOI) against the
publisher record before submitting a final report.

## Repository Contents

Update this section to match the actual files in your project
repository.

-   `README.md` --- project overview, progress and analysis plan.
-   Behavioral/statistical analysis scripts and figures.
-   EEG loading, inspection and visualization scripts.
-   EEG feature extraction and comparison scripts (as developed).
-   Presentation slides and supporting figures.
