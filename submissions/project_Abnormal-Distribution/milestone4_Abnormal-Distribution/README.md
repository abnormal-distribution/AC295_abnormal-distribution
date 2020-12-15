# News Sentiment Analysis for Stock Return Prediction by Abnormal Distribution

## Final Project


## Eduardo PEYNETTI, Jessica WIJAYA, Rohit BERI, Stuart NEILSON


## Overview
Transfer Learning, combined with open sourced state-of-the-art (SOTA) neural network models has democratized and hastened the adoption of machine learning in variety of fields ranging from medical science to astronomy. In this article, we explore the applicability of SOTA Natural Language Processing models for sentiment analysis in the financial domain (news, press releases, 10-Ks) for the purpose of building profitable trading strategies.  

We explore three different models, Loughran-McDonald, BERT, and Fin-BERT. We fine-tune Fin-BERT and take a look into their inner workings. We construct long/short portfolios of stocks based on the sentiment signal from each of these models and look at their performance. We find that sentiment in news is predictive of future stock returns. In the end, we discuss the learnings, challenges, and the path ahead.

* You can watch a short intro video [here](https://youtu.be/IgKKCww1svo)
* Presentation deck is available [here](https://github.com/abnormal-distribution/AC295_abnormal-distribution/blob/master/submissions/project_Abnormal-Distribution/milestone4_Abnormal-Distribution/presentation.pdf)
* Medium article is available [here](https://medium.com/@beri.rohit/b39171ba445c?source=friends_link&sk=799ef49570e3b88888e2e8dcd06fb94a)

## Presentation Deck
* [Link Here](https://github.com/abnormal-distribution/AC295_abnormal-distribution/blob/master/submissions/project_Abnormal-Distribution/milestone4_Abnormal-Distribution/presentation.pdf)


## Video Presentation
* [Link Here](https://youtu.be/IgKKCww1svo)


## Medium Article
* [Link Here](https://medium.com/@beri.rohit/b39171ba445c?source=friends_link&sk=799ef49570e3b88888e2e8dcd06fb94a)


## Contents

------------
    
    ├── README.md
    ├── 10K's
    │   └── 10Ks_EDA_Model.ipynb
    ├── base-model
    │   └── Baseline_Model.ipynb
    ├── finnhub
    │   ├── Finnhub full to Mongo.ipynb
    │   ├── Finn_articles_EDA.ipynb
    │   └── TFRecords_FinnhubNews_Pipeline.ipynb
    ├── key-developments
    │   └── CIQCompustat_keydev_model.ipynb
    ├── new model
    │   ├── Language_Training.ipynb
    │   └── Work_towards_Model.ipynb
    ├── sentiment pipeline
    │   ├── Lean_Pipeline.ipynb
    │   └── Sentiment.ipynb
    ├── tiingo
    │   ├── Tiingo+FinnHub_News_fin_BERT_Lean.ipynb
    │   ├── Tiingo+FinnHub_News_fin_BERT_Lean_Master.ipynb
    │   ├── Tiingo+FinnHub_News_fin_BERT_Lean_Master_HS_extraction.ipynb
    │   ├── Tiingo_News_BERT_Feature_Extraction.ipynb
    │   └── Tiingo_News_to_MongoDB_Atlas.ipynb
    ├── visualizations
    │   └── Visualization_of_attention.ipynb
    └── zipline
        └── Zipline.ipynb

--------

## Notebooks

* **10Ks_EDA_Model.ipynb:**

* **Baseline_Model.ipynb:** 

* **Finnhub full to Mongo.ipynb:** 
* **Finn_articles_EDA.ipynb:** 
* **TFRecords_FinnhubNews_Pipeline.ipynb:** 

* **CIQCompustat_keydev_model.ipynb:** 

* **Language_Training.ipynb:** 
* **Work_towards_Model.ipynb:** 
* **sentiment pipeline:** 
* **Lean_Pipeline.ipynb:** 
* **Sentiment.ipynb:** 

* **Tiingo+FinnHub_News_fin_BERT_Lean.ipynb:** 
* **Tiingo+FinnHub_News_fin_BERT_Lean_Master.ipynb:** 
* **Tiingo+FinnHub_News_fin_BERT_Lean_Master_HS_extraction.ipynb:** 
* **Tiingo_News_BERT_Feature_Extraction.ipynb:** 
* **Tiingo_News_to_MongoDB_Atlas.ipynb:** 

* **Visualization_of_attention.ipynb:** 

* **Zipline.ipynb:** 
