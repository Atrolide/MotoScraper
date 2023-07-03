<img src="https://cdn.discordapp.com/attachments/1090484337897648178/1109444270261284934/logov2.png" alt="MotoScraper Logo" align="left" width="200" style="margin-right: 20px;">

<br><br>
**MotoScraper** is a powerful Discord chat bot designed to scrape data from car sales websites and provide comprehensive information about various cars.<br><br>
With MotoScraper, you can easily search for car listings and retrieve detailed information without manually navigating websites.

<br><br><br><br>
## Key Features:

- **ChatBot:** MotoScraper offers a user-friendly chatbot interface for interacting with the bot. Users can chat with the bot to search for car listings and retrieve detailed information.

- **Filtering Option:** Users can filter car results by brand, allowing them to narrow down their search to specific car manufacturers.

- **Comprehensive Information:** MotoScraper provides all of the necessary and detailed information about various cars, sourced from car sales websites.

- **Ease of Use:** MotoScraper has an intuitive interface and command-based system, making it easy to use.

- **Time Savings:** By automating the process of scraping car sales websites, MotoScraper saves users valuable time.

- **Convenience:** MotoScraper is accessible on Discord, a widely used platform for communication and communities.

- **Continuous Enhancements:** The MotoScraper team regularly adds new features and improves the bot's capabilities.

<br>**MotoScraper aims to make your car search effortless and efficient, providing you with a seamless experience!**<br><br>

<br><br>

## Configuration

**This is a guide on how to run our bot locally**

Before using MotoScraper, make sure you have the following prerequisites installed:

- [Python](https://www.python.org/downloads/) (version 3.9 or above)
- [Git](https://git-scm.com/downloads)

Move to the directory where you want to clone your project to, click righ mouse button and select *Git Bash here*

Then, to clone the repository, run the following command:
```shell
git clone https://github.com/Atrolide/MotoScraper.git
```

Next, [generate a Discord Bot token](https://discordpy.readthedocs.io/en/stable/discord.html) by following the instructions provided.

Then, open the file [env_template](https://github.com/Atrolide/MotoScraper/blob/main/env_template). Replace `your bot token` with the token you generated earlier, change the file name to .env and save.

To run MotoScraper, navigate to the project directory in the terminal and execute the following command:
```shell
python mybot.py
```
Wait until you see following information in console:
```shell
discord.gateway: Shard ID None has connected to Gateway (Session ID: your session id).
```
**The bot should be now up and running!**

<br><br>

## How to Use

MotoScraper is a command-based bot that uses the prefix `/`. Here are the available commands:

### Chatbot Commands:

* **@MotoScraper** -> In order to start chatting you have to ping the bot using this command

* **/help** -> Displays the help message with a list of available commands
* **/olx** -> Scrapes car listings from olx.pl based on the provided car brand
* **/otomoto** -> Scrapes car listings from otomoto.pl based on the provided car brand

### Chart Commands:

* **/olxchart** -> Generates a bar chart of car listings from olx.pl
* **/olxpiechart** -> Generates a pie chart of car listings from olx.pl
* **/otomotochart**-> Generates a bar chart of car listings from otomoto.pl
* **/otomotopiechart** -> Generates a pie chart of car listings from otomoto.pl

<br><br>

## Upcoming Enhancements:
In the next release, we have several exciting enhancements planned to take MotoScraper to the next level:

1. **More Websites:** We plan to expand the bot's capabilities to include additional car sales websites in future releases. 

2. **Bot Hosting:** We will introduce the capability to host the MotoScraper bot, ensuring its availability and reliability round the clock. This will make the bot accessible to users at any time, providing a seamless experience.

3. **More Filtering Options:** Our team is working on providing the users the ability to use more filters such as engine size or horse power.

4. **Database Integration:** We are working on connecting MotoScraper to a database, enabling data storage and retrieval. This will enhance performance and allow for advanced search capabilities and historical data analysis.

5. **Message Broker Integration:** To optimize data retrieval speed and efficiency, we plan to implement a message broker system such as RabbitMQ or Kafka. This enhancement will significantly boost the bot's responsiveness and allow for real-time data updates.

6. **OpenAI API Integration:** We aim to leverage the power of the OpenAI API to enhance the chatbot's user experience. By incorporating natural language processing capabilities, MotoScraper will be able to understand and respond to user queries more intelligently and intuitively.

<br><br>
### Feel free to contribute to MotoScraper by creating pull requests or reporting issues. Your contributions are highly appreciated!
<br><br>
### In case of any problems, bugs or errors, please open an issue, we will try to fix it as soon as possible.
<br><br>

## Preview:
![image](https://github.com/Atrolide/MotoScraper/assets/115810564/41eb8081-86f0-480e-9495-aef161d30885)
![image](https://github.com/Atrolide/MotoScraper/assets/115810564/afc3bb57-5d9e-47fd-ae9d-b85e328bf79b)
![image](https://github.com/Atrolide/MotoScraper/assets/115810564/8ba61893-1766-47a1-97a0-3affe9ae9030)

