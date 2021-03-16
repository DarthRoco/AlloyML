# AlloyML
An Alloy Recommender System Based on Genetic Algorithms and Neural Networks

---

This Project was done under the <b>Clutch</b> Special Interest Group of <a href="https://iste.nitk.ac.in/">ISTE-NITK</a>

The Project was done entirely in <b>Python 3</b> and its various libraries<br>

---

The Project had the following main phases:


<dl>
  <dt>1)Web scraping and Dataset acquistion:</dt>
  <ul>
  <li>Scraped alloy property data from various online sources</li>
    <li>Used Dataset from <a href="https://data.mendeley.com/datasets/msf6jzm52g/1">here</a></li>
    <li>Performed data preprocessing to be able to be fed into Neural Network </li>
  <li> Libraries used: BeautifulSoup4, requests, Pandas ,Pickle </li>
  </ul>
  <dt>2)Model Training:</dt>
  <ul>
    <li>Experimented with different architechtures to obtain best fit model for each of the dataset target properties namely Tensile Strength,Yield Strength,Elongation Limit</li>
    <li>Performed GridSearch to optimise hyperparamters</li>
    <li>Further details regarding model architectures can be found <a href="https://github.com/DarthRoco/AlloyML/blob/main/AlloyML/models/README.md">here</a></li>
    <li>Libraries Used: Tensorflow,scikit-learn,matplotlib</li>
  </ul>
    <dt>3)Build a Genetic Algorithm Solver</dt>
  <ul>
   <li>The Genetic Algorithm takes input as desired alloy property and outputs theoretical composition of such an alloy</li>
    <li>This is done by treating trained neural network as blackbox with GA optimising on its outputs</li>
    <li>Libraries used: Tensorflow,PyGAD</li>
  </ul>
  <dt>4)Build GUI</dt>
  <ul>
  <li>Designed simple Graphical User Interface to abstract code implementation from end user</li>
  <li>Libraries used: tkinter,PyGAD,Tensorflow</li>
  </ul>
</dl>

---

<em>NOTE: <br>While the GUI presented pertains to only Steels,the methodology suggested can be used for any alloy family provided appropriate dataset is available
  <br>
The resulting composition suggested by GA is purely theoretical and as of now has not been verified experimentally.</em>
