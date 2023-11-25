#  Podcast Automation with Transistor.fm

## To Do

- [X] Automating the Creating of Draft Podcase Episodes in Transistor.fm
- [X] Automating the Downloading of Supreme Court Cases
- [X] Automating the Creation of Cover Image for Each Podcast Episode
- [ ] Automating the Uploading of Cover Image & Audio into their Draft Episode in Transistor.fm


## Supreme Court of the United States Podcast Episode Generator

This project generates podcast covers for episodes covering the Supreme Court of the United States (SCOTUS) decisions. It includes a script to download SCOTUS Arguments audio, another to generate the podcast covers, and a GitHub Actions workflow to run the scripts manually.

### Project Structure

- `download-scotus.py`: Python script to download SCOTUS decision data.
- `PodcastCover.py`: Python script to generate podcast covers from decision data.
- `transistor-csv.py`: (Description of this script's purpose, based on your implementation.)
- `scotus.csv`: CSV file containing data related to SCOTUS cases.
- `Blank.png`: Template image used by `PodcastCover.py` to generate podcast covers.
- `.github/workflows/`: Directory containing GitHub Actions workflows to run the scripts.

### Setup

To run these scripts, you'll need Python installed on your machine, along with the `pandas` and `Pillow` packages. You can install them using pip:

```bash
pip install pandas Pillow

### Usage

#### Download SCOTUS Data

To download the latest SCOTUS data:

```bash
python download-scotus.py
```

Make sure to update the `scotus.csv` file path in the script if it's different from your setup.

#### Generate Podcast Covers

To generate podcast covers:

```bash
python PodcastCover.py
```

Ensure `Blank.png` and the font file are in the correct paths as the script expects.

#### Manual GitHub Workflow Trigger

You can also run these scripts via GitHub Actions:

1. Navigate to the 'Actions' tab of your GitHub repository.
2. Select the respective workflow.
3. Click on 'Run workflow' and choose the branch you want to run the workflow on.
4. Click 'Run workflow' again to start the process.

### Customization

You can customize the podcast cover generation by editing `podcastcover.py` to change the font, layout, or design used in the cover images.

### Contributing

Contributions to this project are welcome. Please open an issue or submit a pull request with your proposed changes.


---

This project is not officially affiliated with the Supreme Court of the United States.
```

