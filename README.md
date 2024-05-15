# InferGPT: your local personalised AI agent

InferGPT's mission is to be an AI that knows you better than your best friend. A system that personalises to who you are and what you care about. We want to build something that can:

🔗 Ingest data about you from various sources (with your permission of course)  
💡 Have deep and personal conversations without having to answer lots of questions - it will already infer your needs, make personalised recommendations and remember all your conversations.  
🎯 Help you set and keep track of goals.  
🏗️ Carry out tasks: this is an agent after all - it will go away and action stuff for you!  
🔮 Predict what you need before you need it!  

We aim to be able to answer complex questions that require a deep understanding of someone to effectively answer, such as:
1) How can i be better with my finances?
2) I'm trying to lose weight but its not working, why? 
3) I'm learning to code, can you create a tailored learning plan?  

## Roadmap & Docs
Want more context about how it works, our roadmap and documentation? Check out the [wiki](https://github.com/WaitThatShouldntWork/InferGPT/wiki)

For further reading on InferGPT's components, see any of the following
- [Full system testing](test/README.md)
- [Data persistence](data/README.md)
- [Backend](backend/README.md)
- [Frontend](frontend/README.md)
- [Assets](assets/README.md)
- [Testing](test/README.md)
- [Financial Bot](financialhealthcheckScottLogic/README.md)

## Contribute
See [the contribution guide](CONTRIBUTING.md) for further guidance. Note this guide is in progress!

## Getting Started

In the top-right corner of the page, click Fork.

On the next page, select your GitHub account to create the fork under.
Wait for the forking process to complete. You now have a copy of the repository in your GitHub account.

### Clone the Repository

To clone the repository, you need to have Git installed on your system. Use the [official Git installer](https://git-scm.com/download/win) or [follow the terminal commands guide](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git).

Once you have Git installed, follow these steps:

- Open your preferred terminal.
- Navigate to the directory where you want to clone the repository.
- Run the git clone command for the fork you just created.

### Initial configuration

There is a example property file `.env.example` at the root of this project.

Configuration steps:

- Copy the `.env.example` file at the root of this project.
- Rename the copied file as `.env`.
- Update the `.env` file with your wanted configuration following the guidance in the file.


### Running the application

There are a few ways to run the application:

1. **Docker Compose** - run the entire application within Docker containers configured by Docker Compose.
2. **Locally** - run local instances of the front-end, back-end and a neo4j database.
3. **Individual Docker Containers** - you may choose to run individual components within a Docker container.

For ease of use, we would recommended that you run the application using **Docker Compose**.

For instructions on how to run indivdual components locally or within Docker containers, refer to appropriate READMEs:

- [frontend README](frontend/README.md)
- [backend README](backend/README.md)
- [data README](data/README.md)

#### Running with Docker Compose

- **Ensure Docker is installed and running**. The easiest way to do this is by using the Docker Desktop app (install it from [docker.com](docker.com) if you don't have it).
- In the root directory of the project run `docker compose up`
> [!WARNING]  
> the first time you do this it may take longer as the compose file builds the images.

- View the frontend at [localhost:8650](http://localhost:8650)
- View the Neo4j Browser at [localhost:7474](http://localhost:7474)
- Type the phrase "healthcheck" into the frontend UI to test if everything is connected successfully
 
### Usage
Coming

### LICENCE
See [LICENCE.md](LICENCE.md)
