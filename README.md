[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.10211531.svg)](https://doi.org/10.5281/zenodo.14014887)
[![GitHub Release](https://img.shields.io/badge/release-v1.0.1.1-blue)](https://github.com/SE-vrs-organization/slash-backend)
[![Black Python](https://github.com/SE-vrs-organization/slash-backend/actions/workflows/blackformatting.yaml/badge.svg)](https://github.com/SE-vrs-organization/slash-backend/actions/workflows/blackformatting.yaml)
[![GitHub license](https://img.shields.io/github/license/SE-vrs-organization/slash-backend)](https://github.com/SE-vrs-organization/slash-backend/blob/main/License.md)
<a href="https://github.com/SE-vrs-organization/slash-backend/issues"><img alt="GitHub issues" src="https://img.shields.io/github/issues/SE-vrs-organization/slash-backend"></a>
<a href="https://github.com/SE-vrs-organization/slash-backend/issues"><img alt="GitHub closed issues" src="https://img.shields.io/github/issues-closed/SE-vrs-organization/slash-backend">
<a href="https://github.com/SE-vrs-organization/slash-backend/pulls"><img alt="GitHub pull requests" src="https://img.shields.io/github/issues-pr/SE-vrs-organization/slash-backend">

<p align="center">
    <a href="https://github.com/SE-vrs-organization/slash-backend/issues/new">Report Bug</a>
    ·
    <a href="https://github.com/SE-vrs-organization/slash-backend/issues/new">Request Feature</a>
</p>

```diff
! All the latest changes in slash-phase6 are in "main" branch.
! Score cards (Rubric) are in "Project 2" folder.
```


Do you love shopping? Are you in search of some good deals while shopping online?! Slash is here to help you look for the best deals!


Slash is a publicly accessible web API framework that allows one to scrape the most popular e-commerce websites to get the best deals on the searched items across multiple e-commerce websites. Currently supported websites include [Walmart](https://www.walmart.com/), [Target](https://www.target.com/), [BestBuy](https://www.bestbuy.com/), and [EBay](https://www.ebay.com/).
- **Fast**: With slash, you can save over 50% of your time by comparing deals across websites within seconds
- **Easy**: Slash introduces easy to use public APIs to filter, sort and search through the search results
- **Powerful**: Produces JSON responses that can be easily customised to bring about the desired output

---

<p align="center">
  <a href="#movie_camera-checkout-our-video">Checkout our video</a>
  ::
  <a href="#rocket-installation">Installation</a>
  ::
  <a href="#computer-technology-used">Technology Used</a>
  ::
  <a href="#bulb-use-case">Use Case</a>
  ::
  <a href="#page_facing_up-why">Why</a>
  ::
  <a href="#golf-future-roadmap">Future Roadmap</a>
  ::
  <a href="#sparkles-contributors">Contributors</a>
  ::
  <a href="#Acknowledgement">Acknowledgement</a>
  ::
  <a href="#email-support">Support</a>
  
</p>

---

:movie_camera: Checkout our video
---

[[https://youtu.be/dH4LmxtkDOA]](https://youtu.be/dH4LmxtkDOA)


---

:rocket: Installation
---
1. Clone the Github repositories to a desired location on your computer. You will need [git](https://git-scm.com/) to be preinstalled on your machine. Once the repository is cloned, you will then ```cd``` into the local repository.
```
git clone https://github.com/SE-vrs-organization/slash-backend
```
2. The project slash-backend uses Python 3, so make sure that [Python](https://www.python.org/downloads/) and [Pip](https://pip.pypa.io/en/stable/installation/) are preinstalled. All requirements of the project are listed in the ```requirements.txt``` file. Use pip to install all of those.
```
pip3 install -r requirements.txt
```
3. To run this project, you must install PostgreSQL on your system. If you haven't already installed it, you can download the latest version of PostgreSQL from the official website: [PostgreSQL Downloads](https://www.postgresql.org/download/).

### Configuring Database Connection

Once you've installed PostgreSQL, follow these steps to set up the database connection in your project:

i. Open the database.py file in your project directory.

ii. Locate the top section of the code where you define the database connection settings. It might look something like this:

   ```
   username = 'postgres'
   password = 'admin'
   ```
Replace username and password value from 'postgres', 'pass' with your PostgreSQL username password, respectively.

4. Once all the requirements are installed, use the flask command to run the ```flask``` application.
```
flask run
```
5. While the above is running, go to new terminal and run your UI application by following steps from this repository https://github.com/SE-vrs-organization/slash-ui.
```

:computer: Technology Used
---
- Flask
- Postgre SQL
- Python

:bulb: Use Case
---
* ***Students***: Students coming to university are generally on a budget and time constraint and generally spend hours wasting time to search for products on Websites. Slash is the perfect tool for these students that slashes all the unnecessary details on a website and helps them get prices for a product across multiple websites.Make the most of this tool in the upcoming Black Friday Sale.
* ***Data Analysts***: Finding data for any project is one of the most tedious job for a data analyst, and the datasets found might not be the most recent one. Using slash, they can create their own dataset in real time and format it as per their needs so that they can focus on what is actually inportant.

:page_facing_up: Why
---
- In a market where we are spoilt for choices, we often look for the best deals.  
- The ubiquity of internet access has leveled the retail playing field, making it easy for individuals and businesses to sell products without geographic limitation. In 2020, U.S. e-commerce sales, receiving a boost due to the COVID-19 pandemic, grew 44% and represented more than 21% of total retail sales, according to e-commerce information source Internet Retailer.
- The growth of e-commerce has not only changed the way customers shop, but also their expectations of how brands approach customer service, personalize communications, and provide customers choices.
- E-commerce market has prompted cut throat competition amongst dealers, which is discernable through the price patterns for products of major market players. Price cuts are somewhat of a norm now and getting the best deal for your money can sometimes be a hassle (even while online shopping).
- This is what Slash aims to reduce by giving you an easy to use, all in one place solution for finding the best deals for your products that major market dealers have to offer!
- Slash in its current form is for students who wish to get the best deals out of every e-commerce site and can be used by anyone who is willing to develop an application that consumes these web APIs.
- Future scope includes anything from a web application with a frontend or any Android or IOS application that utilises these Web APIs at their backend. Anyone can build their own custom application on top of these web APIs.

:golf: Phase 6 developments
---
1. 
Added wishlists to track your favorite products.
Revamped the UI in React to improve user experience and help with user retention.
Refactored the application into microservices to scale the UI and backend independently.
Opened the platform to Sellers to directly post their products on the platform.
Added a  cron job for alerting users about price drop of their favorite products.
1. **Wish List Page Enhancement**
   - Description: We have added a price filtering feature that allows users to specify a minimum and maximum price range for their product searches.
   - Functionality: Users can now refine their search results by setting price limits, ensuring they see only products within their budget.
2. **User Interface Revamp**
   - Description: A new sorting feature has been integrated, enabling users to sort products based on their price, from the cheapest to the most expensive.
   - Functionality: This feature enhances the usability of the search function, allowing users to quickly find products that match their price preferences.
3. **Microservices architecture**
   - Description: To aid users in quickly identifying the most affordable options, the cheapest product in any search or filter result is now highlighted.
   - Functionality: This visual cue helps users easily locate the best deals without having to manually compare prices.
4. **Platform for Sellers**
   - Description: Made the UI user friendly and more informative, so that user can use the application easily. The user interface has also been overhauled for a more intuitive and aesthetically pleasing experience.
   - Functionality: Improvements include streamlined navigation, responsive design elements, and a more cohesive color scheme and typography, enhancing overall user interaction with the application.
5. **Price Drop Alert**
   - Description: Most recently added item to wishlist is highlighted and list is displayed based on time of the addition of item to wishlist.
   - Functionality: Recently added items are displayed first on the list. 

<img src = https://github.com/MeryHarikaG/slash-phase5/blob/main/media/Website_2.png>
<img src = https://github.com/MeryHarikaG/slash-phase5/blob/main/media/Website_3.png>
<img src = https://github.com/MeryHarikaG/slash-phase5/blob/main/media/Wishlist%20page.png>

:golf: Future Roadmap
---
Future Roadmap

* Pagination Feature: Implement a pagination feature for the result table allowing to scrape and display multiple results from various e-commerce sites in an organized manner.

* Additional Account Settings: Introduce additional account settings to give users more control over their profiles and preferences, enhancing their personalization and usability.

* Predictive Model: Develop a predictive model that can determine the optimal timing for purchasing the least expensive product from the search results. This feature will provide valuable guidance to users, helping them make informed decisions.

* Enhanced Search Capabilities: Improve the search functionality by introducing advanced search capabilities. This can include options for filtering search results based on ratings, and other relevant criteria, giving users more refined search options.

* Multi-Platform Integration: Expand the platform's capabilities by incorporating search results from various e-commerce platforms such as Etsy, Dick's Sporting Goods, and more. This will provide users with optimized outcomes from a diverse selection of online vendors.

* Social Media Login: Add support for different methods of login, such as Gmail, Facebook, or other social media accounts, to provide users with convenient and secure login options.

* Price Chart Visualization: Introduce a visual representation of price trends for products. This feature can help users understand historical price changes and make more informed purchasing decisions.

* Wishlist Sharing: Enable users to share their wishlists with others. This collaborative feature can be useful for sharing gift ideas or getting recommendations from friends and family.


:sparkles: Contributors
---

1. Shubham Kakride (skakird@ncsu.edu)
2. Rakshita Tantry (rtantry@ncsu.edu)
3. Vinal Bagaria (vbagari@ncsu.edu)



## 🙏 Acknowledgements <a name="Acknowledgement"></a>
We would like to thank Professor Dr Timothy Menzies for helping us understand the process of Maintaining a good Software Engineering project. We would also like to thank the teaching assistants for their support throughout the project.
We would also like to extend our gratitude to previous group : https://github.com/MeryHarikaG/slash-phase5
- [https://streamlit.io/](https://streamlit.io/)
- [https://shields.io/](https://shields.io/)

:email: Support
---
For any queries and help, please reach out to us at : simlyclipse43@gmail.com