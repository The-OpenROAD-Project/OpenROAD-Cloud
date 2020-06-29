# OpenROAD Cloud
The source code that empowers [https://cloud.theopenroadproject.org/](https://cloud.theopenroadproject.org/)

![version](https://img.shields.io/badge/version-beta-blue.svg)
![coverage](https://img.shields.io/badge/coverage-unknown-yellowgreen.svg)
![uptime](https://img.shields.io/badge/uptime-50%25-red.svg)

## Purpose
[The OpenROAD Project](https://theopenroadproject.org/) aims at providing a 24-hour, no-human-in-the-loop layout design 
for SoC, package and PCB with no Power-Performance-Area (PPA) loss. The cloud infrastructure set up at 
[OpenROAD Cloud](https://cloud.theopenroadproject.org/) makes the tools and designs accessible through
an easy-to-use web-based interface.

If you want to jump start using our platform, go to the [Quickstart](#quickstart-guide) section. 
To get a deeper look at the platform, refer to the [documentation](#documentation) section.  

## Quickstart Guide
![quickstart](https://img.shields.io/badge/quickstart-new-brightgreen.svg)

Go to [https://cloud.theopenroadproject.org](https://cloud.theopenroadproject.org), 
register for an account using your email. 

### Prepare Your Design

OpenROAD Cloud processes designs that reside in a `git` repository. 
In order to run your own design through OpenROAD Cloud flow, create add a file to the root of the repository and name it `openroad.yml`.
This file declares required configurations for running the flow. Below is a description for its fields described on the [AES example](https://github.com/OpenROAD-Cloud/aes):

```
platform: nangate45             # currently only supports 'nangate'

design_name: aes_cipher_top     # top-level design name

verilog_files:                  # relative path of the source files
  - src/aes_cipher_top.v
  - src/aes_inv_cipher_top.v
  - src/aes_inv_sbox.v
  - src/aes_key_expand_128.v
  - src/aes_rcon.v
  - src/aes_sbox.v
  - src/timescale.v
sdc_file: constraint.sdc        # relative path of the constraint file

die_area: "0 0 620.15 620.6"            # die area as a box
core_area: "10.07 11.2 610.27 610.8"    # core area as a box

clock_period: 5.00             # clock period in nanoseconds
```

> Make sure to upload the design files (in `.v` format) and the constraint file (`in .sdc` format) to the same repository as well.

### Run OpenROAD Cloud Flow

1. Login to your account on [https://cloud.theopenroadproject.org](https://cloud.theopenroadproject.org).
2. From left panel, click **My Designs**.
3. Click **Import Design**.
4. Give a name to your design (can be any arbitrary nickname), and paste in the repo URL (repository must be public).
5. After the design is added, click **Run on latest version**.
6. You will receive email notifications updating you on the status of the flow.

## Deployment on a Private Cloud
Although the publicly available platform enables our research and offers ease-of-use and latest 
improvements to users around the world, OpenROAD flow can be independently deployed on a private 
cloud infrastructure.

### Architecture
TODO:

### Deployment Guide
TODO:

## Contributing

Propose feature requests that you can work on using the [Feature Request](.github/ISSUE_TEMPLATE/feature_request.md) template.

In general, here are the skills and tracks you can contribute to:

- **Frontend development**: We build user-centric web-based interfaces. You can contribute to this track if you have
decent skills in `HTML`, `CSS`, `JavaScript` and `JQuery`. 
Dare to modernize our frontend stack to `VueJS`, `Angular` or `React`? We would love to hear from you. 
- **Backend development**: Our REST APIs are built using `Python Django REST Framework`. 
In addition, there are some views rendered using `Django template system`. 
Contribute to this track if you are familiar with `Python`, `Djnago`, `REST APIs` and databases.
- **Testing**: writing unit tests, integration tests, and automating this process is at the heart of our
CI/CD pipeline. Contribute to this track to enhance the reliability of the platform.

Before submitting a `Pull Request`, get in touch with the project contributors to align what features you will
be working on. 

## Help
In the issues tab, create a new issue with your question.


## License
BSD 2-Clause License

Copyright (c) 2020, The OpenROAD Project All rights reserved.
