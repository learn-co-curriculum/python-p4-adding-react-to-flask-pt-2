# Adding React to Flask, Part 2

## Learning Goals

- Use React and Flask together to build beautiful and powerful web applications.
- Organize client and server code so that it is easy to understand and maintain.

***

## Key Vocab

- **Full-Stack Development**: development of a frontend and a backend for an
  application. True full-stack development includes a database, a logic/server
  layer, and a frontend built in JavaScript, HTML, and CSS.
- **Backend**: the layer of a full-stack application that handles business logic
  and other programmatic tasks that users do not or should not see. Can be
  written in many languages, including Python, Java, Ruby, PHP, and more.
- **Frontend**: the layer of a full-stack application that users see and
  interact with. It is always written in the frontend languages: JavaScript,
  HTML, and CSS. (_There are others now, but they are based on these three._)
- **Cross-Origin Resource Sharing (CORS)**: a method for a server to indicate
  any ports (or other identifiers) for servers that can share its resources.
- **Transmission Control Protocol (TCP)**: a protocol that defines how computers
  send data to each other. A connection is formed and stays active until the
  applications on either end have finished sending data to one another.
- **Hypertext Transfer Protocol (HTTP)**: a stateless protocol where
  applications communicate for the length of time that it takes for data to be
  transferred.
- **Websocket**: a protocol that allows clients and servers to communicate with
  one another in both directions. The bidirectional nature of websocket
  communication allows a connected state to be generated and the connection
  maintained until it is terminated by one side. This allows for speedy and
  seamless connections between frontends and backends.

***

## Introduction

Now that we've built several Flask backends and reviewed what goes into a
React frontend, let's build a new full-stack application from scratch.

***

## Generating a React Application

To get started, let's spin up our React application using `create-react-app`:

```console
$ npx create-react-app client --use-npm
```

This will create a new React application in a `client` folder, and will use npm
instead of yarn to manage our dependencies.

When we're running React and Flask in development, we'll need two separate
servers running on different ports — we'll run React on port 4000, and
Flask on port 5555. Whenever we want to make a request to our Flask API from
React, we'll need to make sure that our requests are going to port 5555.

We can simplify this process of making requests to the correct port by using
`create-react-app` in development to [proxy the requests to our API][proxy].
This will let us write our network requests like this:

```js
fetch("/movies");
// instead of fetch("http://localhost:5555/movies")
```

To set up this proxy feature, open the `package.json` file in the `client`
directory and add this line at the top level of the JSON object:

```json
"proxy": "http://localhost:5555"
```

Let's also update the "start" script in the the `package.json` file to specify a
different port to run our React app in development:

```json
"scripts": {
  "start": "PORT=4000 react-scripts start"
}
```

With that set up, let's try running our servers! In your terminal, run Flask:

```console
$ Flask s
```

Then, open a new terminal, and run React:

```console
$ npm start --prefix client
```

This will run `npm start` in the client directory. Verify that your app is
working by visiting:

- [http://localhost:4000](http://localhost:4000) to view the React application
- [http://localhost:5555/movies](http://localhost:5555/movies) to view the Flask
  application

We can also see how to make a request using `fetch`. In the React application,
update your `App.js` file with the following code:

```jsx
import { useEffect } from "react";

function App() {
  useEffect(() => {
    fetch("/movies")
      .then((r) => r.json())
      .then((movies) => console.log(movies));
  }, []);

  return <h1>Hello from React!</h1>;
}

export default App;
```

This will use the `useEffect` hook to fetch data from our Flask API, which you
can then view in the console.

## Running React and Flask Together

Since we'll often want to run our React and Flask applications together, it can
be helpful to be able to run them from just one command in the terminal instead
of opening multiple terminals.

To facilitate this, we'll use the excellent [foreman][] gem. Install it:

```console
$ gem install foreman
```

Foreman works with a special kind of file known as a Procfile, which lists
different processes to run for our application. Some hosting services, such as
Heroku, use a Procfile to run applications, so by using a Procfile in
development as well, we'll simplify the deploying process later.

In the root directory, create a file `Procfile.dev` and add this code:

```txt
web: PORT=4000 npm start --prefix client
api: PORT=5555 Flask s
```

Then, run it with Foreman:

```console
$ foreman start -f Procfile.dev
```

This will start both React and Flask on separate ports, just like before; but
now we can run both with one command!

**There is one big caveat to this approach**: by running our client and server
in the same terminal, it can be more challenging to read through the server logs
and debug our code. Furthermore, `byebug` will not work. If you're doing a lot of
debugging in the terminal, you should run the client and server separately to
get a cleaner terminal output and allow terminal-based debugging with `byebug`.

You can run each application separately by opening two terminal windows and
running each of these commands in a separate window:

```console
$ npm start --prefix client
$ Flask s
```

This will run React on port 4000 (thanks to the configuration in the
`client/package.json` file), and Flask on port 5555.

## Conclusion

In the past couple lessons, we've seen how to put together the two pieces we'll
need for full-stack applications by using `Flask new` to create a new Flask API,
and `create-react-app` to create a React project. Throughout the rest of this
module, we'll focus on how our two applications communicate and share data.

## Check For Understanding

Before you move on, make sure you can answer the following questions:

1. What options do you have for running Flask and React at the same time?
2. What are the advantages and disadvantages of using `foreman` as described in
   this lesson?

## Resources

- [Proxying API Requests in Create React App][proxy]

[proxy]: https://create-react-app.dev/docs/proxying-api-requests-in-development/
[foreman]: https://github.com/ddollar/foreman
