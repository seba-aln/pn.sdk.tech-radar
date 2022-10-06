# Technology radar for PubNub SDK Team

The definition of IGI Global Dictionary says:

> A technology radar is a way of observing the market for new innovations and technologies and gather information about them in a consistent style, relate and evaluate them on behalf of the own business.

For us it is the way to find, focus on and share trending and helpful technologies across our team and other teams in PubNub

## Why we do it?

We believe this technology radar will allow us to better discuss on what technologies we should focus in a near future
## How to submit new technology radar?

1. Clone this repository
1. Create a markdown document or copy CSV file under `radars` directory
1. Run `scripts/parse.py` file to generate `json` file

    ```
    source venv/bin/activate
    python scripts/parse.py -f radars/radar_file.md -t md
    ```
2. Commit changes

## List of radars so far
<!-- list below is auto generated. do not modify anything between list-start and list-end -->
<!-- list-start -->
* [SDK Radar 1 Fall 2022](https://radar.thoughtworks.com/?sheetId=https%3A%2F%2Fraw.githubusercontent.com%2Fseba-aln%2Fpn.sdk.tech-radar%2Fmain%2Foutput%2Fsdk-radar-1-fall-2022.json)
<!-- list-end -->

## What's left to do

1. Automatic update of this readme file through GitHub Actions
2. Experiment with generating radars using i.e. [Tech Radar Generator](https://github.com/dprgarner/tech-radar-generator)
3. Use GitHub Pages to host those static files