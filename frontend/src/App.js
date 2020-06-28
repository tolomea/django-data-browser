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
import { doGet } from "./Util";

const assert = require("assert");

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
      model: "",
      fields: [],
      filters: [],
      ...empty,
    };
  }

  fetchResults(state) {
    const url = getUrlForQuery(this.props.config.baseUrl, state, "json");

    return doGet(url).then((response) => {
      response &&
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
      .then((response) => response.json())
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
          this.setState(e.state);
          this.fetchResults(e.state).catch(handleError);
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
      <div id="body">
        <Logo />
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
