You can find the podcast that this automation is for at the following: [Apple Podcasts](https://podcasts.apple.com/us/podcast/supreme-court-of-the-united-states/id1483973915), [Spotify](https://open.spotify.com/show/2T4w6ZUmYAml4ilCpDGFX2), [Google Podcasts](https://podcasts.google.com/feed/aHR0cHM6Ly9mZWVkcy50cmFuc2lzdG9yLmZtL3N1cHJlbWUtY291cnQtb2YtdGhlLXVuaXRlZC1zdGF0ZXM), [Amazon Music Podcasts](https://music.amazon.com/podcasts/77ffa01b-3aa3-4498-916f-ccd640280dca/supreme-court-of-the-united-states),[YouTube](https://www.youtube.com/channel/UC02oIiNULwiiDxB0Aw1aySg),[Castro](https://castro.fm/itunes/1483973915),[GoodPod](https://goodpods.com/podcasts/supreme-court-of-the-united-states-248195) ,[Anghami](https://play.anghami.com/podcast/1029643374),[RadioPublic](https://radiopublic.com/supreme-court-of-the-united-state-GK2bbz),[CastBox](https://castbox.fm/channel/3166723?utm_campaign=ex_share_ch&utm_medium=exlink&country=us) ,[Pandora](https://www.pandora.com/podcast/supreme-court-of-the-united-states/PC:48735),[PodcastAddict](https://podcastaddict.com/podcast/supreme-court-of-the-united-states/3071811),[Player.fm](https://player.fm/series/supreme-court-of-the-united-states),[TuneIn](https://tunein.com/podcasts/Podcasts/Supreme-Court-of-United-States-p1257992/),[iHeartRadio](https://www.iheart.com/podcast/269-supreme-court-of-the-unite-70629899/),[Deezer](https://www.deezer.com/us/show/1932832)

![](https://images-internal.transistor.fm/images/show/12890/thumb_1602212470-artwork.jpg)
#  Podcast Automation with Transistor.fm
- https://developers.transistor.fm
- `https://www.supremecourt.gov/media/audio/mp3files/<Case ID>.mp3`


## To Do

- [X] Automating the Creating of Draft Podcase Episodes in Transistor.fm
- [X] Automating the Downloading of Supreme Court Cases
- [X] Automating the Creation of Cover Image for Each Podcast Episode
- [ ] Automating the Uploading of Cover Image & Audio into their Draft Episode in Transistor.fm

## Future To Do
- [ ] Combine the scripts to operate as a modular python application
- [ ] Fix the Text Placement on Podcast Episode Cover
- [ ] Make it so when podcast-covers.yml runs, it also commit changes to the repo.
- [ ] Make it so when download-scotus.yml runs, it also commit changes to the repo.
- [ ] Refractoring the program to be in Rust language.


## Supreme Court of the United States Podcast Episode Generator



Downloads audio from Supreme Court of the United States (SCOTUS) arguments and generate podcast covers for each episode. It includes a script to download SCOTUS Arguments audio, another to generate the podcast covers, and a GitHub Actions workflow to run the scripts manually. 


### Project Structure

- `download-scotus.py`: Python script to download SCOTUS decision data.
- `podcast-cover.py`: Python script to generate podcast covers from decision data.
- `transistor-csv.py`: (Description of this script's purpose, based on your implementation.)
- `scotus.csv`: CSV file containing data related to SCOTUS cases.
- `Blank.png`: Template image used by `PodcastCover.py` to generate podcast covers.
- `.github/workflows/`: Directory containing GitHub Actions workflows to run the scripts.

### Setup

To run these scripts, you'll need Python installed on your machine, along with the `pandas` and `Pillow` packages. You can install them using pip:

```bash
pip install pandas Pillow
```

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
python podcast-cover.py
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


# This project is not officially affiliated with the Supreme Court of the United States.



