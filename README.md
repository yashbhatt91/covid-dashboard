<div align="center">
    <h1>😷 Covid Today</h1>
    <p>A simple dashboard that visualises 🦠 covid-19 data. Go to the demo page to interact with the data or read more about its features below.</p>

## [Demo](http://h0ngm3i.pythonanywhere.com/)

</div>
<br/>

# Quick Start 🚀
```shell
# install requirements
pip install -r requirements.txt

# start flask app
python app.py
```

# Features 🧩

## Interactive world map bubble chart
![map](https://github.com/hongmei-codes/covid_today/blob/master/demo/map.gif)

The dashboard shows a summary of covid-19 cases around the world. The star 🌟 of the dashboard is the interative world map. You can zoom in, zoom out, navigate to which ever country or city you like. Clicking the bubbles will trigger a popup which shows the number of confirmed covid-19 cases on that day for that particular location. From a zoomed out view, bubble density visually highlights the hard hit areas.

Interact with the map at this [demo](http://h0ngm3i.pythonanywhere.com/).

## Responsive page design
![responsive](https://github.com/hongmei-codes/covid_today/blob/master/demo/responsive.gif)

The dashboard is designed to be responsive so that you can view it on any device you like. As the page width changes, the dashboard will readjust and restructure.

## Updated data
Everytime you visit the site, attemps will be made to fetch new data from [John Hopkins University's](https://github.com/CSSEGISandData/COVID-19) latest daily report. This means you will always get the latest update!


# How was this built? 🤔
## Data Manipulation
The dataset used for the project is from [John Hopkins University](https://github.com/CSSEGISandData/COVID-19). Required data for the dashboard is cleaned and extracted using the powerful [pandas](https://github.com/pandas-dev/pandas) library. The latitude and longitude from the dataset are used to plot bubbles on the map.

## Interactive Map  🗺
The map is created using [folium](https://github.com/python-visualization/folium). Bubbles on the map represent number of confirmed covid-19 cases. Greater confirmed case numbers, means larger circles.

To use follium, first install it will pip or anaconda. 
```console
$ pip install folium
```
or
```console
$ conda install folium -c conda-forge
```

Now you can create a folium map object with the code below.
```python
bubble_map = folium.Map(titles='Stamen toner')
```

Next, plot bubbles to any coordinates using the   `.Circle()`  method.
```python
folium.Circle(location=[-36, 45], radius=1000, color='red').app_to(bubble_map)
```

## Web application
This web app is created using [flask](https://github.com/pallets/flask). This lighweight framework is easy to work with and can speed up the development process. That is why it was chosen for this project. Try out this web app [here](http://h0ngm3i.pythonanywhere.com/)

## Responsiveness
CSS styling is used to make the site responsive. To restructure the different components as width changes, you can use media queries.
```css
@media (max-width: 1000px) {
  .dash {
    flex-direction: column;
  }
```

## Deploying a Flask app
Deploying a flask app to [pythonanywhere](https://www.pythonanywhere.com/) is fairly simple. You need to follow these steps.

1. sign up for an account at [pythonanywhere](https://www.pythonanywhere.com/)
2. upload your code to github
3. open the terminal on pythonanywhere and clone your github repository
4. configure wsgi.py to add in the correct path to your flask app folder and import your app.py.
5. reload your web app and go to your project url to see your deployed web app.

## Technology used
- [X] python
- [X] pandas
- [X] folium
- [X] flask
- [X] html
- [X] css
- [X] pythonanywhere
