import React from "react";
import "./App.css";
import { HomePage, QueryPage } from "./Components";
import { Query, getUrlForQuery } from "./Query";
const assert = require("assert");
let controller;

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
        this.setState({ results: response.results });
        return response;
      });
  }

  componentDidMount() {
    const reqState = {
      model: this.state.model,
      fields: this.state.fields,
      filters: this.state.filters,
      results: [],
    };
    window.history.replaceState(
      reqState,
      null,
      getUrlForQuery(this.props.config.baseUrl, this.state, "html")
    );
    this.fetchResults(this.state).catch(() => null);
    window.onpopstate = (e) => {
      this.fetchResults(e.state).catch(() => null);
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
    };
    window.history.pushState(
      request,
      null,
      getUrlForQuery(this.props.config.baseUrl, newState, "html")
    );
    this.fetchResults(newState)
      .then((response) => {
        response.results = [];
        assert.deepEqual(request, response);
      })
      .catch(() => null);
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
