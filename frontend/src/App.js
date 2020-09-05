import * as Sentry from "@sentry/browser";
import React from "react";
import {
  BrowserRouter,
  Switch,
  Route,
  useParams,
  useLocation,
} from "react-router-dom";
import "./App.css";
import { HomePage, QueryPage, Logo, EditSavedView } from "./Components";
import { Query, getUrlForQuery, empty } from "./Query";
import { doGet, fetchInProgress } from "./Util";

const assert = require("assert");

class QueryApp extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      booting: true,
      loading: false,
      error: undefined,
      model: "",
      fields: [],
      filters: [],
      limit: props.config.defaultRowLimit,
      ...empty,
    };
  }

  handleError(e) {
    if (e.name !== "AbortError") {
      this.setState({ error: true, loading: false });
      console.log(e);
      Sentry.captureException(e);
    }
  }

  fetchResults(state) {
    this.setState({ loading: true });
    const url = getUrlForQuery(this.props.config.baseUrl, state, "json");

    return doGet(url).then((response) => {
      this.setState({
        body: response.body,
        cols: response.cols,
        rows: response.rows,
        length: response.length,
        formatHints: response.formatHints,
        filterErrors: response.filterErrors,
        loading: fetchInProgress,
        error: undefined,
      });
      return response;
    });
  }

  popstate(e) {
    this.setState(e.state);
    this.fetchResults(e.state).catch(this.handleError.bind(this));
  }
  popstate = this.popstate.bind(this);

  componentDidMount() {
    const { model, fieldStr, queryStr, config } = this.props;
    const url = `${config.baseUrl}query/${model}/${fieldStr}.query${queryStr}`;
    doGet(url).then((response) => {
      const reqState = {
        booting: false,
        loading: true,
        error: undefined,
        model: response.model,
        fields: response.fields,
        filters: response.filters,
        limit: response.limit,
        ...empty,
      };
      this.setState(reqState);
      window.history.replaceState(
        reqState,
        null,
        getUrlForQuery(this.props.config.baseUrl, reqState, "html")
      );
      window.addEventListener("popstate", this.popstate);
      this.fetchResults(this.state).catch(this.handleError.bind(this));
    });
  }

  componentWillUnmount() {
    window.removeEventListener("popstate", this.popstate);
  }

  handleQueryChange(queryChange) {
    this.setState(queryChange);
    const newState = { ...this.state, ...queryChange };
    const request = {
      model: newState.model,
      fields: newState.fields,
      filters: newState.filters,
      limit: newState.limit,
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
      .catch(this.handleError.bind(this));
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
        baseUrl={this.props.config.baseUrl}
        {...this.state}
      />
    );
  }
}

function Bob(props) {
  const { model, fieldStr } = useParams();
  return (
    <QueryApp
      {...props}
      model={model}
      fieldStr={fieldStr || ""}
      queryStr={useLocation().search}
    />
  );
}

function App(props) {
  const { baseUrl, sortedModels, canMakePublic } = props;
  return (
    <BrowserRouter basename={baseUrl}>
      <Logo />
      <div id="body">
        <Switch>
          <Route path="/query/:model/:fieldStr?.html">
            <Bob config={props} {...{ sortedModels }} />
          </Route>
          <Route path="/views/:pk.html">
            <EditSavedView {...{ baseUrl, canMakePublic }} />
          </Route>
          <Route path="/">
            <HomePage {...{ sortedModels, baseUrl }} />
          </Route>
        </Switch>
      </div>
    </BrowserRouter>
  );
}

export default App;
