import * as Sentry from "@sentry/browser";
import React from "react";
import "./App.css";
import { HomePage, QueryPage } from "./Components";
import { Query, getUrlForQuery, empty } from "./Query";
import {
  BrowserRouter,
  Switch,
  Route,
  useParams,
  useLocation,
} from "react-router-dom";

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

class QueryApp extends React.Component {
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
    const { model, fieldStr, queryStr, config } = this.props;
    const url = `${config.baseUrl}query/${model}/${fieldStr}.query${queryStr}`;
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

  componentWillUnmount() {
    window.onpopstate = () => {};
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
    return (
      <QueryPage
        query={query}
        sortedModels={this.props.config.sortedModels}
        version={this.props.config.version}
        {...this.state}
      />
    );
  }
}

function Bob(props) {
  const params = useParams();
  return (
    <QueryApp
      {...props}
      model={params.model}
      fieldStr={params.fieldStr || ""}
      queryStr={useLocation().search}
    />
  );
}

function App(props) {
  const { config, sortedModels } = props;
  return (
    <BrowserRouter basename={config.baseUrl}>
      <Switch>
        <Route path="/query/:model/:fieldStr?.html">
          <Bob {...{ config, sortedModels }} />
        </Route>
        <Route path="/">
          <HomePage
            sortedModels={config.sortedModels}
            savedViews={config.savedViews}
            version={config.version}
          />
        </Route>
      </Switch>
    </BrowserRouter>
  );
}

export default App;
