

<!-- PROJECT LOGO -->
<br />
<p align="center">
  <a href="https://github.com/evanokeefe39/TwitterSentimentAnalysis">
    
  </a>

  <h2 align="center">Twitter Sentiment Analysis with Python and Kubernetes</h2>

  <p align="center">
    This repo aims to provide a quickstart for those interested in building python applications in combination with elastic cloud. It's aimed at intermediate python developers with a very basic knowledge of cloud computing concepts. The example provided here uses the Tweepy library and TextBlob library to do sentiment analysis of twitter posts relating to Tesla and Elon Musk. It builds on the original article posted on the <a href="https://realpython.com/twitter-sentiment-python-docker-elasticsearch-kibana/">Real Python</a> blog but has been updated for the current version [7.9] of elastic cloud as well as a few extra features. 
    <a href="https://medium.com/@twentyfoursevenevan">Full Tutorial</a>  
    <br/>
    <br> 
  </p>
</p>


### Built With

* [Twitter API](https://developer.twitter.com/en/docs/twitter-api)
* [Alpha Vantage API](https://www.alphavantage.co/documentation/)
* [Google Cloud](https://cloud.google.com/)
* [Docker for Desktop](https://www.docker.com/products/docker-desktop)
* [Cloude Code](https://cloud.google.com/code)



[![Product Name Screen Shot][product-screenshot]](https://medium.com/@twentyfoursevenevan)
<!-- GETTING STARTED -->
## Getting Started

To get the app running locally follow these steps

### Prerequisites

You will need [Docker for Desktop](https://www.docker.com/products/docker-desktop) to run containers locally. On Windows this will require also enabling [WSL2 backend](https://docs.microsoft.com/en-us/windows/wsl/install-win10). You can also refer to more detailed guide here if unfamiliar with linux and containerization.

A local python installation isn't technically required to run the app since Docker builds an installation of python into the image. You will however need python if you wish to utilize Jupyter Notebooks.

Request access to the [Twitter API](https://developer.twitter.com/en/apply-for-access). Once you have access copy and paste your API keys into the `.env` file in the root directory of the cloned repo. I've left my old keys in the code so you can see what they should look like (my actual keys have been regenerated already). You can also copy and paste these keys into the `app-dev.yaml` in the Manifests folder (the environment variables are named the same as in the `.env` file).

Get an Alpha Vantage API key and copy and paste it into the required cell in the jupyter notebook (the variable named "api_key").

### Installation

1. Clone the repo
```sh
git clone https://github.com/evanokeefe39/TwitterSentimentAnalysis.git
```
2. Build the Docker stack 
```sh
docker-compose build
```
4. Run the Docker stack
```sh
docker-compose up
```



<!-- USAGE EXAMPLES -->
## Usage

To access the kibana homepage got to http://localhost:5601, if you go to the dashboard tab it should automatically prompt you to make an "index pattern". Just type in "sentiment*" and click create. You can then start creating visualization using all data indexed under the sentiment index we created in our python code or anything matching the pattern "sentiment*" 

i.e we could create another python script that indexes under "sentiment_Nikola" or "sentiment_ElectricVehicles" and these would match due to the wildcard character on the end of "sentiment" in our pattern.

_For more examples, please refer to the [Full Tutorial](https://medium.com/@twentyfoursevenevan)_



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.



<!-- CONTACT -->
## Contact

Evan O'Keefe  - evan.okeefe39@gmail.com

<!-- ACKNOWLEDGEMENTS -->
## Acknowledgements

* [Real Python - Twitter Sentiment Analysis – Python, Docker, Elasticsearch, Kibana](https://realpython.com/twitter-sentiment-python-docker-elasticsearch-kibana/)

[product-screenshot]: images/demo.PNG