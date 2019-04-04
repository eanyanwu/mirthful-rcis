## Why React?

TODO: Explain benefits, especially compared to previous version

## Why npm, webpack, babel and all these extra tools?

At its simplest, a webpage is just one `index.html` file. You might be asking yourself why we need all these extra tools.
Fair question. This is no place to go on a rant concerning the Javascript community, so I'll stick to explaining why we need thse three tools. 
We actually only need babel. But because we need babel, npm becomes necessary.
Webpack is a nice to have.

Let me explain:
- Babel: We will be using the react framework. Normally, you could just stick this in a `<script>` tag and voila. However, I would argue, one of the best things about React is its HTML-like syntax for describing the creation of components. This syntax is called JSX. Unfortunately, it is not supported by all browsers, so a "transpiler" is needed to convert it to vanilla javascript before being fed into a browser. Babel is this transpiler. Take a look at [this](https://reactjs.org/docs/add-react-to-a-website.html#optional-try-react-with-jsx) article.
- Webpack: I only use webpack because it lets me start local development server with automatic code reloading whenever any files in the project change. It is as easy as `npm run start`

## Resources for learning about React:

TODO: Included FREE resources
