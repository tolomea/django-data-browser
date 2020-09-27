import * as Sentry from "@sentry/browser";
import React, { useState } from "react";
import { sortBy } from "lodash";
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

const BOOTING = "Booting...";
const LOADING = "Loading...";
const ERROR = "Error";

class QueryApp extends React.Component {
  handleError(e) {
    if (e.name !== "AbortError") {
      this.props.setStatus(ERROR);
      console.log(e);
      Sentry.captureException(e);
    }
  }

  fetchResults(state) {
    this.props.setStatus(LOADING);
    const url = getUrlForQuery(this.props.config.baseUrl, state, "json");

    return doGet(url).then((response) => {
      this.props.setQuery({
        ...this.props.query,
        body: response.body,
        cols: response.cols,
        rows: response.rows,
        length: response.length,
        formatHints: response.formatHints,
        filterErrors: response.filterErrors,
      });
      this.props.setStatus(fetchInProgress ? LOADING : undefined);
      return response;
    });
  }

  popstate(e) {
    this.props.setQuery(e.state);
    this.fetchResults(e.state).catch(this.handleError.bind(this));
  }
  popstate = this.popstate.bind(this);

  componentDidMount() {
    const { model, fieldStr, queryStr, config } = this.props;
    const url = `${config.baseUrl}query/${model}/${fieldStr}.query${queryStr}`;
    doGet(url).then((response) => {
      const reqState = {
        model: response.model,
        fields: response.fields,
        filters: response.filters,
        limit: response.limit,
        ...empty,
      };
      this.props.setQuery(reqState);
      this.props.setStatus(LOADING);
      window.history.replaceState(
        reqState,
        null,
        getUrlForQuery(this.props.config.baseUrl, reqState, "html")
      );
      window.addEventListener("popstate", this.popstate);
      this.fetchResults(this.props.query).catch(this.handleError.bind(this));
    });
  }

  componentWillUnmount() {
    window.removeEventListener("popstate", this.popstate);
  }

  handleQueryChange(queryChange, reload = true) {
    const newState = { ...this.props.query, ...queryChange };

    this.props.setQuery(newState);
    if (!reload) return;

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
        const res = { ...response, ...empty };
        res.filters = sortBy(res.filters, ["pathStr"]);
        const req = { ...request };
        req.filters = sortBy(req.filters, ["pathStr"]);
        assert.deepStrictEqual(res, req);
      })
      .catch(this.handleError.bind(this));
  }

  render() {
    if (this.props.status === BOOTING) return "";
    const query = new Query(
      this.props.config,
      this.props.query,
      this.handleQueryChange.bind(this)
    );
    return (
      <QueryPage
        overlay={this.props.status}
        query={query}
        sortedModels={this.props.config.sortedModels}
        allModelFields={this.props.config.allModelFields}
        baseUrl={this.props.config.baseUrl}
        {...this.props.query}
      />
    );
  }
}

function Bob(props) {
  const { model, fieldStr } = useParams();
  const [status, setStatus] = useState(BOOTING);
  const [query, setQuery] = useState({
    model: "",
    fields: [],
    filters: [],
    limit: props.config.defaultRowLimit,
    ...empty,
  });
  return (
    <QueryApp
      {...{
        model,
        status,
        setStatus,
        query,
        setQuery,
        ...props,
      }}
      fieldStr={fieldStr || ""}
      queryStr={useLocation().search}
    />
  );
}

function App(props) {
  const { baseUrl, sortedModels, allModelFields, canMakePublic } = props;
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
            <HomePage {...{ sortedModels, allModelFields, baseUrl }} />
          </Route>
        </Switch>
      </div>
    </BrowserRouter>
  );
}

export default App;
