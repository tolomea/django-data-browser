import * as Sentry from "@sentry/browser";
import React from "react";
import "./App.css";
import { HomePage, QueryPage } from "./Components";
import { Query, getUrlForQuery, empty } from "./Query";
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
    this.state = {
      booting: true,
      version: props.config.version,
      model: "",
      fields: [],
      filters: [],
      ...empty,
    };
  }

  fetchResults(state) {
    const url = getUrlForQuery(this.props.config.baseUrl, state, "json");

    if (controller) controller.abort();
    controller = new AbortController();

    if (!state.model)
      // TODO do we need this clause?
      return Promise.resolve({
        model: "",
        fields: [],
        filters: [],
        ...empty,
      });

    return fetch(url, { signal: controller.signal })
      .then((res) => res.json())
      .then((response) => {
        if (response.version !== this.state.version) {
          console.log("Version mismatch, hard reload");
          window.location.reload(true);
        }
        delete response.version;
        return response;
      })
      .then((response) => {
        this.setState({
          body: response.body,
          cols: response.cols,
          rows: response.rows,
          filterErrors: response.filterErrors,
        });
        return response;
      });
  }

  componentDidMount() {
    const loc = window.location;
    const path =
      (loc.pathname.endsWith(".html")
        ? loc.pathname.slice(0, -5)
        : loc.pathname) + ".query";
    const url = `${loc.protocol}//${loc.host}${path}${loc.search}`;
    fetch(url)
      .then((res) => res.json())
      .then((response) => {
        const reqState = {
          booting: false,
          model: response.model,
          fields: response.fields,
          filters: response.filters,
          ...empty,
        };
        this.setState(reqState);
        window.history.replaceState(
          reqState,
          null,
          getUrlForQuery(this.props.config.baseUrl, reqState, "html")
        );
        window.onpopstate = (e) => {
          this.fetchResults(e.state).catch(handleError);
          this.setState(e.state);
        };
        this.fetchResults(this.state).catch(handleError);
      });
  }

  handleQueryChange(queryChange) {
    this.setState(queryChange);
    const newState = { ...this.state, ...queryChange };
    const request = {
      model: newState.model,
      fields: newState.fields,
      filters: newState.filters,
      ...empty,
    };
    window.history.pushState(
      request,
      null,
      getUrlForQuery(this.props.config.baseUrl, newState, "html")
    );
    this.fetchResults(newState)
      .then((response) => {
        response = { ...response, ...empty };
        assert.deepStrictEqual(response, request);
      })
      .catch(handleError);
  }

  render() {
    if (this.state.booting) return "";
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
