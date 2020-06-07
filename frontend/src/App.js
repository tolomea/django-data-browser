import * as Sentry from "@sentry/browser";
import React from "react";
import "./App.css";
import { HomePage, QueryPage } from "./Components";
import { Query, getUrlForQuery } from "./Query";
const assert = require("assert");
let controller;

function handleError(e) {
  if (e.name === "AbortError") {
    console.log("request aborted");
  } else {
    console.log(e);
    Sentry.captureException(e);
  }
}

class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = props.initialState;
  }

  fetchResults(state) {
    const url = getUrlForQuery(this.props.config.baseUrl, state, "json");

    if (controller) controller.abort();
    controller = new AbortController();

    return fetch(url, { signal: controller.signal })
      .then((res) => res.json())
      .then((response) => {
        if (response.version !== this.state.version)
          window.location.reload(true);
        delete response.version;
        return response;
      })
      .then((response) => {
        this.setState({
          results: response.results,
          filterErrors: response.filterErrors,
        });
        return response;
      });
  }

  componentDidMount() {
    const reqState = {
      model: this.state.model,
      fields: this.state.fields,
      filters: this.state.filters,
      results: [],
      filterErrors: [],
    };
    window.history.replaceState(
      reqState,
      null,
      getUrlForQuery(this.props.config.baseUrl, this.state, "html")
    );
    this.fetchResults(this.state).catch(handleError);
    window.onpopstate = (e) => {
      this.fetchResults(e.state).catch(handleError);
      this.setState(e.state);
    };
  }

  handleQueryChange(queryChange) {
    this.setState(queryChange);
    const newState = { ...this.state, ...queryChange };
    const request = {
      model: newState.model,
      fields: newState.fields,
      filters: newState.filters,
      results: [],
      rows: [],
      cols: [],
      filterErrors: [],
    };
    window.history.pushState(
      request,
      null,
      getUrlForQuery(this.props.config.baseUrl, newState, "html")
    );
    this.fetchResults(newState)
      .then((response) => {
        response.results = [];
        response.cols = [];
        response.rows = [];
        response.filterErrors = [];
        assert.deepEqual(response, request);
      })
      .catch(handleError);
  }

  render() {
    const query = new Query(
      this.props.config,
      this.state,
      this.handleQueryChange.bind(this)
    );
    if (this.state.model)
      return (
        <QueryPage
          query={query}
          sortedModels={this.props.config.sortedModels}
          version={this.props.config.version}
          {...this.state}
        />
      );
    else
      return (
        <HomePage
          query={query}
          sortedModels={this.props.config.sortedModels}
          savedViews={this.props.config.savedViews}
          version={this.props.config.version}
        />
      );
  }
}

export default App;
