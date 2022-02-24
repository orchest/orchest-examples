<p align="center">
<a href="https://orchest.io">
  <img src="imgs/logo.png" width="300px" />
</a>
</p>
<br/>

[Website](https://www.orchest.io) —
[Main repo](https://github.com/orchest/orchest) —
[Docs](https://orchest.readthedocs.io/en/stable/)

# Orchest examples

This is a list of official and community submitted examples 🤗. This list is used by
Orchest to propose starter examples to users, including information such as the
author, the number of stars and forks of the repo. If you would like to be part
of this, make a PR!

## Contributing

Make a PR that adds a new entry to the list of examples in this README. This entry must
have the following format (mind the spaces!):

```- [title](github url) -<!--o--> description (length limit of 280) <!--o-->- `tag1` `tag2` `tag3` (up to five tags)```

You could also add a badge in your repo by adding the following script in your `README.md` (NOTE: you need to replace `your-repo-url` with your repo URL).

```markdown
[![Open in Orchest](https://github.com/orchest/orchest-examples/raw/main/imgs/open_in_orchest.svg)](https://cloud.orchest.io/?import_url=your-repo-url)
```

An example badge to import our [quickstart](https://github.com/orchest/quickstart) repo in Orchest:

[![Open in Orchest](https://github.com/orchest/orchest-examples/raw/main/imgs/open_in_orchest.svg)](https://cloud.orchest.io/?import_url=https://github.com/orchest/quickstart)

And thank you 💗!

## Examples

<!-- EXAMPLES_BEGIN -->
- [Quickstart Pipeline](https://github.com/orchest/quickstart) -<!--o--> A quickstart pipeline that trains some simple models in parallel. <!--o-->-   `quickstart` `machine-learning` `training` `scikit-learn`
- [Orchest + dbt](https://github.com/ricklamers/orchest-dbt) -<!--o--> Use dbt inside of Orchest for your materialized views. <!--o-->-   `python` `dbt` `sql`
- [Image Super-Resolution](https://github.com/fruttasecca/image_super_resolution) -<!--o--> Use Image Super-Resolution (ISR) to enhance any image with different methods. <!--o-->-   `python` `super-resolution` `machine-learning` `computer-vision`
- [Coqui TTS](https://github.com/ricklamers/orchest-coqui-tts) -<!--o--> Generate an audio snippet from a text sample and send it as a message on Slack/Discord. <!--o-->- `tts` `audio` `machine-learning`
- [Redis and Postgres](https://github.com/ricklamers/orchest-redis-postgres) -<!--o--> An example of how to use Redis and Postgres in an Orchest pipeline. <!--o-->- `postgres` `services`
- [Weaviate + Orchest](https://github.com/ricklamers/orchest-weaviate-tweakers-search) -<!--o--> Search scraped comments with semantic vector search. <!--o-->- `nlp` `streamlit` `search` `scraping`
- [Polyglot: Python, Julia and R in one pipeline](https://github.com/ricklamers/orchest-multi-language-pipeline) -<!--o--> An example pipeline showing how to use multiple languages in a same Orchest pipeline. <!--o-->- `environments` `julia` `r` `python`
- [Web Scraping using Photon](https://github.com/ricklamers/photon-orchest-pipeline) -<!--o--> A pipeline that uses the open source Photon library for webscraping. Use this as a starting point for a data ingest pipeline. <!--o-->- `scraping`
- [Search HN comments with PyWebIO](https://github.com/ricklamers/orchest-meilisearch-pywebio-hn) -<!--o--> Use web scraping, Meilisearch and PyWebIO for lightning fast comment search on HN. <!--o-->- `python` `pywebio` `scraping`
- [Mixing R and Python in one pipeline](https://github.com/orchest-examples/orchest-pipeline-r-python-mix) -<!--o--> A pipeline showcasing how Python and R can be used within the same pipeline. It also shows how you can call the Orchest SDK from within R. <!--o-->- `r` `python`
- [Calling the Orchest SDK from Julia](https://github.com/orchest-examples/julia-orchest-sdk) -<!--o--> An example pipeline that uses PyCall to be able to call the Orchest SDK from within Julia. <!--o-->- `julia`
- [OAuth QuickBooks example project](https://github.com/ricklamers/orchest-quickbooks-oauth) -<!--o--> Specific example of using the QuickBooks OAuth API in Orchest, but can be used for any OAuth 2.0 authentication flow. <!--o-->- `python` `oauth` `finance`
- [Two phase pipeline + Streamlit](https://github.com/ricklamers/two-phase-pipeline-streamlit) -<!--o--> This is an example project that demonstrates how to create a pipeline that consists of two phases of execution. <!--o-->- `python` `streamlit`
- [Scraped language classifier](https://github.com/ricklamers/orchest-language-classifier) -<!--o--> This pipeline classifies random text paragraphs found on websites linked to from random Wikipedia pages. <!--o-->- `python` `scraping` `streamlit`
- [Deep_AutoViML Pipeline](https://github.com/rsesha/deep_autoviml_pipeline) -<!--o--> Use popular python library, Deep_AutoViML to build multiple deep learning Keras models on any dataset, any size with this pipeline. Data must be in data folder and models are saved in your project folder. <!--o-->- `quickstart` `keras` `machine-learning` `tensorflow`
- [AutoViz Pipeline](https://github.com/rsesha/autoviz_pipeline) -<!--o--> Use popular python library, AutoViz to visualize any dataset, any size with this pipeline. Data must be in data folder and charts are saved in AutoViz_Plots fodler. <!--o-->- `quickstart` `auto-visualization` `machine-learning`
