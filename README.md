# Frictionless Data Exchanges (FRX) for data challenges

Welcome to the FRX Challenges project! This is an open source repository that provides key software components for running competitive data science challenges.

FRX stands for **F**rictionless **R**eproducibility e**X**change. Inspired by [Donoho, 2023](https://doi.org/10.48550/arXiv.2310.00865). This project enables communities to leverage cloud infrastructure and interactive computing tools to **host data challenges with live computation**.

## Target functionality and goals

This is a young project that is under active development.
Below are the core workflows that we wish to support:

- **prompts**: Allow organizers to create a website that describes the data challenge and provides instructions for participants. 
- **submissions**: Allow participants to create one or more submissions for evaluation. 
- **evaluators**: Leverage cloud infrastructure to run submissions against standardized environments and datasets, and allow organizers to define their own evaluation scripts, criteria, and metrics.
- **feedback**: Provide information to participants about how their submissions scored relative to others.
- **teams**: Allow participants to submit and view their results as a team of people.

## About this project and acknowledgements

This project was built in collaboration with [the HHMI CellMap Segmentation challenge](https://cellmapchallenge.janelia.org/), which funded its original development.
Our goal is to generalize the infrastructure that enabled this challenge to be used for other communities, datasets, and workflows.

It builds heavily upon the Jupyter ecosystem and is designed to be interoperable with community-based cloud infrastructure like [JupyterHub](https://jupyterhub.readthedocs.io) and [BinderHub](https://binderhub.readthedocs.io).

It is currently developed and maintained [by 2i2c](https://2i2c.org), a non-profit dedicated to providing communities with interactive computing infrastructure to create and share knowledge.

## Technical details

This repository contains the core software that powers the FRX Challenges platform.
It consists of a Django application that is meant to leverage cloud infrastructure as part of the evaluation system.

### Additional Helm chart

The Helm chart lets a user create a reproducible and maintainable
deployment of FRX Challenges on a Kubernetes cluster in a cloud environment. The
released charts are made available in our [Helm chart
repository](https://2i2c.org/frx-challenges-helm-chart).
